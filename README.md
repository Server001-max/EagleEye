# 🦅 EagleEye - Autonomous AI Pentesting Framework

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-Powered-green.svg)](https://ollama.com)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

EagleEye is an autonomous security testing framework that combines reconnaissance, AI-powered analysis, and vulnerability exploitation using local LLMs. No API keys required - everything runs locally on your machine.

## Features

- **Autonomous Reconnaissance**: Automatically enumerates subdomains using a comprehensive wordlist and scans for open ports with service detection
- **Local AI Analysis**: Uses Ollama to run LLMs locally for intelligent vulnerability assessment and attack vector identification
- **Vulnerability Detection**: Tests for common web vulnerabilities including SQL Injection and Cross-Site Scripting (XSS)
- **AI-Generated Exploits**: Automatically generates proof-of-concept exploit code for detected vulnerabilities
- **Comprehensive Reporting**: Generates detailed reports in both human-readable text format and structured JSON format
- **Fully Offline**: All processing happens locally - no data sent to external APIs
- **Multi-Threaded**: Uses concurrent processing for fast scanning performance
- **Rich Terminal Interface**: Beautiful color-coded output with progress indicators

## Requirements

- **Python 3.8 or higher**: Core programming language
- **Ollama**: Local LLM server for AI capabilities
- **Operating System**: Linux, macOS, or Windows (with WSL2 for Windows)

## Quick Start

Get EagleEye running in minutes with these commands:

```bash
# Install Ollama - the local AI server
curl -fsSL https://ollama.com/install.sh | sh

# Download the recommended AI model for security analysis
ollama pull qwen2.5:7b

# Start Ollama service in background
ollama serve

# Clone EagleEye repository
git clone https://github.com/yourusername/EagleEye.git
cd EagleEye

# Install Python dependencies
pip install -r requirements.txt

# Run your first security scan
python main.py -t https://example.com

Installation
Step 1: Install Ollama

Ollama is required for AI-powered analysis. Install it using:
bash

curl -fsSL https://ollama.com/install.sh | sh

Step 2: Download AI Model

Pull a model for security analysis. The recommended model is qwen2.5:7b:
bash

ollama pull qwen2.5:7b

Alternative models you can use:

    llama3:8b - Meta's Llama 3 model

    mistral:7b - Mistral AI model

    codellama:7b - Specialized for code generation

Step 3: Clone and Install EagleEye
bash

git clone https://github.com/yourusername/EagleEye.git
cd EagleEye
pip install -r requirements.txt

Step 4: Start Ollama Service

Ollama must be running before using EagleEye:
bash

ollama serve

Usage
Basic Usage

Scan a target with default settings:
bash

python main.py -t https://example.com

Advanced Usage

Customize your scan with various options:
bash

# Use a different AI model
python main.py -t https://example.com --model llama3

# Skip AI analysis (faster, but less intelligent)
python main.py -t https://example.com --no-ai

# Generate only JSON report
python main.py -t https://example.com --output json

# Increase thread count for faster scanning
python main.py -t https://example.com --threads 20

# Set custom timeout for requests
python main.py -t https://example.com --timeout 15

# Combine multiple options
python main.py -t https://example.com --model mistral --threads 20 --output both

Command Line Arguments
Argument	Description	Default
-t, --target	Target URL or IP address to scan	Required
--model	Ollama model to use for AI analysis	qwen2.5:7b
--no-ai	Skip the AI analysis phase	False
--output	Output format: txt, json, or both	both
--threads	Number of threads for concurrent scanning	10
--timeout	HTTP request timeout in seconds	10
Configuration

EagleEye can be configured using environment variables in a .env file:
env

# Ollama Configuration
OLLAMA_HOST=localhost          # Ollama server host
OLLAMA_PORT=11434             # Ollama server port
OLLAMA_MODEL=qwen2.5:7b       # Default AI model

# Performance Settings
MAX_THREADS=10                # Maximum concurrent threads
TIMEOUT=10                    # Request timeout in seconds

# Report Settings
REPORT_DIR=reports/           # Directory for reports
LOG_LEVEL=INFO                # Logging level (DEBUG, INFO, WARNING, ERROR)

Custom Wordlist

To customize subdomain enumeration, modify the SUBDOMAIN_WORDLIST in config/settings.py:
python

SUBDOMAIN_WORDLIST = [
    "www", "mail", "ftp", "custom1", "custom2"
]

Architecture
Modules Overview

Reconnaissance Module

    Subdomain Finder: Uses DNS resolution with a comprehensive wordlist to discover subdomains

    Port Scanner: Detects open ports and identifies running services

AI Module

    LLM Handler: Interfaces with Ollama for local AI analysis

    Exploit Generator: Creates AI-generated exploit code for detected vulnerabilities

Exploit Module

    SQL Injection: Tests URL parameters for SQL injection vulnerabilities using various payloads

    XSS: Tests for Cross-Site Scripting vulnerabilities with multiple payload types

Report Module

    Generator: Creates comprehensive reports in both text and JSON formats

Example Output
Terminal Output
text

╔═══════════════════════════════════════════════════════════╗
║                    🦅 EAGLEEYE REPORT                    ║
╠═══════════════════════════════════════════════════════════╣
║  Target: example.com                                      ║
║  Time:   2024-01-01 12:00:00                             ║
╚═══════════════════════════════════════════════════════════╝

═══ SUBDOMAINS ═══
  - www.example.com
  - mail.example.com
  - admin.example.com
  - api.example.com
  - dev.example.com

═══ OPEN PORTS ═══
  - 22: SSH (open)
  - 80: HTTP (open)
  - 443: HTTPS (open)
  - 3306: MySQL (open)

═══ VULNERABILITIES ═══
  - SQL Injection
  - XSS

═══ AI ANALYSIS ═══
  Potential Vulnerabilities:
    - SQL Injection in login.php
    - XSS in search.php
    - Open MySQL port (3306) exposed to internet
  
  Related CVEs:
    - CVE-2023-12345
    - CVE-2023-67890
  
  Risk Score: 8/10
  
  Recommendations:
    - Implement input validation for all user inputs
    - Move database to private subnet
    - Enable Web Application Firewall (WAF)
    - Apply security patches for MySQL

Report File

A detailed report is saved to reports/report_example_com_20240101_120000.txt containing all scan results.
Legal Disclaimer

IMPORTANT: This tool is for authorized security testing only.

By using EagleEye, you agree to:

    Only scan targets you have explicit written permission to test

    Not use this tool for any illegal or malicious purposes

    Comply with all applicable laws and regulations

    Accept full responsibility for your actions

The author is not responsible for any misuse, damage, or legal consequences resulting from the use of this tool. Always obtain proper authorization before conducting security testing.
Security Considerations

    All processing is done locally - no data is sent to external servers

    The tool does not contain any backdoors or malicious code

    Reports are stored locally and not shared automatically

    Use in isolated environments when testing sensitive targets

Contributing

Contributions are welcome and appreciated. To contribute:

    Fork the repository

    Create a feature branch

    Make your changes

    Submit a pull request

Guidelines:

    Write clear commit messages

    Follow existing code style

    Add tests for new features

    Update documentation accordingly

License

This project is licensed under the MIT License. See the LICENSE file for details.

MIT License

Copyright (c) 2024 EagleEye Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
