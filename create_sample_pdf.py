from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import os

def create_sample_pdf(path):
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, "Visa Application Form")
    
    c.drawString(100, 700, "Surname:")
    c.acroForm.textfield(name='Text_Field_01', tooltip='Surname',
                        x=200, y=690, width=300, height=20,
                        borderColor=colors.black, fillColor=colors.white, 
                        textColor=colors.black, forceBorder=True)
    
    c.drawString(100, 650, "Given Name:")
    c.acroForm.textfield(name='Text_Field_02', tooltip='Given Name',
                        x=200, y=640, width=300, height=20,
                        borderColor=colors.black, fillColor=colors.white, 
                        textColor=colors.black, forceBorder=True)
                        
    c.drawString(100, 600, "Nationality:")
    c.acroForm.textfield(name='Text_Field_03', tooltip='Nationality',
                        x=200, y=590, width=300, height=20,
                        borderColor=colors.black, fillColor=colors.white, 
                        textColor=colors.black, forceBorder=True)

    c.save()

if __name__ == "__main__":
    create_sample_pdf("visa_form.pdf")
