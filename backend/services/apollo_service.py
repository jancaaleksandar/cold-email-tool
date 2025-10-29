import os

import httpx


class ApolloService:
    """Service for Apollo.io API integration"""

    def __init__(self):
        self.api_key = os.getenv("APOLLO_API_KEY")
        self.base_url = "https://api.apollo.io/v1"

    async def enrich_person(
        self, first_name: str, last_name: str, company: str = None, linkedin_url: str = None
    ) -> dict:
        """
        Enrich person data using Apollo.io
        """
        if not self.api_key:
            raise ValueError("APOLLO_API_KEY not configured")

        async with httpx.AsyncClient() as client:
            payload = {
                "api_key": self.api_key,
                "first_name": first_name,
                "last_name": last_name,
            }

            if company:
                payload["organization_name"] = company
            if linkedin_url:
                payload["linkedin_url"] = linkedin_url

            try:
                response = await client.post(f"{self.base_url}/people/match", json=payload, timeout=30.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                return {"error": str(e), "success": False}

    async def find_email(self, first_name: str, last_name: str, domain: str) -> dict:
        """
        Find email address using Apollo.io
        """
        if not self.api_key:
            raise ValueError("APOLLO_API_KEY not configured")

        async with httpx.AsyncClient() as client:
            payload = {"api_key": self.api_key, "first_name": first_name, "last_name": last_name, "domain": domain}

            try:
                response = await client.post(f"{self.base_url}/people/match", json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()

                if data.get("person") and data["person"].get("email"):
                    return {
                        "email": data["person"]["email"],
                        "confidence": data["person"].get("email_status"),
                        "success": True,
                    }
                return {"error": "Email not found", "success": False}
            except httpx.HTTPError as e:
                return {"error": str(e), "success": False}

    async def search_people(self, filters: dict) -> dict:
        """
        Search for people using Apollo.io filters
        """
        if not self.api_key:
            raise ValueError("APOLLO_API_KEY not configured")

        async with httpx.AsyncClient() as client:
            payload = {"api_key": self.api_key, **filters}

            try:
                response = await client.post(f"{self.base_url}/mixed_people/search", json=payload, timeout=30.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                return {"error": str(e), "success": False}
