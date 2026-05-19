import resend
import os
from app.core.config import settings
from app.models.schemas import LeadSubmission

def send_audit_email(lead: LeadSubmission, pdf_path: str):
    """Attaches the compiled PDF and sends it via Resend API."""
    print(f"[Email] Dispatching report to {lead.email} via Resend...")
    
    if not settings.RESEND_API_KEY:
        print("[Email Error] RESEND_API_KEY not configured.")
        return

    resend.api_key = settings.RESEND_API_KEY

    with open(pdf_path, "rb") as f:
        pdf_bytes = list(f.read())

    # Resend restricts free tier to verified domains or the registered email.
    # The 'from' email below usually needs to be updated to your verified domain (e.g. 'onboarding@resend.dev' or your domain).
    from_email = "SimplifIQ Assessment <onboarding@resend.dev>"
    
    params = {
        "from": from_email,
        "to": [lead.email],
        "subject": f"Your personalized audit for {lead.company_name}",
        "html": f"""
        <p>Hi {lead.prospect_name},</p>
        <p>Thank you for your interest. We've compiled an automated initial audit of <strong>{lead.company_name}</strong> based on your submission.</p>
        <p>Please find the report attached to this email.</p>
        <p>Best,<br>The SimplifIQ Team</p>
        """,
        "attachments": [
            {
                "filename": f"{lead.company_name}_Audit.pdf",
                "content": pdf_bytes
            }
        ]
    }
    
    try:
        email_response = resend.Emails.send(params)
        print(f"[Email] Successfully sent to {lead.email} via Resend. ID: {email_response.get('id', 'N/A')}")
    except Exception as e:
        print(f"[Email Error] Failed to send email via Resend: {e}")
        raise e