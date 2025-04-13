import os
import json
import logging
import asyncio
from pydantic import BaseModel
from typing import List, Optional, Union
from dotenv import load_dotenv
from beeai_framework.workflows.workflow import Workflow, WorkflowReservedStepName
from beeai_framework.backend.chat import ChatModel, ChatModelInput
from beeai_framework.backend.message import UserMessage
from src.templates.inference_template import inference_prompt_template, InferenceTemplateInput
from src.evaluation.evaluation_utils import calculate_similarity

# Setup Logging with detailed format
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Load WatsonX configuration
WATSONX_PROJECT_ID = os.getenv("PROJECT_ID", "")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY", "")
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
WATSONX_MODEL = os.getenv("WATSONX_MODEL", "")

# Load Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Determine provider/model to use from environment variable
# Default to "ollama:granite3.2" if not set.
MODEL_NAME = os.getenv("BEEAI_MODEL_NAME", "ollama:granite3.2")
logger.info(f"Using inference model: {MODEL_NAME}")

# Determine the appropriate base URL based on provider:
if MODEL_NAME.startswith("watsonx:"):
    BASE_URL = WATSONX_URL
else:
    BASE_URL = OLLAMA_BASE_URL

chat_model: ChatModel = ChatModel.from_name(MODEL_NAME)

class InferenceMatcherState(BaseModel):
    document_template: str
    target_output: dict
    current_inference: Optional[str] = None
    current_score: Optional[float] = None
    best_inference: Optional[str] = None
    best_score: Optional[float] = None
    iteration_count: int = 0
    max_iterations: int = 10
    search_parameters: List[str] = []
    current_parameter_index: int = 0

async def generate_inference(state: InferenceMatcherState) -> str:
    """
    Generate an inference using the provided prompt.
    If an exception occurs during chat_model.create(), catch it and return a termination step.
    """
    param = state.search_parameters[state.current_parameter_index]
    logger.info(f"[Step: Generate] Using Parameters: {param}")

    input_data = InferenceTemplateInput(
        document_content=state.document_template,
        parameter1=param,
        parameter2=state.iteration_count
    )

    rendered_prompt = inference_prompt_template.render(input_data)
    logger.debug(f"[Rendered Prompt]:\n{rendered_prompt}")

    message = UserMessage(content=rendered_prompt)
    try:
        # Pass the proper base URL via settings
        output = await chat_model.create(
            ChatModelInput(messages=[message], settings={"base_url": BASE_URL})
        )
    except Exception as e:
        logger.error("Error during model inference", exc_info=True)
        # Return a termination step rather than propagating the error further
        return "terminate_workflow_error"
        
    state.current_inference = output.get_text_content()
    logger.info(f"[Generated Inference]:\n{state.current_inference}\n")
    return "evaluate_inference"

async def evaluate_inference(state: InferenceMatcherState) -> str:
    logger.info("[Step: Evaluate] Calculating similarity score")
    score = calculate_similarity(state.current_inference, state.target_output)
    state.current_score = score
    logger.info(f"[Evaluation Score]: {score}")
    return "compare_and_store"

async def compare_and_store(state: InferenceMatcherState) -> str:
    logger.info("[Step: Compare & Store] Comparing with best score")
    if state.best_score is None or state.current_score > state.best_score:
        state.best_score = state.current_score
        state.best_inference = state.current_inference
        logger.info(f"[Best Inference Updated] Score: {state.best_score}")
    return "check_termination"

async def check_termination(state: InferenceMatcherState) -> Union[str, WorkflowReservedStepName]:
    logger.info("[Step: Termination Check] Evaluating end condition")
    state.iteration_count += 1
    state.current_parameter_index += 1

    if (state.iteration_count >= state.max_iterations or
        state.current_parameter_index >= len(state.search_parameters)):
        logger.info("[Terminating Workflow] Maximum iterations or parameters exhausted")
        return "output_best_inference"
    else:
        logger.info("[Continuing Workflow] Proceeding to next iteration")
        return Workflow.SELF

async def output_best_inference(state: InferenceMatcherState) -> WorkflowReservedStepName:
    logger.info("[Step: Output] Displaying final best inference")
    print("\n✅ Final Best Inference:")
    print(state.best_inference)
    print(f"Score: {state.best_score}")
    return Workflow.END

async def terminate_workflow_error(state: InferenceMatcherState) -> WorkflowReservedStepName:
    logger.error("Terminating workflow due to inference error.")
    print("\n❌ Workflow terminated due to inference error.")
    return Workflow.END

# Instantiate Workflow and add steps
inference_workflow = Workflow(schema=InferenceMatcherState)
inference_workflow.add_step("generate_inference", generate_inference)
inference_workflow.add_step("evaluate_inference", evaluate_inference)
inference_workflow.add_step("compare_and_store", compare_and_store)
inference_workflow.add_step("check_termination", check_termination)
inference_workflow.add_step("output_best_inference", output_best_inference)
inference_workflow.add_step("terminate_workflow_error", terminate_workflow_error)

# Optional entry point to run standalone
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()

    async def main():
        logger.info("[MAIN] Running InferenceMatcher Workflow example")
        template = open("src/examples/sample_document.txt").read()
        targets = json.load(open("src/config/targets.json"))

        # Example search parameters for demonstration.
        state = InferenceMatcherState(
            document_template=template,
            target_output=targets,
            search_parameters=[
                "use_embedding=True, model=watsonx:granite-13b-instruct-v2",
                "use_embedding=False, model=watsonx:codellama",
                "retriever_method=cosine"
            ],
            max_iterations=3
        )
        result = await inference_workflow.run(state)
        print("\n✅ Best Result:", result.state.best_inference)

    asyncio.run(main())
    logger.info("[MAIN] Workflow execution completed")
