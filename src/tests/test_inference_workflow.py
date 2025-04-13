import pytest
from src.workflows.inference_matcher_workflow import inference_workflow, InferenceMatcherState
import json
import asyncio

@pytest.mark.asyncio
async def test_basic_workflow():
    # Sample document
    document = """Generate a Python class for a web server that supports TLS 1.2 and handles 1000 requests/sec."""

    # Target criteria
    target = {
        "target_description": "The generated inference should represent a valid configuration for a web server.",
        "criteria": {
            "max_latency": "50ms",
            "throughput": "1000 requests/second",
            "security_protocols": ["TLS 1.2", "OAuth2"]
        }
    }

    # Search parameters
    params = ["version=1.0", "version=2.0"]

    # Initialize state
    state = InferenceMatcherState(
        document_template=document,
        target_output=target,
        search_parameters=params,
        max_iterations=2
    )

    # Run the workflow
    result = await inference_workflow.run(state)

    # Assertions
    assert result.state.best_inference is not None
    assert isinstance(result.state.best_score, float)
    assert result.state.best_score >= 0.0 and result.state.best_score <= 1.0
