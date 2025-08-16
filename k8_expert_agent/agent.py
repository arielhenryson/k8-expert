from google.adk.agents import Agent
from jinja2 import Environment, FileSystemLoader
import os
import subprocess

def run_kubectl_command(command: str) -> dict:
    """
    Executes a kubectl command and returns the output or error.

    Args:
        command (str): The kubectl command to execute (e.g., "get pods --namespace default").
                       The 'kubectl' part is assumed and should not be included.

    Returns:
        dict: A dictionary with 'status' and either 'result' on success
              or 'error_message' on failure.
    """
    if not isinstance(command, str):
        return {
            "status": "error",
            "error_message": "Command must be a string."
        }

    # Security Best Practice: Split the command string into a list to avoid shell injection.
    # The command should not include "kubectl" as we are adding it here.
    full_command = ["kubectl"] + command.split()

    try:
        # Execute the command
        print(f"Executing command: {' '.join(full_command)}")
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,  # Capture output as a string
            check=True,  # Raise an exception for non-zero exit codes
            timeout=60  # Add a timeout for safety
        )

        # Return the standard output
        return {
            "status": "success",
            "result": result.stdout
        }

    except FileNotFoundError:
        # This error occurs if 'kubectl' is not installed or not in the system's PATH
        return {
            "status": "error",
            "error_message": "Error: 'kubectl' command not found. Please ensure it is installed and in your PATH."
        }
    except subprocess.CalledProcessError as e:
        # This error occurs if the command returns a non-zero exit code (i.e., an error)
        return {
            "status": "error",
            "error_message": f"Command failed with error:\n{e.stderr}"
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "error_message": "Command timed out after 60 seconds."
        }
    except Exception as e:
        # Catch any other unexpected errors
        return {
            "status": "error",
            "error_message": f"An unexpected error occurred: {str(e)}"
        }

script_dir = os.path.dirname(os.path.abspath(__file__))
template_folder_path = os.path.join(script_dir, "prompts")
env = Environment(loader=FileSystemLoader(template_folder_path))

template = env.get_template("main_instruction.jinja")
instruction = template.render()

root_agent = Agent(
    name="root_agent",
    model="gemini-live-2.5-flash-preview",
    description=(
        "An agent that helps users investigate and resolve issues in a "
        "Kubernetes cluster by running kubectl commands."
    ),
    instruction=instruction,
    tools=[run_kubectl_command],
)