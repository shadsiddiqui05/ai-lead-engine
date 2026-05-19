from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.models.schemas import LeadSubmission
from app.services.orchestrator import run_automation_pipeline
import os

app = FastAPI(
    title="SimplifIQ Lead Engine API",
    description="Automated B2B lead enrichment, AI auditing, and PDF generation.",
    version="1.0.0"
)

# Mount the static directory to serve assets
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", include_in_schema=False)
async def serve_ui():
    """Serve the sleek HTML landing page."""
    return FileResponse("app/static/index.html")

@app.post("/api/v1/leads", status_code=202)
async def submit_lead(lead: LeadSubmission, background_tasks: BackgroundTasks):
    """
    Accepts lead data, validates it via Pydantic, and triggers the automation pipeline.
    Returns 202 immediately to prevent HTTP timeouts during processing.
    """
    background_tasks.add_task(run_automation_pipeline, lead)
    
    return {
        "status": "processing",
        "message": f"Lead received for {lead.company_name}. Research and reporting pipeline initiated."
    }

if __name__ == "__main__":
    import uvicorn
    # Start the application
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)