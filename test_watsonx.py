# test_watsonx.py

import os
import logging
import asyncio
from dotenv import load_dotenv
from beeai_framework.backend.chat import ChatModel, ChatModelInput
from beeai_framework.backend.message import UserMessage

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Load WatsonX configuration from .env
PROJECT_ID = os.getenv("PROJECT_ID", "")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY", "")
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
# Use the dedicated WatsonX model name variable
MODEL_NAME = os.getenv("BEEAI_WATSONX_MODEL_NAME", "watsonx:granite-13b-instruct-v2")

logger.info(f"Testing WatsonX connection using model: {MODEL_NAME} and base URL: {WATSONX_URL}")
print(f"Loaded WatsonX URL from .env: {WATSONX_URL}")

# Initialize the ChatModel for WatsonX
chat_model = ChatModel.from_name(MODEL_NAME)

async def test_connection():
    # Create a simple message to test the connection/inference
    message = UserMessage(content="Hello, test WatsonX connection.")
    try:
        # Pass the proper base URL via settings (WatsonX endpoint)
        output = await chat_model.create(
            ChatModelInput(messages=[message], settings={"base_url": WATSONX_URL})
        )
        logger.info("WatsonX connection successful.")
        print("Output:", output.get_text_content())
    except Exception as e:
        logger.error("Error testing WatsonX connection", exc_info=True)
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(test_connection())
