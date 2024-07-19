# script to check that ollama is installed and running properly

import subprocess
import sys
import os
import platform

def check_ollama_installed():
    try:
        subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_ollama_unix():
    install_command = """
    curl -fsSL https://example.com/install-ollama.sh | sh
    """
    try:
        subprocess.run(install_command, shell=True, check=True)
        print("Ollama installed successfully on Unix-based system.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Ollama on Unix-based system: {e}")
        sys.exit(1)

def install_ollama_windows():
    install_command = """
    powershell -Command "Invoke-WebRequest -Uri 'https://example.com/install-ollama.ps1' -OutFile 'install-ollama.ps1'; ./install-ollama.ps1"
    """
    try:
        subprocess.run(install_command, shell=True, check=True)
        print("Ollama installed successfully on Windows.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Ollama on Windows: {e}")
        sys.exit(1)

def start_ollama_server():
    try:
        subprocess.run("ollama serve", check=True)
        print("Ollama server started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Ollama server: {e}")
        sys.exit(1)

def main():
    if not check_ollama_installed():
        print("Ollama is not installed. Installing Ollama...")
        if platform.system() == "Windows":
            install_ollama_windows()
        else:
            install_ollama_unix()
    else:
        print("Ollama is already installed.")
    
    start_ollama_server()

    # Your main script logic here
    print("Running main script...")

if __name__ == "__main__":
    main()
