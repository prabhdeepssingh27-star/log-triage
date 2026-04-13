# Security Log Triage Copilot

An AI-powered security tool that analyzes SSH logs, detects attack patterns, and generates professional incident reports.

## What It Does

- Detects **brute force attacks** (same IP, multiple failed logins)
- Detects **password spraying** (same IP, multiple usernames)
- Extracts evidence log lines for each finding
- Generates an **AI-powered analyst report** using a local LLM
- Clean web interface for uploading logs and downloading reports

## Tech Stack

- Python
- Streamlit
- Ollama (llama3.2)

## How To Run

1. Install dependencies:
2. Install and start Ollama:
3. Run the app:
4. Upload a `.txt` or `.log` SSH log file and get your report.

## Detection Rules

| Attack Type | Logic |
|---|---|
| Brute Force | Same IP with 5+ failed login attempts |
| Password Spraying | Same IP attempting 3+ different usernames |

## Sample Output

Upload a log file and the tool will detect threats, generate an AI summary, and allow you to download a markdown report.

