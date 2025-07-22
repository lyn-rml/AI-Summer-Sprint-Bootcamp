import google.generativeai as genai
import os
from typing import Literal

def generate_email(
    description: str,
    tone: Literal['professional', 'friendly'] = 'professional',
    length: Literal['short', 'medium', 'long'] = 'medium',
    mode: Literal['generate', 'improve'] = 'generate',
    api_key: str = None
) -> str:
    """
    Generate or improve an email based on parameters
    
    Args:
        description (str): Email description or draft to improve
        tone (str): 'professional' or 'friendly'
        length (str): 'short', 'medium', or 'long'
        mode (str): 'generate' (create from description) or 'improve' (enhance existing draft)
        api_key (str): Google Gemini API key. If None, will try to get from environment variable GEMINI_API_KEY
        
    Returns:
        str: Generated or improved email content
    """
    
    # Setup API
    if api_key is None:
        api_key = getattr(generate_email, 'api_key', None)
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("API key is required. Set generate_email.api_key, GEMINI_API_KEY environment variable, or pass api_key parameter")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Build prompt based on mode
    if mode == 'generate':
        prompt = _build_generate_prompt(description, tone, length)
    elif mode == 'improve':
        prompt = _build_improve_prompt(description, tone, length)
    else:
        raise ValueError("Mode must be 'generate' or 'improve'")
    
    # Generate email
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating email: {str(e)}"

def _build_generate_prompt(description: str, tone: str, length: str) -> str:
    """Build prompt for generating new email"""
    
    tone_instructions = {
        'professional': 'formal, business-appropriate, respectful',
        'friendly': 'warm, casual but polite, personable'
    }
    
    length_instructions = {
        'short': 'concise and brief (2-4 sentences)',
        'medium': 'moderate length (1-2 paragraphs)',
        'long': 'detailed and comprehensive (2-4 paragraphs)'
    }
    
    prompt = f"""
Write a {tone_instructions[tone]} email that is {length_instructions[length]}.

Email requirements:
- Topic/Purpose: {description}
- Tone: {tone_instructions[tone]}
- Length: {length_instructions[length]}

Please include:
1. Appropriate subject line
2. Professional greeting
3. Clear main content
4. Appropriate closing

Format the output as:
Subject: [subject line]

[email body]

Best regards,
[Sender]
"""
    return prompt

def _build_improve_prompt(draft: str, tone: str, length: str) -> str:
    """Build prompt for improving existing email draft"""
    
    tone_instructions = {
        'professional': 'more formal, business-appropriate, and respectful',
        'friendly': 'warmer, more casual but still polite, and personable'
    }
    
    length_instructions = {
        'short': 'more concise and brief',
        'medium': 'moderate length with good detail',
        'long': 'more detailed and comprehensive'
    }
    
    prompt = f"""
Please improve the following email draft to make it {tone_instructions[tone]} and {length_instructions[length]}.

Original draft:
{draft}

Improvement requirements:
- Make the tone {tone_instructions[tone]}
- Adjust length to be {length_instructions[length]}
- Improve clarity and structure
- Fix any grammar or formatting issues
- Keep the core message intact

Please provide the improved version with proper email formatting including subject line if missing.
"""
    return prompt
import os
import google.generativeai as genai
from typing import Literal

import os
from typing import Literal
import google.generativeai as genai

def rebuild_given_email(
    draft: str,
    tone: Literal['professional', 'friendly'] = 'professional',
    length: Literal['short', 'medium', 'long'] = 'medium',
    api_key: str = None
) -> str:
    """
    Improve an existing email draft based on tone and length preferences.

    Args:
        draft (str): Original email draft to improve
        tone (str): 'professional' or 'friendly'
        length (str): 'short', 'medium', or 'long'
        api_key (str): Google Gemini API key. If None, tries from generate_email.api_key or GEMINI_API_KEY

    Returns:
        str: Improved email content
    """

    if not draft.strip():
        return "⚠️ The draft email cannot be empty."

    if api_key is None:
        # Try to get from generate_email.api_key (if it exists)
        api_key = getattr(generate_email, 'api_key', None)
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("❌ API key is required. Set generate_email.api_key, GEMINI_API_KEY environment variable, or pass api_key parameter.")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
Improve the following email:

Tone: {"Formal and business-appropriate" if tone == "professional" else "Friendly and warm"}
Length: {"Concise" if length == "short" else "Moderate detail" if length == "medium" else "Detailed and comprehensive"}

Email:
\"\"\"{draft}\"\"\"

Instructions:
- Keep the original message and intent.
- Fix grammar, punctuation, and clarity.
- Apply the tone and adjust length as specified.
- Add or adjust subject line if needed.

Return only the improved email in well-formatted text.
"""

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"❌ Error improving email: {str(e)}"

# Optional: you can set a default API key like this
generate_email.api_key = "AIzaSyAZf036xdFOtalMYLqgF7ZibMRU5O2TkVU"
