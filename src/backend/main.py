import subprocess
import os
import sys
import time
import atexit
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from src.frontend.chat_window import ChatWindow

ollama_process = None

def check_and_install_ollama():
    try:
        # Check if Ollama is installed
        subprocess.run(["ollama", "--version"], check=True)
    except FileNotFoundError:
        print("Ollama is not installed. Installing Ollama...")

        installer_path = "ollama-installer.exe"
        
        if not os.path.exists(installer_path):
            print("Downloading Ollama installer...")
            installer_url = "https://ollama.com/download/OllamaSetup.exe"
            try:
                # Download the Ollama installer
                response = urllib.request.urlopen(installer_url)
                with open(installer_path, "wb") as file:
                    file.write(response.read())
            except urllib.error.URLError as e:
                print(f"Failed to download Ollama installer: {e.reason}")
                return
            except Exception as e:
                print(f"Unexpected error: {e}")
                return

        try:
            # Run the installer silently
            print("Running the Ollama installer...")
            subprocess.run([installer_path, "/S"])

            # Add Ollama to PATH
            ollama_path = "C:\\Program Files\\Ollama\\bin"
            os.environ["PATH"] += os.pathsep + ollama_path

            # Ensure Ollama is not running automatically after installation
            stop_ollama_server()

        except subprocess.CalledProcessError as e:
            print(f"Failed to install Ollama: {e}")

def start_ollama_server():
    global ollama_process
    try:
        # Start Ollama server
        ollama_process = subprocess.Popen(["ollama", "serve"])
        time.sleep(5)  # Wait for the server to start
    except Exception as e:
        print(f"Failed to start Ollama server: {e}")

def stop_ollama_server():
    global ollama_process

    # Stop the subprocess if it was started by this script
    if ollama_process:
        ollama_process.terminate()
        ollama_process.wait()
        print("Ollama server stopped.")
    
    # Kill any other running ollama processes using taskkill
    try:
        subprocess.run(["taskkill", "/f", "/im", "Ollama.exe"], check=True)
        print("Terminated any running Ollama processes.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to terminate Ollama process: {e}")

def main():
    check_and_install_ollama()
    stop_ollama_server()
    start_ollama_server()
    atexit.register(stop_ollama_server)
    chat_window = ChatWindow()
    chat_window.show_chat_page()
    chat_window.root.mainloop()

if __name__ == "__main__":
    main()
