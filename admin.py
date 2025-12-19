from utils.pdf_handler import fill_pdf_form
import os

class AdminAgent:
    def __init__(self):
        # Simple mapping for demo purposes. 
        # In a real app, this might be dynamic or more comprehensive.
        self.field_mapping = {
            "surname": "Text_Field_01", # Example mapping, needs to be adjusted based on actual PDF
            "given_name": "Text_Field_02",
            "nationality": "Text_Field_03",
            "passport_number": "Text_Field_04",
            # Add more mappings as needed
        }

    def fill_application(self, user_data, pdf_template_path):
        """
        user_data: dict containing keys like 'surname', 'given_name', etc.
        pdf_template_path: path to the blank PDF
        """
        
        # Map user data to PDF fields
        pdf_data = {}
        for user_key, user_value in user_data.items():
            if user_key in self.field_mapping:
                pdf_field = self.field_mapping[user_key]
                pdf_data[pdf_field] = user_value
            else:
                # Fallback: try to use the key directly if it matches a PDF field
                # This is useful if we pass raw PDF field names
                pdf_data[user_key] = user_value

        output_path = "filled_application.pdf"
        
        result_path = fill_pdf_form(pdf_template_path, output_path, pdf_data)
        
        return result_path
