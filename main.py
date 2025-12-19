import streamlit as st
import os
from agents.researcher import ResearcherAgent
from agents.clerk import ClerkAgent
from agents.admin import AdminAgent
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="The Bureaucracy Navigator", layout="wide")

st.title("The Bureaucracy Navigator")

# Sidebar
st.sidebar.header("Travel Details")
nationality = st.sidebar.text_input("Nationality", "Indian")
destination = st.sidebar.text_input("Destination", "Japan")
visa_type = st.sidebar.text_input("Visa Type", "Tourist Visa")

if st.sidebar.button("Start Research"):
    with st.spinner("Researching requirements..."):
        researcher = ResearcherAgent()
        requirements = researcher.find_requirements(nationality, destination, visa_type)
        st.session_state['requirements'] = requirements
        st.success("Research Complete!")

# Section 1: Requirements
st.header("1. Visa Requirements")
if 'requirements' in st.session_state:
    st.json(st.session_state['requirements'])
else:
    st.info("Click 'Start Research' to find requirements.")

# Section 2: Upload Documents
st.header("2. Upload Documents")
uploaded_passport = st.file_uploader("Upload Passport Image", type=['png', 'jpg', 'jpeg'])
uploaded_bank_statement = st.file_uploader("Upload Bank Statement Image", type=['png', 'jpg', 'jpeg'])

# Section 3: Audit & Apply
st.header("3. Audit & Apply")

if st.button("Audit & Apply"):
    if 'requirements' not in st.session_state:
        st.error("Please run research first.")
    elif not uploaded_passport or not uploaded_bank_statement:
        st.error("Please upload both documents.")
    else:
        # Save uploaded files temporarily
        passport_path = "temp_passport.jpg"
        bank_path = "temp_bank.jpg"
        
        with open(passport_path, "wb") as f:
            f.write(uploaded_passport.getbuffer())
        with open(bank_path, "wb") as f:
            f.write(uploaded_bank_statement.getbuffer())
            
        with st.spinner("Auditing documents..."):
            clerk = ClerkAgent()
            audit_result = clerk.audit_documents(passport_path, bank_path, st.session_state['requirements'])
            
        if audit_result.get("status") == "PASS":
            st.success("Audit Passed!")
            st.json(audit_result)
            
            with st.spinner("Filling application form..."):
                admin = AdminAgent()
                # Prepare user data for form filling
                # In a real app, we might ask for more details or extract more from the docs
                user_data = audit_result.get("extracted_data", {})
                # Add some dummy data for the demo if needed, or use what we have
                user_data['nationality'] = nationality
                
                # Assuming we have a template.pdf in the root
                pdf_template_path = "visa_form.pdf" 
                if not os.path.exists(pdf_template_path):
                     st.warning(f"Template PDF '{pdf_template_path}' not found. Please place it in the project root.")
                else:
                    result_path = admin.fill_application(user_data, pdf_template_path)
                    
                    if result_path:
                        st.success("Application Filled Successfully!")
                        with open(result_path, "rb") as pdf_file:
                            st.download_button(
                                label="Download Application",
                                data=pdf_file,
                                file_name="filled_visa_application.pdf",
                                mime="application/pdf"
                            )
                    else:
                        st.error("Failed to fill application.")
            
        else:
            st.error(f"Audit Failed: {audit_result.get('reason')}")
            st.json(audit_result)
