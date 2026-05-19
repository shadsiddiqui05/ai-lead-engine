import os
import uuid
import tempfile
from app.models.schemas import LeadSubmission
from app.services.enrichment import gather_company_context
from app.services.ai_agent import generate_insights
from app.services.pdf_builder import create_pdf
from app.services.emailer import send_audit_email
from app.services.google_service import log_lead_to_sheet, upload_pdf_to_drive

def run_automation_pipeline(lead: LeadSubmission):
    """The master function that executes the end-to-end workflow asynchronously."""
    pdf_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}_{lead.company_name.replace(' ', '_')}_audit.pdf")
    
    # Log initial status
    log_lead_to_sheet(lead.prospect_name, lead.email, lead.company_name, "Processing")
    
    try:
        print(f"\n--- [START] Pipeline initiated for {lead.company_name} ---")
        
        # Step 1: Scrape & Enrich
        context = gather_company_context(lead.company_name, lead.website)
        
        # Step 2: AI Analysis & Formatting
        report_data = generate_insights(lead.company_name, context)
        
        # Step 3: PDF Generation
        create_pdf(lead, report_data, pdf_path)
        
        # Bonus: PDF Archiving
        upload_pdf_to_drive(pdf_path, lead.company_name)
        
        # Step 4: Email Delivery
        send_audit_email(lead, pdf_path)
        
        print(f"--- [SUCCESS] Workflow complete for {lead.company_name} ---\n")
        # Log success status
        log_lead_to_sheet(lead.prospect_name, lead.email, lead.company_name, "Completed")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n--- [ERROR] Pipeline failed for {lead.company_name}: {str(e)} ---\n")
        # Log failure status
        log_lead_to_sheet(lead.prospect_name, lead.email, lead.company_name, "Failed")
        
    finally:
        # Crucial: Always clean up the temporary PDF file to prevent storage leaks on the server
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            print(f"[Cleanup] Removed temporary file: {pdf_path}")