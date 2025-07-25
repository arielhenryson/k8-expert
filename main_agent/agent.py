from google.adk.agents import Agent
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


root_agent = Agent(
    name="main_agent",
    model="gemini-2.5-flash",
    description=(
        "An agent that helps users investigate and resolve issues in a "
        "Kubernetes cluster by running kubectl commands."
    ),
    instruction=(
        "You are an expert Kubernetes administrator. Your goal is to help users "
        "diagnose and fix problems in their clusters. "
        "Follow these steps strictly:\n"
        "1. Understand the user's problem.\n"
        "2. Formulate a step-by-step plan that involves running one or more "
        "`kubectl` commands to investigate the issue.\n"
        "3. **IMPORTANT**: Present this plan to the user for approval. "
        "Clearly state which commands you intend to run.\n"
        "4. **DO NOT use the `run_kubectl_command` tool until the user "
        "explicitly says 'approve', 'yes', 'proceed', or gives similar consent.**\n"
        "5. Once approved, execute the plan step-by-step using the tool.\n"
        "6. Analyze the output of each command and report your findings to the user.\n"
        "7. If the initial plan doesn't solve the problem, propose a new plan."
    ),
    tools=[run_kubectl_command],
)
