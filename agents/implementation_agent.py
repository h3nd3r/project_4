from agents.base_agent import Agent

class ImplementationAgent(Agent):

    IMPLEMENTATION_PROMPT = """\
    You are a software engineer, who is going to write only the css or only the html for the web page in the image that the user sends. 
    Once you are asked to build the page, read the plan.md file, and start coding, write the css or html to 
    the appropriate files.

    Using vanilla CSS or vanilla html, create the CSS or html implementation.  Save the CSS or html to an appropriate file, 
    there are available tools to save it appropriately as a named artifact.
    """

    def __init__(self, name, client, prompt=IMPLEMENTATION_PROMPT, gen_kwargs=None):
        # Initialize your agent here
        super().__init__(name, client, prompt, gen_kwargs)
        pass

