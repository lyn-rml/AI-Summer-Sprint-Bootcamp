import google.generativeai as genai
import os
from typing import Literal, Optional

class EmailGenerator:
    """Simple email generator and improver using Google Gemini"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize with API key
        
        Args:
            api_key: Google Gemini API key. If None, uses GEMINI_API_KEY env variable
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("API key required. Set GEMINI_API_KEY environment variable or pass api_key")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_email(
        self,
        description: str,
        tone: Literal['professional', 'friendly'] = 'professional',
        length: Literal['short', 'medium', 'long'] = 'medium'
    ) -> str:
        """
        Generate a new email from description
        
        Args:
            description: What the email should be about
            tone: Email tone - 'professional' or 'friendly'
            length: Email length - 'short', 'medium', or 'long'
            
        Returns:
            Generated email content
        """
        
        tone_style = {
            'professional': 'formal, business-appropriate, respectful',
            'friendly': 'warm, casual but polite, conversational'
        }
        
        length_guide = {
            'short': 'brief and concise (2-4 sentences)',
            'medium': 'moderate length (1-2 paragraphs)', 
            'long': 'detailed and comprehensive (3-4 paragraphs)'
        }
        
        prompt = f"""
Write an email that is {tone_style[tone]} and {length_guide[length]}.

Topic: {description}

Requirements:
- Include subject line
- Proper greeting and closing
- Clear, well-structured content
- {tone_style[tone]} tone throughout

Format:
Subject: [subject line]

[email body with greeting, content, and closing]
"""
        
        return self._generate_content(prompt)
    
    def improve_email(
        self,
        draft: str,
        tone: Literal['professional', 'friendly'] = 'professional',
        length: Literal['short', 'medium', 'long'] = 'medium'
    ) -> str:
        """
        Improve an existing email draft
        
        Args:
            draft: Original email to improve
            tone: Desired tone - 'professional' or 'friendly'
            length: Desired length - 'short', 'medium', or 'long'
            
        Returns:
            Improved email content
        """
        
        if not draft.strip():
            return "Error: Email draft cannot be empty"
        
        tone_adjustment = {
            'professional': 'more formal and business-appropriate',
            'friendly': 'warmer and more conversational while remaining polite'
        }
        
        length_adjustment = {
            'short': 'more concise and to-the-point',
            'medium': 'well-balanced with appropriate detail',
            'long': 'more detailed and comprehensive'
        }
        
        prompt = f"""
Improve this email draft:

Original Email:
{draft}

Make it {tone_adjustment[tone]} and {length_adjustment[length]}.

Improvements needed:
- Fix grammar, spelling, and punctuation
- Improve clarity and flow
- Adjust tone to be {tone_adjustment[tone]}
- Adjust length to be {length_adjustment[length]}
- Keep the original message and intent
- Ensure proper email formatting

Return only the improved email.
"""
        
        return self._generate_content(prompt)
    
    def _generate_content(self, prompt: str) -> str:
        """Generate content using Gemini model with error handling"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating email: {str(e)}"


# Convenience functions for backward compatibility
def generate_email(
    description: str,
    tone: Literal['professional', 'friendly'] = 'professional',
    length: Literal['short', 'medium', 'long'] = 'medium',
    api_key: Optional[str] = None
) -> str:
    """Generate email using function interface"""
    generator = EmailGenerator(api_key)
    return generator.generate_email(description, tone, length)


def improve_email(
    draft: str,
    tone: Literal['professional', 'friendly'] = 'professional', 
    length: Literal['short', 'medium', 'long'] = 'medium',
    api_key: Optional[str] = None
) -> str:
    """Improve email using function interface"""
    generator = EmailGenerator(api_key)
    return generator.improve_email(draft, tone, length)


# Example usage:
if __name__ == "__main__":
    # Using class interface
    email_gen = EmailGenerator()
    
    # Generate new email
    new_email = email_gen.generate_email(
        "Follow up on project meeting", 
        tone='professional', 
        length='medium'
    )
    
    # Improve existing email
    draft = "hey can we meet tomorrow about the project?"
    improved = email_gen.improve_email(draft, tone='professional', length='medium')
    
    print("Generated Email:")
    print(new_email)
    print("\nImproved Email:")
    print(improved)