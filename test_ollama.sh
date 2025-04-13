#!/bin/bash
# test_ollama.sh
# This script gets the current host IP from the default route,
# extracts the IP from the OLLAMA_BASE_URL in the .env file,
# compares them, and warns if they differ.

# Get current host IP from ip route (assuming the route contains "src <IP>")
CURRENT_IP=$(ip route | grep -oP 'src \K\S+')
echo "Current host IP: $CURRENT_IP"

# Extract the OLLAMA_BASE_URL from the .env file and parse out the IP address.
# Assumes the URL is in the format: http://<IP>:11434
if [ -f .env ]; then
    ENV_URL=$(grep "^OLLAMA_BASE_URL=" .env | cut -d '=' -f2)
    # Remove the protocol (http://) and port (:11434)
    ENV_IP=$(echo "$ENV_URL" | sed -e 's|http://||' -e 's|:11434||')
    echo "OLLAMA_BASE_URL IP in .env: $ENV_IP"
else
    echo "Warning: .env file not found. Using default URL."
    ENV_IP="localhost"
fi

# Compare the two IP addresses
if [ "$CURRENT_IP" != "$ENV_IP" ]; then
    echo "WARNING: The current host IP ($CURRENT_IP) does not match the OLLAMA_BASE_URL IP in .env ($ENV_IP)."
    echo "Using the URL defined in .env: $ENV_URL"
else
    echo "The current host IP matches the OLLAMA_BASE_URL IP in .env."
fi

# Run the python test script
python3 test_ollama.py
