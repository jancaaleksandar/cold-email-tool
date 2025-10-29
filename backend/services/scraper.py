import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import httpx


class ScraperService:
    """Service for web scraping and data extraction"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def scrape_company_website(self, url: str) -> dict:
        """
        Scrape basic information from a company website
        """
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(url, headers=self.headers, timeout=30.0)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                # Extract basic info
                title = soup.find("title")
                description = soup.find("meta", attrs={"name": "description"})

                # Try to find social links
                social_links = self._extract_social_links(soup, url)

                # Try to find contact email
                emails = self._extract_emails(soup.get_text())

                return {
                    "url": url,
                    "title": title.text.strip() if title else None,
                    "description": description["content"] if description and description.get("content") else None,
                    "social_links": social_links,
                    "emails": list(set(emails)) if emails else [],
                    "success": True,
                }
        except Exception as e:
            return {"error": str(e), "success": False}

    async def scrape_linkedin_company(self, linkedin_url: str) -> dict:
        """
        Scrape LinkedIn company page (basic info only - respects robots.txt)
        Note: For production, use LinkedIn API instead
        """
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(linkedin_url, headers=self.headers, timeout=30.0)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                # Extract basic publicly available info
                # Note: Most LinkedIn data requires authentication
                title = soup.find("title")

                return {
                    "url": linkedin_url,
                    "title": title.text.strip() if title else None,
                    "note": "Limited data - use LinkedIn API for full access",
                    "success": True,
                }
        except Exception as e:
            return {"error": str(e), "success": False}

    async def find_company_domain(self, company_name: str) -> dict:
        """
        Try to find company domain using search
        Note: This is a basic implementation - consider using Clearbit or similar
        """
        try:
            # Simple approach: try common patterns
            company_slug = company_name.lower().replace(" ", "").replace(",", "").replace(".", "")
            possible_domains = [
                f"{company_slug}.com",
                f"{company_slug}.io",
                f"{company_slug}.co",
            ]

            async with httpx.AsyncClient(follow_redirects=True) as client:
                for domain in possible_domains:
                    try:
                        response = await client.get(f"https://{domain}", headers=self.headers, timeout=10.0)
                        if response.status_code == 200:
                            return {
                                "company_name": company_name,
                                "domain": domain,
                                "url": f"https://{domain}",
                                "success": True,
                            }
                    except:
                        continue

            return {"error": "Domain not found", "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}

    async def extract_contact_page(self, website_url: str) -> dict:
        """
        Find and scrape contact page
        """
        try:
            # First, try to find contact page
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(website_url, headers=self.headers, timeout=30.0)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                # Look for contact page link
                contact_link = None
                for link in soup.find_all("a", href=True):
                    href = link["href"].lower()
                    if any(word in href for word in ["contact", "about", "team"]):
                        contact_link = urljoin(website_url, link["href"])
                        break

                if contact_link:
                    # Scrape contact page
                    response = await client.get(contact_link, headers=self.headers, timeout=30.0)
                    soup = BeautifulSoup(response.text, "html.parser")

                # Extract emails and phone numbers
                text = soup.get_text()
                emails = self._extract_emails(text)
                phones = self._extract_phones(text)

                return {
                    "contact_page_url": contact_link,
                    "emails": list(set(emails)),
                    "phones": list(set(phones)),
                    "success": True,
                }
        except Exception as e:
            return {"error": str(e), "success": False}

    def _extract_social_links(self, soup: BeautifulSoup, base_url: str) -> dict:
        """Extract social media links from page"""
        social_links = {}
        social_domains = {
            "linkedin.com": "linkedin",
            "twitter.com": "twitter",
            "x.com": "twitter",
            "facebook.com": "facebook",
            "instagram.com": "instagram",
            "youtube.com": "youtube",
        }

        for link in soup.find_all("a", href=True):
            href = link["href"]
            for domain, platform in social_domains.items():
                if domain in href:
                    social_links[platform] = href
                    break

        return social_links

    def _extract_emails(self, text: str) -> list:
        """Extract email addresses from text"""
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        emails = re.findall(email_pattern, text)
        # Filter out common non-personal emails
        filtered = [e for e in emails if not any(x in e.lower() for x in ["example.com", "test.com", "placeholder"])]
        return filtered[:10]  # Limit to 10

    def _extract_phones(self, text: str) -> list:
        """Extract phone numbers from text"""
        phone_pattern = r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]"
        phones = re.findall(phone_pattern, text)
        return phones[:5]  # Limit to 5
