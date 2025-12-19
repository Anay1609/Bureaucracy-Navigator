from langchain_community.tools import DuckDuckGoSearchRun
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

class ResearcherAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-flash-latest')
        self.search = DuckDuckGoSearchRun()

    def find_requirements(self, nationality, destination_country, visa_type):
        query = f"official {visa_type} requirements for {nationality} citizen visiting {destination_country}"
        search_results = self.search.run(query)

        prompt = f"""
        Based on the following search results, extract the following information:
        1. Maximum stay duration
        2. Passport validity rule
        3. Bank balance requirement

        Search Results:
        {search_results}

        Return the output as a JSON object with keys: 'max_stay', 'passport_validity', 'bank_balance'.
        Do not include markdown formatting like ```json ... ```. Just the raw JSON string.
        """

        response = self.model.generate_content(prompt)
        try:
            # Clean up potential markdown formatting if the model ignores the instruction
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            return json.loads(text)
        except Exception as e:
            print(f"Error parsing researcher response: {e}")
            return {"error": "Could not extract requirements"}
