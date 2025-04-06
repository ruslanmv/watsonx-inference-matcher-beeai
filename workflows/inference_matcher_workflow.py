from pydantic import BaseModel
from typing import List, Optional, Union
from beeai_framework.workflows.workflow import Workflow, WorkflowReservedStepName
from beeai_framework.backend.chat import ChatModel, ChatModelInput
from beeai_framework.backend.message import UserMessage
from src.templates.inference_template import inference_prompt_template, InferenceTemplateInput
from src.evaluation.evaluation_utils import calculate_similarity
import json

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


# Load the model from Ollama or WatsonX
chat_model: ChatModel = ChatModel.from_name("ollama:llama3.1")


async def generate_inference(state: InferenceMatcherState) -> str:
    param = state.search_parameters[state.current_parameter_index]

    input_data = InferenceTemplateInput(
        document_content=state.document_template,
        parameter1=param,
        parameter2=state.iteration_count
    )

    rendered_prompt = inference_prompt_template.render(input_data)
    message = UserMessage(content=rendered_prompt)
    output = await chat_model.create(ChatModelInput(messages=[message]))
    state.current_inference = output.get_text_content()

    print(f"\n[Generated Inference]:\n{state.current_inference}\n")
    return "evaluate_inference"


async def evaluate_inference(state: InferenceMatcherState) -> str:
    score = calculate_similarity(state.current_inference, state.target_output)
    state.current_score = score

    print(f"[Evaluation Score]: {score}")
    return "compare_and_store"


async def compare_and_store(state: InferenceMatcherState) -> str:
    if state.best_score is None or state.current_score > state.best_score:
        state.best_score = state.current_score
        state.best_inference = state.current_inference
        print(f"[Best Inference Updated] Score: {state.best_score}")
    return "check_termination"


async def check_termination(state: InferenceMatcherState) -> Union[str, WorkflowReservedStepName]:
    state.iteration_count += 1
    state.current_parameter_index += 1

    if (state.iteration_count >= state.max_iterations or
        state.current_parameter_index >= len(state.search_parameters)):
        return "output_best_inference"
    else:
        return Workflow.SELF


async def output_best_inference(state: InferenceMatcherState) -> WorkflowReservedStepName:
    print("\n✅ Final Best Inference:")
    print(state.best_inference)
    print(f"Score: {state.best_score}")
    return Workflow.END


# Instantiate Workflow
inference_workflow = Workflow(schema=InferenceMatcherState)
inference_workflow.add_step("generate_inference", generate_inference)
inference_workflow.add_step("evaluate_inference", evaluate_inference)
inference_workflow.add_step("compare_and_store", compare_and_store)
inference_workflow.add_step("check_termination", check_termination)
inference_workflow.add_step("output_best_inference", output_best_inference)


# Optional entry point to run standalone
if __name__ == "__main__":
    import asyncio

    async def main():
        # Load example input and config
        template = open("src/examples/sample_document.txt").read()
        targets = json.load(open("src/config/targets.json"))

        state = InferenceMatcherState(
            document_template=template,
            target_output=targets,
            search_parameters=["version=1", "version=2", "version=3"],
            max_iterations=3
        )

        result = await inference_workflow.run(state)
        print("\n✅ Best Result:", result.state.best_inference)

    asyncio.run(main())
