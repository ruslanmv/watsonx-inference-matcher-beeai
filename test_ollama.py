# test_ollama.py
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

# Print the loaded OLLAMA_BASE_URL from .env
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
print(f"Loaded OLLAMA_BASE_URL from .env: {OLLAMA_BASE_URL}")

# For testing, we force use the Ollama provider model:
MODEL_NAME = "ollama:granite3.2"
logger.info(f"Testing Ollama connection using model: {MODEL_NAME} and base URL: {OLLAMA_BASE_URL}")

# Initialize the ChatModel (assuming LiteLLM handles the rest)
chat_model = ChatModel.from_name(MODEL_NAME)

async def test_connection():
    # Create a simple message to test
    message = UserMessage(content="Hello, test Ollama connection.")
    try:
        output = await chat_model.create(
            ChatModelInput(messages=[message], settings={"base_url": OLLAMA_BASE_URL})
        )
        logger.info("Ollama connection successful.")
        print("Output:", output.get_text_content())
    except Exception as e:
        logger.error("Error testing Ollama connection", exc_info=True)

if __name__ == "__main__":
    asyncio.run(test_connection())
