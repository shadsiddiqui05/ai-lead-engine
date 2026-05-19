from tavily import TavilyClient
from app.core.config import settings

client = TavilyClient(api_key=settings.TAVILY_API_KEY)

def gather_company_context(company_name: str, website: str) -> dict:
    """
    Pulls company data using Tavily search + extract.
    Returns a dict of raw research ready to feed into Gemini.
    """
    queries = [
        f"{company_name} company overview business model revenue 2024 2025",
        f"{company_name} competitors market position {website}",
        f"{company_name} latest news funding product launches",
        f"{company_name} tech stack engineering culture",
    ]
 
    all_results = []
    for q in queries:
        resp = client.search(
            query=q,
            search_depth="advanced",   # deeper crawl
            max_results=5,
            include_answer=True,       # Tavily's own AI summary
            include_raw_content=True,  # full page text
        )
        all_results.append({
            "query": q,
            "answer": resp.get("answer", ""),
            "results": [
                {
                    "title": r["title"],
                    "url": r["url"],
                    "content": r["content"][:800],  # trim for token budget
                }
                for r in resp.get("results", [])
            ]
        })
 
    # Also extract the homepage directly
    try:
        extract = client.extract(urls=[f"https://{website}"])
        homepage_text = extract["results"][0].get("raw_content", "")[:2000]
    except Exception:
        homepage_text = ""
 
    return {
        "company_name": company_name,
        "website": website,
        "homepage_content": homepage_text,
        "research": all_results,
    }