# Email Triage Agent

Project aims to explore **LangGraph** and **Python** by building an email analyzer that can extract critical information and make a decision based on the information obtained, whether it be an escalation or a follow up email to the user. I'm hoping to eventually apply these learnings for other applications like a deck analyzer agent or a more efficient way to be notified about important emails and notifications. Another application is to help businesses with inquiries they receive via email for their inventory. Being able to parse through their inventory list and extract key information from a quote can help save their sales teams time and also help flag emails based on a specific criteria (e.g. price threshold, # of orders)

## Setup

This project runs its LLM calls against a local **Ollama** model, so you'll need Ollama installed and running in addition to the Python environment.

1. **Install and start Ollama**, then pull the model used by the chains:
   ```
   ollama pull llama3.1
   ```
   Ollama needs to be running in the background (the desktop app or `ollama serve`) before you run the app.

2. **Create a virtual environment and install dependencies:**
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```
   python main.py
   ```
   This parses `EMAILS[0]` from `email_demo/example_emails.py` and prints the extracted notice details plus whether escalation is required.
