# Multi-Agent-Resume-Genie
A multi-agent tool designed to help users analyze job postings, enhance resumes, and prepare for interviews using AI-driven insights.

## Setup

### 1. Installaton
For stability, this project is developed and tested with **Python 3.9.6**.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2.Environment Variables
Create a .env file and add the following variables.
```bash
JOB_POSTING_PATH=/path/to/your/job_posting.txt
RESUME_PATH=/path/to/your/resume.txt
```
Execute `metagpt --init-config` to generate `~/.metagpt/config2.yaml`. Edit this file with your configurations.
```bash
llm:
  api_type: 'openai' # or azure / ollama / groq etc. Check LLMType for more options
  model: 'gpt-4o-mini' # or gpt-3.5-turbo
  base_url: 'https://api.openai.com/v1' # or forward url / other llm url
  api_key: 'YOUR_API_KEY'
```

### 3. Execution
```bash
python main.py
python main.py --log=DEBUG # run with logs
```