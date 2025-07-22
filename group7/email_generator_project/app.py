from flask import Flask, render_template, request, redirect
from utils.email_generator import generate_email, rebuild_given_email

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
    length = request.form.get('length', 'medium')  # Optional, used by your generator

    # Generate the email text
    generated = generate_email(idea, tone, length)

    # Save the data (pass each argument individually)
    save_email(
        idea=idea,
        tone=tone,
        generated=generated,
        improved=""  # Empty for now
    )

    # Load emails to show on page
    emails = get_all_emails()

    # Render result
    return render_template('index.html', result=generated, emails=emails)



@app.route('/improve', methods=['POST'])
def improve():
    old_email = request.form['original_email']
    improved = rebuild_given_email(old_email)
    tone = request.form.get('tone', 'professional')
    length = request.form.get('length','medium')
    
    idea = request.form['idea']

    improved_text = rebuild_email(
        draft = old_email,
        tone = tone, 
        length = length
    )
    
    # Save improved version
    save_email(
    idea='Project update email '+idea,
    tone=tone,
    generated=old_email,
    improved=improved
)

    email_history = get_all_emails()
    return render_template('index.html', emails=email_history, improved=improved, original=old_email)

if __name__ == '__main__':
    app.run(debug=True)

from dotenv import load_dotenv
load_dotenv()  # load environment variables from .env (if you use .env)

