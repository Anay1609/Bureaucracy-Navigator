# Bureaucracy Navigator

The **Bureaucracy Navigator** is an AI-powered agentic workflow designed to simplify visa applications. It uses a team of AI agents to research requirements, audit documents, and fill out application forms automatically.

## 🤖 Agents

1.  **Researcher Agent**: Uses **DuckDuckGo** to find official visa requirements and **Gemini Flash Latest** to extract key rules (max stay, passport validity, bank balance).
2.  **Clerk Agent**: Uses **Gemini Flash Latest** (Vision) to audit your uploaded Passport and Bank Statement against the researched rules.
3.  **Admin Agent**: Automatically fills out the PDF visa application form with your details.

## 🛠️ Prerequisites

- Python 3.10+ (Python 3.14 supported with specific steps)
- A Google Cloud API Key (for Gemini models)

## 🚀 Installation

1.  **Clone the repository** (or navigate to the project folder):

    ```bash
    cd bureaucracy-navigator
    ```

2.  **Install Dependencies**:
    _Note: If you are using Python 3.14, follow these specific steps to avoid compatibility issues:_

    ```bash
    # 1. Install requirements
    pip install -r requirements.txt

    # 2. Fix Altair version for Streamlit compatibility
    pip install "altair<6"
    ```

    _For older Python versions, you can simply run:_

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration**:
    Create a `.env` file in the root directory and add your Google API Key:

    ```env
    GOOGLE_API_KEY=your_api_key_here
    ```

4.  **Generate Sample PDF** (Optional):
    If you don't have a `visa_form.pdf` template, generate a sample one:
    ```bash
    python create_sample_pdf.py
    ```

## ▶️ Usage

1.  Start the Streamlit application:
    ```bash
    streamlit run main.py
    ```
2.  Open your browser at `http://localhost:8501`.
3.  Enter your **Nationality**, **Destination**, and **Visa Type** in the sidebar.
4.  Click **Start Research** to find requirements.
5.  Upload your **Passport** and **Bank Statement** images.
6.  Click **Audit & Apply**.
    - If the audit passes, the agents will fill the PDF form.
    - Download the completed application.

## mb Project Structure

- `main.py`: The Streamlit UI and orchestrator.
- `agents/`: Contains the AI agent logic (`researcher.py`, `clerk.py`, `admin.py`).
- `utils/`: Helper scripts for PDF handling.
- `requirements.txt`: Project dependencies.
