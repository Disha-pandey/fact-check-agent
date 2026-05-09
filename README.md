# Fact-Check Agent — AI-Powered PDF Claim Verification Web App

An AI-powered Streamlit web application that uploads PDF documents, extracts factual claims, verifies them against live web sources, and generates verification reports.

The system is designed to identify outdated, misleading, or hallucinated claims commonly found in:
- marketing content
- AI-generated reports
- research summaries
- business documents
- statistical statements

---

# Features

## PDF Upload & Text Extraction
- Upload PDF documents directly in the web app
- Extracts text using `pypdf`
- Detects claim-like sentences automatically

## Intelligent Claim Detection
The application identifies factual claims related to:
- percentages
- financial figures
- dates and years
- rankings
- growth metrics
- technical statements
- statistical information

## Live Web Verification
Claims are verified using live web search through:
- Tavily API
- Serper Google Search API
- DuckDuckGo fallback search

## AI-Based Fact Checking
Uses OpenAI to:
- analyze evidence
- verify factual accuracy
- generate explanations
- provide confidence scores
- suggest corrected facts

## Verification Results
Each claim is classified as:
- ✅ Verified
- ⚠️ Inaccurate
- ❌ False / No Evidence
- ❓ Needs Review

## Report Generation
- Interactive verification table
- Download CSV report
- Download Markdown report

---

# Tech Stack

## Frontend
- Streamlit

## Backend / Processing
- Python

## Libraries Used
- pypdf
- pandas
- requests
- duckduckgo-search

## APIs
- OpenAI API
- Tavily API
- Serper API

---

# Project Structure

```txt
fact-check-agent/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── sample_trap_document.md
│
├── src/
│   ├── __init__.py
│   ├── pdf_utils.py
│   ├── claim_extractor.py
│   ├── web_search.py
│   ├── verifier.py
│   └── report_utils.py
│
└── .streamlit/
    └── config.toml

Installation & Setup
1.Clone Repository
git clone https://github.com/Disha-pandey/fact-check-agent.git
cd fact-check-agent

2. Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Mac/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file and add your API keys:

OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
SERPER_API_KEY=your_serper_api_key

5. Run the Application
streamlit run app.py
Streamlit Cloud Deployment
Steps
Push the project to GitHub
Open Streamlit Community Cloud
Click New App
Select the repository
Set main file path:
app.py
Add Streamlit secrets:
OPENAI_API_KEY = "your_openai_api_key"
TAVILY_API_KEY = "your_tavily_api_key"
SERPER_API_KEY = "your_serper_api_key"
Deploy the application
Render Deployment

Use the following start command:

streamlit run app.py --server.port $PORT --server.address 0.0.0.0
Example Workflow
Upload a PDF document
Extract factual claims
Search live web evidence
Verify claim accuracy using AI
Generate downloadable verification reports
Future Improvements
Multi-language support
OCR support for scanned PDFs
Export PDF reports
Advanced source ranking
Citation confidence scoring
Batch document verification
Author
Disha Pandey

GitHub:
https://github.com/Disha-pandey

License

This project is developed for educational and project submission purposes.