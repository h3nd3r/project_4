from agents.base_agent import Agent

class ImplementationAgent(Agent):

    IMPLEMENTATION_PROMPT = """\
    You are a software engineer, who is going to write only the css for the web page in the image that the user sends. 
    Once you are asked to build the page, read the plan.md file, and start coding, write the css to 
    the appropriate files.

    Using vanilla CSS, create the CSS implementation.  Save the CSS to an appropriate file, 
    there are available tools to save it appropriately as a named artifact.
    """

    def __init__(self, name, client, prompt=IMPLEMENTATION_PROMPT, gen_kwargs=None):
        # Initialize your agent here
        super().__init__(name, client, prompt, gen_kwargs)
        pass

class HtmlAgent(Agent):

    HTML_PROMPT = """\
    You are a software engineer, who is going to write only the html for the web page in the image that the user sends. 
    Once you are asked to build the page, read the plan.md file, and start coding, write the html to 
    the appropriate files.

    Using vanilla html, create the html implementation.  Save the html to the appropriate file, 
    there are available tools to save it as an appropriately named artifact.
    """

    def __init__(self, name, client, prompt=HTML_PROMPT, gen_kwargs=None):
        # Initialize your agent here
        super().__init__(name, client, prompt, gen_kwargs)
        pass
    # read plan.md and generate code for one of the milestones
    # could also take feedback to fix milestone


    # # Add other methods as needed

