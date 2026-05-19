import resend
from app.core.config import settings
from app.models.schemas import LeadSubmission

resend.api_key = settings.RESEND_API_KEY

def send_audit_email(lead: LeadSubmission, pdf_path: str):
    """Attaches the compiled PDF and sends it via the Resend API."""
    print(f"[Email] Dispatching report to {lead.email}...")
    
    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = list(pdf_file.read())

    params = {
        "from": "SimplifIQ Assessment <onboarding@resend.dev>", # Allowed on Resend Free Tier
        "to": [lead.email],
        "subject": f"Your personalized audit for {lead.company_name}",
        "html": f"""
        <p>Hi {lead.prospect_name},</p>
        <p>Thank you for your interest. We've compiled an automated initial audit of <strong>{lead.company_name}</strong> based on your submission.</p>
        <p>Please find the report attached to this email.</p>
        <p>Best,<br>The SimplifIQ Team</p>
        """,
        "attachments": [
            {"filename": f"{lead.company_name}_Audit.pdf", "content": pdf_bytes}
        ]
    }
    
    resend.Emails.send(params)