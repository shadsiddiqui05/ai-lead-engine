from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class LeadSubmission(BaseModel):
    prospect_name: str
    email: EmailStr
    company_name: str
    website: Optional[str] = None

# --- NESTED MODELS FOR THE AI AUDIT ---
class Product(BaseModel):
    name: str
    description: str

class CompetitiveLandscape(BaseModel):
    main_competitors: List[str]
    competitive_advantages: List[str]
    market_position: str

class DigitalPresence(BaseModel):
    seo_strength: str 
    content_strategy: str
    developer_community: str
    social_signals: str

class FinancialSignals(BaseModel):
    revenue_estimate: str
    growth_trajectory: str
    funding_status: str
    profitability_notes: str

class GrowthOpportunity(BaseModel):
    title: str
    description: str
    priority: str 

class AuditScore(BaseModel):
    overall: int
    digital_presence: int
    market_position: int
    growth_potential: int
    operational_maturity: int

class Recommendation(BaseModel):
    title: str
    detail: str
    impact: str 

class ReportData(BaseModel):
    """The main schema matching the massive Gemini output."""
    company_name: str
    website: str
    industry: str
    founded: str
    headquarters: str
    valuation: str
    employee_count: str
    business_model: str
    executive_summary: str 
    key_products: List[Product]
    target_markets: List[str]
    competitive_landscape: CompetitiveLandscape
    digital_presence: DigitalPresence
    financial_signals: FinancialSignals
    tech_stack_signals: List[str]
    growth_opportunities: List[GrowthOpportunity]
    risk_factors: List[str]
    audit_score: AuditScore
    key_insights: List[str] 
    recommendations: List[Recommendation]