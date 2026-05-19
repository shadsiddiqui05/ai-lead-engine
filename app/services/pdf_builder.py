import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from app.models.schemas import LeadSubmission, ReportData

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def create_pdf(lead: LeadSubmission, report_data: ReportData, output_path: str) -> str:
    """Renders the HTML template with AI data and compiles it to a PDF."""
    print("[PDF] Rendering template and building PDF...")
    template = env.get_template("report.html")
    
    html_content = template.render(
        company_name=lead.company_name,
        prospect_name=lead.prospect_name,
        report_data=report_data
    )
    
    HTML(string=html_content).write_pdf(output_path)
    return output_path