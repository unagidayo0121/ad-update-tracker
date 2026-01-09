import os
import google.generativeai as genai
from typing import Optional

class GeminiProcessor:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Warning: GOOGLE_API_KEY not found. Gemini processing will be skipped.")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def process_article(self, article_title: str, article_content: str) -> Optional[dict]:
        """
        Analyzes the article to determine:
        1. Is it an update about Ad platform features?
        2. Is it relevant to the Japan market?
        3. A 3-line summary in Japanese.
        
        Returns a dict with 'summary' if relevant, else None.
        """
        if not self.model:
            return None

        prompt = f"""
        You are an expert Ad Tech analyst. Analyze the following article title and content.

        Article Title: {article_title}
        Article Content Snippet: {article_content[:2000]}

        Tasks:
        1. Determine if this article is announcing a Feature Update, Policy Change, or New Functionality for an advertising platform (Google Ads, Yahoo Ads, Meta, etc.).
        2. Determine if this update is relevant to the Japanese market (or is a global update applicable to Japan).
        3. If YES to both, generate a concise 3-line summary in Japanese.
        
        Output Format (JSON):
        {{
            "is_ad_update": true/false,
            "is_relevant_to_japan": true/false,
            "summary_ja": "string (3 lines max)"
        }}
        
        Only return the JSON.
        """

        try:
            response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            import json
            result = json.loads(response.text)
            
            if result.get("is_ad_update") and result.get("is_relevant_to_japan"):
                return {
                    "summary": result.get("summary_ja")
                }
            return None
        except Exception as e:
            print(f"Error processing with Gemini: {e}")
            return None
