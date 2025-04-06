import streamlit as st
import subprocess
import pandas as pd
from src.debugger.utils import get_chatbot_suggestion
import base64

st.set_page_config(page_title="🛠 Auto Error Debugger with WatsonX", layout="wide")
st.title("🧠 Auto Error Debugger Assistant with WatsonX")
st.markdown("This assistant will analyze Python code and fix errors automatically using IBM WatsonX LLMs.")

code_input = st.text_area("Paste your Python code here:", height=300)
max_attempts = st.slider("Maximum Fix Attempts", 1, 10, 3)
run_option = st.radio("Run Code Locally Before Debugging?", ("Yes", "No"))
fixed_code_area = st.empty()
output_area = st.empty()
log_data = []

def run_code(code):
    result = subprocess.run(["python", "-c", code], capture_output=True, text=True)
    if result.returncode == 0:
        return True, result.stdout
    else:
        return False, result.stderr

if st.button("🔁 Debug and Run"):
    code = code_input
    attempt = 1
    success = False
    error = ""

    if run_option == "Yes":
        while not success and attempt <= max_attempts:
            output_area.info(f"Attempt {attempt}: Executing code...")
            success, output = run_code(code)

            if success:
                output_area.success("✅ Code executed successfully.")
                output_area.code(output)
                fixed_code_area.markdown("### ✅ Final Suggested Code")
                st.code(code, language='python')
                log_data.append([attempt, code_input, code, error, success])
                break
            else:
                error = output
                st.warning(f"⚠️ Error encountered:")
                st.code(error)
                suggestion = get_chatbot_suggestion(error, code)
                code = suggestion
                attempt += 1

        if not success:
            output_area.error("❌ Max attempts reached. Code still has errors.")

    else:
        error = ""
        suggestion = get_chatbot_suggestion(error, code)
        code = suggestion
        output_area.info("⚠️ Code not executed. Showing static suggestion:")
        fixed_code_area.markdown("### 🤖 Suggested Fix")
        st.code(code, language='python')
        log_data.append([attempt, code_input, code, error, "Skipped"])

    if log_data:
        st.markdown("---")
        st.markdown("### 📋 Debug Log")
        log_df = pd.DataFrame(log_data, columns=["Attempt", "Original Code", "Suggested Code", "Error", "Success"])
        st.dataframe(log_df)

        csv = log_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="debug_log.csv">Download Debug Log CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
