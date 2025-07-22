from flask import Flask, render_template, request, redirect
from utils.email_generator import generate_email, improve_email

from models.database import save_email, get_all_emails


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Load email history to show on the same page
    email_history = get_all_emails()
    return render_template('index.html', emails=email_history)

@app.route('/generate', methods=['POST'])
def generate():
    idea = request.form['idea']
    tone = request.form.get('tone', 'friendly')
    length = request.form.get('length', 'medium')  # NEW: get length from form

    # Pass all needed params to your email generator
    generated = generate_email(idea, tone, length)

    # Save email data including length
    save_email({
        'idea': idea,
        'tone': tone,
        'length': length,       # NEW: store length
        'generated': generated,
        'improved': ""
    })

    # Reload page with result and history
    emails = get_all_emails()
    return render_template('index.html', result=generated, emails=emails)


@app.route('/improve', methods=['POST'])
def improve():
    old_email = request.form['original_email']
    improved = improve_email(old_email)

    # Save improved version
    save_email(idea='Improved email', tone='N/A', generated=old_email, improved=improved)

    email_history = get_all_emails()
    return render_template('index.html', emails=email_history, improved=improved, original=old_email)

if __name__ == '__main__':
    app.run(debug=True)

from dotenv import load_dotenv
import os
import openai

load_dotenv()  # load environment variables from .env (if you use .env)

