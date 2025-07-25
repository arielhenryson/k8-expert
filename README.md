# k8-expert

<p align="center">
<strong>🤖 Your AI-powered assistant for Kubernetes 🤖</strong>
</p>

<p align="center">
k8-expert is a smart agent that helps you investigate, manage, and resolve issues in your Kubernetes clusters using natural language.
</p>

<p align="center">
<img src="public/demo.png" alt="Demo" width="700"/>
</p>

## 🌟 What is k8-expert?

k8-expert simplifies Kubernetes cluster management by providing a conversational interface to `kubectl`. Instead of memorizing complex commands, you can simply ask the agent what you want to know or do. It's designed for both beginners who are learning Kubernetes and experienced engineers who want to streamline their workflow.

The agent leverages a powerful large language model to understand your requests, execute the appropriate `kubectl` commands securely, and interpret the output for you.

## ✨ Features

* **Natural Language Interface:** Interact with your cluster by asking questions in plain English.

* **Secure Command Execution:** Runs `kubectl` commands in a sandboxed environment to prevent unintended changes.

* **Resource Inspection:** Easily get the status, logs, and descriptions of pods, deployments, services, and other K8s resources.

* **Error Investigation:** Helps diagnose common issues like `CrashLoopBackOff`, `ImagePullBackOff`, and pending pods.

* **Streamlined Workflow:** Reduces the time spent looking up `kubectl` syntax and flags.

## ⚙️ How It Works

The system is built around a central **Agent** powered by Google's Gemini model.

1. **User Prompt:** You provide a prompt in natural language (e.g., "Are all my pods in the default namespace running?").

2. **Agent Interpretation:** The agent analyzes your request and determines which `kubectl` command is needed to answer it.

3. **Tool Execution:** The agent uses the `run_kubectl_command` tool to safely execute the command against your currently configured Kubernetes cluster.

4. **Result Analysis:** The agent receives the output from `kubectl`, analyzes it, and formulates a clear, human-readable response.

5. **Answer:** The final answer is presented to you, often with summaries, explanations, or suggestions for next steps.

## 🚀 Getting Started

### Prerequisites

* **Conda

* **kubectl:** You must have `kubectl` installed and configured to point to a Kubernetes cluster. You can test your connection by running `kubectl get nodes`.

### Installation & Setup

1. **Create and activate the conda environment:**
   ```bash
   conda create -n k8-expert python=3.12 -y
   conda activate k8-expert
   ```

2. Install dependencies
   ```bash
   pip install .
   ```

3. Set up your environment variables
   ```bash
   cp k8_expert_agent/.env.example k8_expert_agent/.env
   ```

4. Run the Agent
   ```bash
   adk web
   ```