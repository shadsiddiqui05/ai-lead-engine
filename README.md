# SimplifIQ Lead Engine

An automated B2B lead enrichment, AI auditing, and PDF generation workflow built for the SimplifIQ AI Software Developer Intern Assessment.

## Overview
This system automatically researches inbound leads, generates a highly personalized business audit, compiles it into a professional PDF report, and emails it directly to the prospect—all without human intervention.

### Core Workflow
1. **Intake & Validation**: Receives prospect data (Name, Email, Company, Website) via a FastAPI endpoint.
2. **Enrichment**: Uses the Tavily API to scrape real-time market data, recent news, and the prospect's actual website.
3. **AI Auditing**: Feeds the raw data into Google's Gemini 2.5 Flash model to generate a massive, structured JSON audit including financial signals, competitive analysis, and strategic recommendations.
4. **PDF Generation**: Renders the JSON into a beautiful HTML template using Jinja2 and converts it to a PDF using Weasyprint.
5. **Delivery**: Dispatches the PDF as an attachment to the prospect's email using the Resend API.
6. **Logging & Archiving (Bonus)**: Logs the lead's status to a Google Sheet and archives the generated PDF to a Google Drive folder.

## System Architecture & Design Decisions
- **FastAPI + BackgroundTasks**: We use FastAPI for lightning-fast request validation (via Pydantic). The pipeline is offloaded to `BackgroundTasks` so the API responds instantly with an `HTTP 202 Accepted`. This prevents HTTP timeouts during long research/generation cycles without the heavy overhead of introducing Celery/Redis for a prototype.
- **Strict Structured AI Outputs**: We enforce strict JSON schemas (`ReportData` Pydantic model) on the LLM output. This ensures the PDF template never breaks due to missing or hallucinated fields.
- **Graceful Fallbacks**: If Tavily web scraping fails (e.g. site blocks scrapers), the exception is caught and the pipeline continues gracefully with empty context, allowing Gemini to rely on its training data instead of breaking the workflow.
- **Temporary File Management**: PDFs are generated in the OS-agnostic temp directory (`tempfile.gettempdir()`) and are strictly cleaned up in a `finally` block to prevent server storage leaks.

## Setup Instructions

### Prerequisites
You will need API keys for the following services:
- **Gemini API** (Google AI Studio)
- **Tavily API** (Search & Extraction)
- **Resend API** (Email Delivery)
- **Google Cloud API Key** (For Sheets/Drive integration)

### 1. Environment Setup
Clone the repository and install the dependencies:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory and populate it with your keys:
```env
GEMINI_API_KEY=your_gemini_key
TAVILY_API_KEY=your_tavily_key
RESEND_API_KEY=your_resend_key
# Google Workspace Integrations
GOOGLE_SERVICE_ACCOUNT_FILE=your_service_account.json
GOOGLE_SHEET_ID=your_sheet_id
GOOGLE_DRIVE_FOLDER_ID=your_drive_folder_id
```

### 3. Running the Server
Start the FastAPI server using Uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000/api/v1/leads`. You can use the interactive Swagger documentation at `http://localhost:8000/docs` to submit a test lead.
