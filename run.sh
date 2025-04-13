#!/bin/bash
# run_test.sh
# This script runs the Inference Matcher Workflow test.

# Ensure the current directory is the project root
echo "Running Inference Matcher Workflow test..."

# Option 1: Run using the module approach
python -m src.workflows.inference_matcher_workflow

# Option 2: Alternatively, if you prefer to run the script directly, uncomment below:
# export PYTHONPATH=$(pwd)
# python src/workflows/inference_matcher_workflow.py
