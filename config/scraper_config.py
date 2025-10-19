import os
from firecrawl import Firecrawl

def scraper_config() -> Firecrawl:
    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))
    return firecrawl