import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from app.core.config import settings
from app.models.schemas import LeadSubmission

def send_audit_email(lead: LeadSubmission, pdf_path: str):
    """Attaches the compiled PDF and sends it via SMTP."""
    print(f"[Email] Dispatching report to {lead.email}...")
    
    sender_email = settings.SMTP_EMAIL
    sender_password = settings.SMTP_PASSWORD
    
    if not sender_email or not sender_password:
        print("[Email Error] SMTP_EMAIL or SMTP_PASSWORD not configured.")
        return

    msg = MIMEMultipart()
    msg['From'] = f"SimplifIQ Assessment <{sender_email}>"
    msg['To'] = lead.email
    msg['Subject'] = f"Your personalized audit for {lead.company_name}"
    
    body = f"""
    <p>Hi {lead.prospect_name},</p>
    <p>Thank you for your interest. We've compiled an automated initial audit of <strong>{lead.company_name}</strong> based on your submission.</p>
    <p>Please find the report attached to this email.</p>
    <p>Best,<br>The SimplifIQ Team</p>
    """
    msg.attach(MIMEText(body, 'html'))
    
    with open(pdf_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(pdf_path))
    part['Content-Disposition'] = f'attachment; filename="{lead.company_name}_Audit.pdf"'
    msg.attach(part)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"[Email] Successfully sent to {lead.email}")
    except Exception as e:
        print(f"[Email Error] Failed to send email: {e}")
        raise e