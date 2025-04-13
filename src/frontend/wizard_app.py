import streamlit as st
import json
import asyncio
from src.workflows.inference_matcher_workflow import inference_workflow, InferenceMatcherState

st.set_page_config(page_title="Agent Generator Wizard", layout="wide")
st.title("🧠 Agent Generator Wizard")
st.markdown("Fill in the fields below to generate your custom agent based on your needs.")

# Sidebar inputs
document_content = st.text_area("📄 Document Template", height=200, placeholder="Paste infrastructure or agent template text here...")

# Dynamic parameter input as list
param_count = st.slider("🔧 Number of parameter sets", 1, 10, 3)
parameters = []
for i in range(param_count):
    parameters.append(st.text_input(f"Parameter Set {i+1}", value=f"version={i+1}"))

# Target JSON input
st.markdown("### 🎯 Target Output Configuration")
target_json = st.text_area("Paste target output JSON:", value='''{
  "target_description": "The generated inference should represent a valid configuration for a web server.",
  "criteria": {
    "max_latency": "50ms",
    "throughput": "1000 requests/second",
    "security_protocols": ["TLS 1.2", "OAuth2"]
  }
}''', height=150)

# Max iterations
max_iterations = st.slider("🔁 Max Iterations", min_value=1, max_value=20, value=5)

# Run button
if st.button("🚀 Generate Agent"):
    if not document_content or not parameters:
        st.warning("Please fill in the document template and parameters.")
    else:
        with st.spinner("Running Inference Matcher Workflow..."):
            try:
                parsed_target = json.loads(target_json)
                state = InferenceMatcherState(
                    document_template=document_content,
                    target_output=parsed_target,
                    search_parameters=parameters,
                    max_iterations=max_iterations
                )
                result = asyncio.run(inference_workflow.run(state))
                st.success("✅ Agent generation completed!")
                st.markdown("### 🏁 Best Matching Inference")
                st.code(result.state.best_inference, language="python")
                st.markdown(f"**Score:** {result.state.best_score}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
