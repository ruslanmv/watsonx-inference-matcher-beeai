import os
import logging
import requests
from dotenv import load_dotenv
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes

# Load environment variables
load_dotenv()

# IBM WatsonX credentials
API_KEY = os.getenv("API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"

# Get bearer token

def get_bearer_token(apikey):
    form = {
        "apikey": apikey,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }
    response = requests.post("https://iam.cloud.ibm.com/oidc/token", data=form)
    if response.status_code != 200:
        raise Exception("Failed to get bearer token")
    return response.json().get("access_token")

# Bearer token required for model initialization
credentials = {
    "apikey": API_KEY,
    "url": WATSONX_URL,
    "token": get_bearer_token(API_KEY)
}

# Model parameters
parameters = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 1000,
    GenParams.STOP_SEQUENCES: ["\n\n\n"]
}

# Load LLAMA model from WatsonX
model_id = ModelTypes.LLAMA_2_70B_CHAT

llm_model = Model(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=PROJECT_ID
)

# Generates corrected code from the error + original code

def generate_code(code: str, language: str, message_error: str) -> str:
    instruction = f"""You are given a code snippet in {language} that contains syntax errors and logical issues. 
Fix the code and return only the corrected version. Do not provide explanations or additional information."""

    if message_error:
        prompt = f"""<s>[INST] <<SYS>>
{instruction}
<</SYS>>
The following is the code to fix:
{code}
The error is: {message_error}
[/INST]"""
    else:
        prompt = f"""<s>[INST] <<SYS>>
{instruction}
<</SYS>>
Fix the following code:
{code}
[/INST]"""

    result = llm_model.generate([prompt])
    generated = result[0]['results'][0]['generated_text']
    return generated.strip()

# Entry point used by debugger_app.py

def get_chatbot_suggestion(error: str, code: str) -> str:
    return generate_code(code=code, language="Python", message_error=error)
