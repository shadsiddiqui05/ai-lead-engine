import json
import google.generativeai as genai
from app.core.config import settings
from app.models.schemas import ReportData

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# Use the fast and stable Flash model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={"temperature": 0.2, "response_mime_type": "application/json"},
)

AUDIT_SCHEMA = """
{
  "company_name": "string",
  "website": "string",
  "industry": "string",
  "founded": "string",
  "headquarters": "string",
  "valuation": "string",
  "employee_count": "string",
  "business_model": "string",
  "executive_summary": "3-4 sentence compelling overview",
  "key_products": [{"name": "string", "description": "string"}],
  "target_markets": ["string"],
  "competitive_landscape": {
    "main_competitors": ["string"],
    "competitive_advantages": ["string"],
    "market_position": "string"
  },
  "digital_presence": {
    "seo_strength": "Extremely Strong | Strong | Medium | Weak",
    "content_strategy": "string",
    "developer_community": "string",
    "social_signals": "string"
  },
  "financial_signals": {
    "revenue_estimate": "string",
    "growth_trajectory": "string",
    "funding_status": "string",
    "profitability_notes": "string"
  },
  "tech_stack_signals": ["string"],
  "growth_opportunities": [
    {"title": "string", "description": "string", "priority": "High | Medium"}
  ],
  "risk_factors": ["string"],
  "audit_score": {
    "overall": 0,
    "digital_presence": 0,
    "market_position": 0,
    "growth_potential": 0,
    "operational_maturity": 0
  },
  "key_insights": ["5 sharp, specific, non-generic insights"],
  "recommendations": [
    {"title": "string", "detail": "string", "impact": "High | Medium"}
  ]
}
"""

def generate_insights(company_name: str, context: dict) -> ReportData:
    """
    Feed Tavily research into Gemini -> get structured audit JSON back.
    """
    print(f"[AI] Generating massive structured audit for {company_name}...")

    prompt = f"""
    You are a senior business intelligence analyst. Based on the following research data about {company_name}, 
    generate a deeply personalized, professional audit report.

    RESEARCH DATA:
    {json.dumps(context, indent=2)}

    Generate the audit as valid JSON matching this schema exactly:
    {AUDIT_SCHEMA}

    Rules:
    - Be specific — use actual data from the research, not generic statements.
    - Audit scores should be realistic integers between 60-97.
    - Key insights must be sharp and non-obvious — things a consultant would charge for.
    - Recommendations must be actionable and tied to their actual business.
    - CRITICAL: If quantitative data (like valuation, revenue, or headcount) is missing, DO NOT guess. Output 'Not Publicly Disclosed'.

    Return ONLY the JSON object.
    """

    response = model.generate_content(prompt)
    raw_text = response.text.strip()
    
    # Failsafe: Remove markdown code blocks if the LLM hallucinated them
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
        
    raw_text = raw_text.strip()

    try:
        audit_data = json.loads(raw_text, strict=False)
        # Convert the raw dictionary into our strict Pydantic model
        return ReportData(**audit_data)
        
    except json.JSONDecodeError as e:
        print("\n--- RAW AI OUTPUT FOR DEBUGGING ---")
        print(raw_text)
        print("-----------------------------------\n")
        raise Exception(f"Failed to parse AI JSON: {str(e)}")