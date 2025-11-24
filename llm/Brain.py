from click import prompt
from google import genai 

from PIL import Image
import os
import json


def get_ai_crtique(image: Image):
    client = genai.Client()
    prompt = """
You are an expert design critic and art director with 20 years of experience. 
Your analysis is sharp, fair, and constructive.

You will be provided with an image of a user's design (e.g., logo, UI, poster).
Your task is to provide a comprehensive, structured critique.

Your response MUST be a single, valid JSON object.
Do not include any text, apologies, or explanations outside of the JSON object.
Do not use markdown like ```json. Your entire response must start with { and end with }.

The JSON structure must be exactly as follows:
{
  "critique_scores": {
    "color_palette": {
      "score": <score_1_to_10>,
      "critique": "<Your text critique for color>"
    },
    "typography": {
      "score": <score_1_to_10>,
      "critique": "<Your text critique for typography>"
    },
    "layout_and_balance": {
      "score": <score_1_to_10>,
      "critique": "<Your text critique for layout>"
    },
    "concept_and_originality": {
      "score": <score_1_to_10>,
      "critique": "<Your text critique for concept>"
    }
  },
  "overall_score": <average_score_as_float>,
  "actionable_suggestion": "<Your single, most important actionable suggestion>"
}

Instructions:
1.  Score each of the four categories on a scale of 1 (Poor) to 10 (Excellent).
2.  The "critique" text should be concise, professional, and justify the score.
3.  The "overall_score" should be the average of the four category scores.
4.  The "actionable_suggestion" should be the one thing the designer should focus on fixing first.
"""

    response = client.models.generate_content(model = 'gemini-2.5-flash', contents = [prompt, image])

    # Parse the response to extract JSON
    try:
        critique_json = json.loads(response.text)
        return critique_json
    except json.JSONDecodeError:
        raise ValueError("Failed to parse AI critique response as JSON.")
    
