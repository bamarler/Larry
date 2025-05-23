import subprocess
import time
import atexit
import urllib.request
import psutil
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from src.frontend.gui import GUI
from src.backend.system_manager import SystemManager
from src.backend.chat_manager import ChatManager
from src.backend.model_manager import ModelManager
from src.backend.settings_manager import SettingsManager

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

def set_ollama_models_directory():
    # Ensure Model Folder Exists
    model_folder = "ollama-models"
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)
    
    # Set OLLAMA_MODELS environment variable to the app directory
    app_directory = os.path.realpath(model_folder)
    os.environ["OLLAMA_MODELS"] = app_directory
    print(f"OLLAMA_MODELS set to {app_directory}")

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
    
def stop_ollama_app():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Check if the process name contains "ollama" (case insensitive)
            if 'ollama' in proc.info['name'].lower():
                print(f"Terminating process {proc.info['name']} with PID {proc.info['pid']}")
                proc.terminate()  # Graceful termination
                proc.wait(timeout=3)  # Wait for the process to terminate
                print(f"Process {proc.info['pid']} terminated successfully.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print(f"Could not terminate process {proc.info['pid']}: {e}")

def main():
    set_ollama_models_directory()
    check_and_install_ollama()
    stop_ollama_app()
    start_ollama_server()
    atexit.register(stop_ollama_server)
    SystemManager()
    ChatManager()
    ModelManager()
    SettingsManager()
    gui = GUI()
    gui.root.mainloop()

if __name__ == "__main__":
    main()
