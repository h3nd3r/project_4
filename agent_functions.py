import sys
import os
import requests
from langfuse.decorators import observe
from langfuse.openai import AsyncOpenAI
from dotenv import load_dotenv
from agents.planning_agent import PlanningAgent
from agents.implementation_agent import ImplementationAgent

load_dotenv()

#@traceable
@observe
async def call_implementation_agent(client, message_history):
    implementation_agent = ImplementationAgent(name="Implementation Agent", client=client)
    response_message = await implementation_agent.execute(message_history)
    return response_message

@observe
async def call_planning_agent(client, message_history):
    print("call_planning_agent() called")
    planning_agent = PlanningAgent(name="Planning Agent", client=client)
    response_message = await planning_agent.execute(message_history)
    return response_message
# Create an instance of the Agent class
