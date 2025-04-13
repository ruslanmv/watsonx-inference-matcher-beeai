
# Setup Guide

This guide explains how to set up your development environment for the Watsonx Inference Matcher project. Follow the steps below to install the required dependencies and configure the two supported LLM providers: **IBM watsonx.ai (IBM Cloud)** and **Ollama**.

---

## 1. Clone the Repository & Setup Environment

### 1.1 Clone the Repository
```bash
git clone https://github.com/ruslanmv/watsonx-inference-matcher-beeai.git
cd watsonx-inference-matcher-beeai
```

### 1.2 Create and Activate a Virtual Environment

Create a virtual environment:
```bash
python -m venv .venv
```

Activate the virtual environment:
- **macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

### 1.3 Install Dependencies
Install all required packages:
```bash
pip install -r requirements.txt
```
Make sure the following packages are installed:
- `beeai-framework`
- `streamlit`
- `pydantic`
- `python-dotenv`
- `ibm-watson-machine-learning`
- `ibm_watsonx_ai`
- (Optional) `ollama-python` for integrating with Ollama

---

## 2. IBM watsonx.ai Setup (IBM Cloud)

### 2.1 Create a `.env` File

In the project root, create a file named `.env` and add your IBM watsonx.ai credentials:
```
API_KEY=your_watsonx_api_key
PROJECT_ID=your_project_id
URL=https://us-south.ml.cloud.ibm.com
```
*Replace the URL with your region-specific endpoint if needed (e.g., Frankfurt, London, Sydney, Tokyo, or Toronto).*

### 2.2 Initialize the watsonx.ai Client

Use the new IBM watsonx.ai Python SDK (v1.0) to create an authenticated client. For example:
```python
from ibm_watsonx_ai import APIClient, Credentials

credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com",  # Replace with your region-specific URL
    api_key="your_watsonx_api_key"             # Or use token="your_token" if preferred
)

# Initialize the client with your project or space ID
client = APIClient(credentials, project_id="your_project_id")
# Alternatively, for a space-based configuration:
# client = APIClient(credentials, space_id="your_space_id")
```

### 2.3 Firewall Considerations

Ensure that your network/firewall settings allow access to the following endpoints:
- `https://us-south.ml.cloud.ibm.com`
- `https://eu-de.ml.cloud.ibm.com`
- `https://eu-gb.ml.cloud.ibm.com`
- `https://au-syd.ml.cloud.ibm.com`
- `https://jp-tok.ml.cloud.ibm.com`
- `https://ca-tor.ml.cloud.ibm.com`
- Additionally:
  - `https://api.au-syd.dai.cloud.ibm.com`
  - `https://api.ca-tor.dai.cloud.ibm.com`
  - `https://api.dataplatform.cloud.ibm.com`
  - `https://iam.cloud.ibm.com`

For more detailed instructions, refer to the official [IBM watsonx.ai documentation](https://www.ibm.com/cloud/watsonx-ai).

---

## 3. Ollama Setup

### 3.1 Installation

#### macOS
Download and install the Ollama macOS application from [ollama.com](https://ollama.com/download).

#### Windows
Download the Windows installer from [ollama.com](https://ollama.com/download).

#### Linux
Install Ollama by running:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Docker
Alternatively, pull the official Ollama Docker image:
```bash
docker pull ollama/ollama
```

### 3.2 Running a Model with Ollama

To run a model (for example, Llama 3.2), execute:
```bash
ollama run llama3.2
```

### 3.3 Using the Ollama Python Library

If you plan to integrate Ollama within your Python code, install the Ollama Python client:
```bash
pip install ollama-python
```

### 3.4 Running the Ollama Server and REST API

Start the Ollama server:
```bash
./ollama serve
```
In a separate terminal, run a model:
```bash
./ollama run llama3.2
```
You can also generate responses via the REST API:
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?"
}'
```
For additional customization (e.g., setting temperature, system messages), consult the [Ollama documentation](https://ollama.com/library).

---

## 4. Summary of Commands

| Task                            | Command                                                         |
|---------------------------------|-----------------------------------------------------------------|
| Clone repository                | `git clone https://github.com/ruslanmv/watsonx-inference-matcher-beeai.git` |
| Create virtual environment      | `python -m venv .venv`                                            |
| Activate virtual environment    | `source .venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows) |
| Install dependencies            | `pip install -r requirements.txt`                               |
| Run backend workflow            | `python -m src.workflows.inference_matcher_workflow`              |
| Launch WatsonX debugger         | `streamlit run src/debugger/debugger_app.py`                      |
| Launch Wizard UI                | `streamlit run src/frontend/wizard_app.py`                        |
| Run tests                       | `pytest src/tests/`                                              |

---

By following the steps in this guide, you will have your development environment configured to work with both IBM watsonx.ai and Ollama. Adjust configuration values in the `.env` file and client initialization code to match your credentials and deployment region.
