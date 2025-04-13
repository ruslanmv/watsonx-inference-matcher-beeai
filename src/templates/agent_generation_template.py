from pydantic import BaseModel
from beeai_framework.utils.templates import PromptTemplate

class AgentTemplateInput(BaseModel):
    agent_name: str
    purpose: str
    input_format: str
    output_format: str
    tools_required: list[str]

# Template that guides the LLM to generate a structured agent configuration.

agent_generation_template: PromptTemplate = PromptTemplate(
    schema=AgentTemplateInput,
    template="""
You are tasked with generating a software agent configuration. Below are the requirements:

Agent Name: {{agent_name}}
Purpose: {{purpose}}
Input Format: {{input_format}}
Output Format: {{output_format}}
Required Tools:
{{#tools_required}}
- {{.}}
{{/tools_required}}

Instructions:
Create a full Python class that defines the agent with the following capabilities:
- Initialization parameters matching the input format
- Method for processing input and generating the expected output
- Integration hooks for the listed tools

Make sure the code is clean, well-documented, and ready to deploy.
"""
)
