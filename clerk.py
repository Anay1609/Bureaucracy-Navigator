import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

class ClerkAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def audit_documents(self, passport_image_path, bank_statement_image_path, requirements_json):
        try:
            passport_img = Image.open(passport_image_path)
            bank_img = Image.open(bank_statement_image_path)
        except Exception as e:
            return {"status": "FAIL", "reason": f"Error loading images: {e}", "extracted_data": {}}

        prompt = f"""
        You are a strict visa clerk. Audit these documents against the following requirements:
        {json.dumps(requirements_json)}

        1. Extract the Passport Expiry Date from the passport image.
        2. Compare it to the 'passport_validity' rule (e.g., must be valid for 6 months).
        3. Extract the Bank Balance from the bank statement image.
        4. Compare it to the 'bank_balance' requirement.

        Return a JSON object with the following structure:
        {{
            "status": "PASS" or "FAIL",
            "reason": "Explanation of pass or fail",
            "extracted_data": {{
                "passport_expiry": "YYYY-MM-DD",
                "bank_balance": "Amount found"
            }}
        }}
        Do not include markdown formatting like ```json ... ```. Just the raw JSON string.
        """

        response = self.model.generate_content([prompt, passport_img, bank_img])
        
        try:
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            return json.loads(text)
        except Exception as e:
            print(f"Error parsing clerk response: {e}")
            return {"status": "FAIL", "reason": "AI parsing error", "extracted_data": {}}
