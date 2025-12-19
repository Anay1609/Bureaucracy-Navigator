import pypdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

def get_form_fields(pdf_path):
    """
    Uses pypdf to read a PDF and returns a dictionary of all form field names.
    """
    try:
        reader = pypdf.PdfReader(pdf_path)
        fields = reader.get_fields()
        if fields:
            return {k: v.get('/V', '') for k, v in fields.items()}
        return {}
    except Exception as e:
        print(f"Error reading PDF fields: {e}")
        return {}

def fill_pdf_form(input_path, output_path, data_dict):
    """
    Takes a source PDF, a dictionary of data (keys matching the form fields), 
    and saves a new filled PDF to the output path.
    
    Note: pypdf's form filling capabilities are limited. 
    For a robust solution, we often use a combination of pypdf to read and 
    reportlab to overlay text, or pypdf's update_page_form_field_values if supported.
    Here we will use pypdf's update_page_form_field_values for simplicity as requested.
    """
    try:
        reader = pypdf.PdfReader(input_path)
        writer = pypdf.PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.update_page_form_field_values(
            writer.pages[0], data_dict
        )

        with open(output_path, "wb") as output_stream:
            writer.write(output_stream)
        
        return output_path
    except Exception as e:
        print(f"Error filling PDF: {e}")
        return None
