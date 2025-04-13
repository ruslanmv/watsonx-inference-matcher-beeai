#!/bin/bash
# test_watsonx.sh
# This script tests the WatsonX connection by running test_watsonx.py

echo "Running WatsonX connection test..."
python test_watsonx.py
if [ $? -eq 0 ]; then
    echo "WatsonX connection test passed."
else
    echo "WatsonX connection test failed."
fi