import os
import json
import google.generativeai as genai
from google.api_core import exceptions
from typing import Dict, Any, Optional

class GeminiService:
    """
    AI Engineer implementation for Multilingual Learning Assistant.
    Uses Gemini 1.5 Flash for high speed and structured JSON output.
    """
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        
        genai.configure(api_key=api_key)
        
        # We use gemini-1.5-flash for the best balance of speed and reasoning
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )

    def _safe_generate(self, prompt: str, system_instruction: str) -> Dict[str, Any]:
        """Internal helper to handle API calls and parse JSON safely."""
        try:
            # Combining system instruction and prompt for clarity
            full_prompt = f"SYSTEM: {system_instruction}\n\nUSER: {prompt}"
            response = self.model.generate_content(full_prompt)
            
            if not response.text:
                return {"error": "Empty response from AI service", "content": None}
                
            return json.loads(response.text)
        
        except exceptions.InvalidArgument as e:
            return {"error": f"Invalid request parameters: {str(e)}", "content": None}
        except exceptions.ResourceExhausted:
            return {"error": "Quota exceeded. Please try again later.", "content": None}
        except json.JSONDecodeError:
            return {"error": "AI returned malformed JSON", "content": response.text}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}", "content": None}

    def explain_topic(self, topic: str, language: str, grade: str) -> Dict[str, Any]:
        """Generates a grade-appropriate explanation in the specified language."""
        system_instruction = (
            f"You are a master educator. Explain topics clearly for a student at {grade} level. "
            "Return a JSON object with keys: 'title', 'explanation' (Markdown formatted), "
            "and 'key_terms' (a list of 3-5 important words)."
        )
        prompt = f"Explain the topic '{topic}' in the language: {language}."
        
        return self._safe_generate(prompt, system_instruction)

    def summarize_text(self, text: str, language: str) -> Dict[str, Any]:
        """Summarizes long text into a concise format."""
        system_instruction = (
            f"You are a summarization expert. Output in {language}. "
            "Return a JSON object with keys: 'summary' (concise paragraph) and 'bullet_points' (list of 3 key takeaways)."
        )
        prompt = f"Summarize the following text accurately:\n\n{text}"
        
        return self._safe_generate(prompt, system_instruction)

    def generate_quiz(self, topic: str, language: str) -> Dict[str, Any]:
        """Generates 5 multiple choice questions in a structured format."""
        system_instruction = (
            f"You are a quiz generator. Create 5 multiple-choice questions about '{topic}' in {language}. "
            "Return a JSON object with a key 'quiz' containing a list of objects. "
            "Each object must have: 'question', 'options' (list of 4 strings), and 'correct_answer' (exact string from options)."
        )
        prompt = f"Generate a 5-question MCQ quiz about {topic}."
        
        return self._safe_generate(prompt, system_instruction)