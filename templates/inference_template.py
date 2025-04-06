from pydantic import BaseModel
from beeai_framework.utils.templates import PromptTemplate

class InferenceTemplateInput(BaseModel):
    document_content: str
    parameter1: str
    parameter2: int

# This template generates an inference based on a user document and input parameters.
# It uses Mustache-style syntax for variable placeholders.

inference_prompt_template: PromptTemplate = PromptTemplate(
    schema=InferenceTemplateInput,
    template="""
You are a configuration assistant. Based on the following document, generate a well-formed configuration or inference.

Document:
{{document_content}}

Context Parameters:
- Parameter1: {{parameter1}}
- Parameter2: {{parameter2}}

Instructions:
Please infer the most relevant configuration or structure based on the above inputs. Output must be concise and directly actionable.
"""
)
