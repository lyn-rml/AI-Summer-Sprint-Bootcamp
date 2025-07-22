# AI Email Generator

## Project Overview

This is a simple web app that generates emails based on user input using OpenAI's GPT models. Users enter a general idea and select tone and length to receive a generated email, with options to improve it and view email history.

---

## Features

- Input a general idea for the email
- Select tone: Friendly, Professional, Urgent
- Select email length: Short, Medium, Long
- Generate emails powered by OpenAI's GPT API
- Improve generated emails with a single click
- Save and view previously generated emails

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

Obtain an OpenAI API Key
Sign up at OpenAI and create an account

Go to the API keys page: OpenAI API Keys

Generate a new secret key and copy it

create a .env file with the following content:

OPENAI_API_KEY=your-api-key-here

Run the application
python app.py
Open your browser and go to http://127.0.0.1:5000/

