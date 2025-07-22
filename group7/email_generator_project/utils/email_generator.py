import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # or set directly

import openai

def generate_email(idea, tone, length="medium", details=None):
    # Build the prompt including length, tone, idea, and optional details
    prompt = f"Write a {length} length email about the idea: '{idea}' with a {tone} tone."
    if details:
        prompt += f" Include the following details: {details}"

    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are an expert email writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()



def improve_email(original_email):
    prompt = f"Improve this email by making it clearer and more professional:\n\n{original_email}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in rewriting emails clearly and professionally."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

