import os

from email_validator import EmailNotValidError, validate_email
import httpx


class EmailValidationService:
    """Service for email validation using external APIs"""

    def __init__(self):
        self.api_key = os.getenv("EMAIL_VALIDATION_API_KEY")
        self.provider = os.getenv("EMAIL_VALIDATION_PROVIDER", "hunter")

    async def validate_email_syntax(self, email: str) -> dict:
        """Basic email syntax validation"""
        try:
            valid = validate_email(email, check_deliverability=False)
            return {"valid": True, "email": valid.normalized, "method": "syntax"}
        except EmailNotValidError as e:
            return {"valid": False, "error": str(e), "method": "syntax"}

    async def validate_email_full(self, email: str) -> dict:
        """
        Full email validation using external API
        Supports Hunter.io, ZeroBounce, etc.
        """
        if not self.api_key:
            # Fallback to syntax validation only
            return await self.validate_email_syntax(email)

        if self.provider == "hunter":
            return await self._validate_hunter(email)
        elif self.provider == "zerobounce":
            return await self._validate_zerobounce(email)
        else:
            return await self.validate_email_syntax(email)

    async def _validate_hunter(self, email: str) -> dict:
        """Validate email using Hunter.io API"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://api.hunter.io/v2/email-verifier",
                    params={"email": email, "api_key": self.api_key},
                    timeout=30.0,
                )
                response.raise_for_status()
                data = response.json()

                if "data" in data:
                    result = data["data"]
                    return {
                        "valid": result.get("status") == "valid",
                        "email": email,
                        "status": result.get("status"),
                        "score": result.get("score"),
                        "result": result.get("result"),
                        "provider": "hunter",
                        "success": True,
                    }
                return {"valid": False, "error": "Invalid response", "success": False}
            except httpx.HTTPError as e:
                return {"valid": False, "error": str(e), "success": False}

    async def _validate_zerobounce(self, email: str) -> dict:
        """Validate email using ZeroBounce API"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://api.zerobounce.net/v2/validate",
                    params={"email": email, "api_key": self.api_key},
                    timeout=30.0,
                )
                response.raise_for_status()
                data = response.json()

                return {
                    "valid": data.get("status") == "valid",
                    "email": email,
                    "status": data.get("status"),
                    "sub_status": data.get("sub_status"),
                    "provider": "zerobounce",
                    "success": True,
                }
            except httpx.HTTPError as e:
                return {"valid": False, "error": str(e), "success": False}

    async def find_email_pattern(self, first_name: str, last_name: str, domain: str) -> dict:
        """
        Find email pattern for a domain using Hunter.io
        """
        if not self.api_key or self.provider != "hunter":
            return {"error": "Hunter.io API key required", "success": False}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://api.hunter.io/v2/email-finder",
                    params={
                        "domain": domain,
                        "first_name": first_name,
                        "last_name": last_name,
                        "api_key": self.api_key,
                    },
                    timeout=30.0,
                )
                response.raise_for_status()
                data = response.json()

                if "data" in data and data["data"].get("email"):
                    return {
                        "email": data["data"]["email"],
                        "confidence": data["data"].get("score"),
                        "pattern": data["data"].get("pattern"),
                        "success": True,
                    }
                return {"error": "Email not found", "success": False}
            except httpx.HTTPError as e:
                return {"error": str(e), "success": False}
