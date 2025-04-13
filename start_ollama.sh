#!/bin/bash

# Friendly messages
FRIENDLY_MESSAGE="WatsonX Inference Matcher - Ollama Serving"
INSTALL_MESSAGE="Installing Ollama..."
STOP_MESSAGE="Stopping Ollama systemd service..."
START_MESSAGE="Starting Ollama server (ollama serve)..."
DONT_CLOSE_MESSAGE="Don't close this terminal; the Ollama server is running."

# Function to check if Ollama is installed
check_ollama_installed() {
  if command -v ollama &> /dev/null; then
    return 0  # Ollama is installed
  else
    return 1  # Ollama is not installed
  fi
}

# Function to install Ollama
install_ollama() {
  echo "$FRIENDLY_MESSAGE"
  echo "$INSTALL_MESSAGE"
  curl -fsSL https://ollama.com/install.sh | sh
  if check_ollama_installed; then
    echo "Ollama installation successful."
  else
    echo "Ollama installation failed."
    exit 1
  fi
}

# Function to stop and start Ollama service
stop_and_start_ollama() {
  echo "$FRIENDLY_MESSAGE"
  echo "$STOP_MESSAGE"
  sudo systemctl stop ollama.service

  # Verify the service is stopped
  if sudo systemctl is-active ollama.service; then
    echo "Failed to stop Ollama service."
    exit 1
  else
    echo "Ollama service stopped."
  fi

  echo "$FRIENDLY_MESSAGE"
  echo "$START_MESSAGE"
  ollama serve
  echo "$FRIENDLY_MESSAGE"
  echo "$DONT_CLOSE_MESSAGE"
}

# Main script logic
if ! check_ollama_installed; then
  install_ollama
fi

stop_and_start_ollama