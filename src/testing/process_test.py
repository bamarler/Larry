import psutil
import subprocess

# Function to list all running processes
def list_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            print(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Function to terminate a process by PID
def terminate_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()  # or process.kill() for a forceful kill
        process.wait(timeout=3)  # Wait for the process to terminate
        print(f"Process {pid} terminated successfully.")
    except psutil.NoSuchProcess:
        print(f"No such process with PID {pid}.")
    except psutil.AccessDenied:
        print(f"Access denied to terminate process with PID {pid}.")
    except psutil.TimeoutExpired:
        print(f"Process {pid} termination timed out.")

# Example usage
if __name__ == "__main__":
    print("Listing all running processes:")
    list_processes()

    pid_to_terminate = int(input("Enter the PID of the process to terminate: "))
    terminate_process(pid_to_terminate)
