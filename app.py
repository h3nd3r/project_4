import base64
from dotenv import load_dotenv
import chainlit as cl
from agent_functions import call_implementation_agent, call_planning_agent
load_dotenv()
import pdb
import json
from helpers import find_all_json

# Note: If switching to LangSmith, uncomment the following, and replace @observe with @traceable
# from langsmith.wrappers import wrap_openai
# from langsmith import traceable
# client = wrap_openai(openai.AsyncClient())

from langfuse.decorators import observe
from langfuse.openai import AsyncOpenAI

client = AsyncOpenAI()

gen_kwargs = {
    "model": "gpt-4o",
    "temperature": 0.2
}

SYSTEM_PROMPT = """\
You are a helpful project manager that helps people create web pages based on images or verbose descriptions \
by coordinating an implementation agent and a planning agent, but not outputing any work yourself. \
If the person has provided an image, use it to guide the creation of the web page. \
If the person has provided a description, use it to guide the creation of the web page. \
If the person hasn't provided anything, ask for an image or description. \

Once you have what is needed, call the planning agent to plan the next step in building the page via json function \
call provided.  

Once the planning agent has provided a plan and written the plan.md file, call the implementation agent to write the html\
for the page to a file via json function call provided. \

Once the implementation agent has written the html file, call the implementation agent again to write the css\
for the page to a file via json function call provided. \

Once the implementation agent has written the css file, call the panning agent again to update the plan.md file \
using the json function call provided. \

If you need to call a function, only output the function call. Call functions \
using json formatted as follows:

# call the implementation agent to write the html or css for the page to a file
{ "function": "call_implementation_agent"}

# call the planning agent to plan the next step in building the page or write a new \
# plan or update an existing plan to a plan.md file
{ "function": "call_planning_agent"}

Call the function provided to have implementation agent to write the html or css for the page to a file. \
Call the function provided to have the planning agent to plan the next step in building the page or write a new \
plan or update an existing plan to a plan.md file.
"""

@observe
@cl.on_chat_start
def on_chat_start():    
    message_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    cl.user_session.set("message_history", message_history)

@observe
async def generate_response(client, message_history, gen_kwargs):
    response_message = cl.Message(content="")
    await response_message.send()

    stream = await client.chat.completions.create(messages=message_history, stream=True, **gen_kwargs)
    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await response_message.stream_token(token)
    
    await response_message.update()

    return response_message

@cl.on_message
@observe
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history", [])

    # Processing images exclusively
    images = [file for file in message.elements if "image" in file.mime] if message.elements else []

    if images:
        print("image")        # Read the first image and encode it to base64
        with open(images[0].path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode('utf-8')
        message_history.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": message.content
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        })
        '''
                message_history.append({"role": "user", "content": message.content})
                response_message = await generate_response(client, message_history, gen_kwargs)
                message_history.append({"role": "assistant", "content": response_message.content})
                cl.user_session.set("message_history", message_history)
        '''

    message_history.append({"role": "user", "content": message.content})
    response_message = await generate_response(client, message_history, gen_kwargs)
    message_history.append({"role": "assistant", "content": response_message.content})
    cl.user_session.set("message_history", message_history)

    if "function" in response_message.content:
        print("function")
        functions = find_all_json(response_message.content)
        #pdb.set_trace()
        for function in functions:
            print(f"while: {function}")
            try:
                #json_message = json.loads(function)
                function_name = function.get("function")
                print("function_name: ", function_name)
                if function_name == "call_implementation_agent":
                    result = await call_implementation_agent(client, message_history)
                elif function_name == "call_planning_agent":
                    result = await call_planning_agent(client, message_history)
                else:
                    result = "Unknown result"
                    
                message_history.append({"role": "system", "content": result})
                response_message = await generate_response(client, message_history, gen_kwargs)
                
                print("response_message: \"", response_message.content, "\"")

            except json.JSONDecodeError:
                print("Error: Unable to parse the message as JSON")
                json_message = None

            message_history.append({"role": "user", "content": message.content})
            message_history.append({"role": "assistant", "content": response_message.content})

        cl.user_session.set("message_history", message_history)

    else:
        print("no function")
        # pdb.set_trace()


if __name__ == "__main__":
    cl.main()
