# k8-expert

Your AI-powered SRE for Kubernetes

## Setup

1. **Create and activate the conda environment:**
   ```bash
   conda create -n k8-expert python=3.12 -y
   conda activate k8-expert
   ```

2. Install dependencies
   ```bash
   pip install .
   ```

3. Create a `.env` file and add your `GOOGLE_API_KEY`:
   ```bash
   touch .env
   echo "GOOGLE_API_KEY=YOUR_API_KEY" > .env
   ```
   Replace `YOUR_API_KEY` with your actual Google API key.

4. Run the application
   ```bash
   chainlit run app.py
   ```