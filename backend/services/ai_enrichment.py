import json
import os

import openai


class AIEnrichmentService:
    """Service for AI-powered lead enrichment using OpenAI"""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
        self.model = "gpt-4o-mini"  # or gpt-4 for better results

    async def enrich_lead_profile(self, lead_data: dict) -> dict:
        """
        Use AI to enrich lead profile with additional insights
        """
        if not self.api_key:
            return {"error": "OpenAI API key not configured", "success": False}

        try:
            prompt = self._build_enrichment_prompt(lead_data)

            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional B2B lead researcher. Provide accurate, actionable insights about leads.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=500,
            )

            result = response.choices[0].message.content

            return {"ai_insights": result, "model": self.model, "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}

    async def generate_personalized_intro(self, lead_data: dict, company_info: dict = None) -> dict:
        """
        Generate a personalized introduction or email opening
        """
        if not self.api_key:
            return {"error": "OpenAI API key not configured", "success": False}

        try:
            prompt = self._build_personalization_prompt(lead_data, company_info)

            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert cold email writer. Create personalized, engaging email openings.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.8,
                max_tokens=300,
            )

            intro = response.choices[0].message.content

            return {"personalized_intro": intro, "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}

    async def extract_company_info(self, company_name: str, website: str = None) -> dict:
        """
        Extract and summarize company information
        """
        if not self.api_key:
            return {"error": "OpenAI API key not configured", "success": False}

        try:
            prompt = f"""
            Research and provide key information about the company "{company_name}"{" (website: " + website + ")" if website else ""}.
            
            Provide:
            1. Industry
            2. Company size estimate
            3. Main products/services
            4. Recent news or developments (if known)
            5. Pain points they might have
            
            Format as JSON with keys: industry, size, products, news, pain_points
            """

            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a company research analyst. Provide concise, factual information.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=400,
            )

            result = response.choices[0].message.content

            try:
                # Try to parse as JSON
                company_info = json.loads(result)
            except json.JSONDecodeError:
                # If not valid JSON, return as text
                company_info = {"raw_info": result}

            return {"company_info": company_info, "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}

    async def analyze_linkedin_profile(self, linkedin_data: dict) -> dict:
        """
        Analyze LinkedIn profile data and extract insights
        """
        if not self.api_key:
            return {"error": "OpenAI API key not configured", "success": False}

        try:
            prompt = f"""
            Analyze this LinkedIn profile data and provide insights:
            
            {json.dumps(linkedin_data, indent=2)}
            
            Provide:
            1. Career trajectory summary
            2. Key skills and expertise
            3. Potential pain points based on role
            4. Best approach angle for outreach
            
            Format as JSON.
            """

            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional networker analyzing profiles for outreach."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.6,
                max_tokens=400,
            )

            result = response.choices[0].message.content

            return {"linkedin_insights": result, "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}

    def _build_enrichment_prompt(self, lead_data: dict) -> str:
        """Build prompt for lead enrichment"""
        lead_info = []
        if lead_data.get("first_name") and lead_data.get("last_name"):
            lead_info.append(f"Name: {lead_data['first_name']} {lead_data['last_name']}")
        if lead_data.get("title"):
            lead_info.append(f"Title: {lead_data['title']}")
        if lead_data.get("company"):
            lead_info.append(f"Company: {lead_data['company']}")
        if lead_data.get("linkedin_url"):
            lead_info.append(f"LinkedIn: {lead_data['linkedin_url']}")

        return f"""
        Based on the following lead information, provide insights about:
        1. Their likely responsibilities and decision-making authority
        2. Potential pain points in their role
        3. Best communication approach
        4. Relevant topics for engagement
        
        Lead Information:
        {chr(10).join(lead_info)}
        
        Provide concise, actionable insights.
        """

    def _build_personalization_prompt(self, lead_data: dict, company_info: dict = None) -> str:
        """Build prompt for personalized introduction"""
        return f"""
        Create a personalized, engaging email opening (2-3 sentences) for:
        
        Lead: {lead_data.get("first_name", "")} {lead_data.get("last_name", "")}
        Title: {lead_data.get("title", "Unknown")}
        Company: {lead_data.get("company", "Unknown")}
        {f"Additional context: {company_info}" if company_info else ""}
        
        Make it:
        - Specific and personalized
        - Relevant to their role
        - Natural and conversational
        - Not salesy or generic
        """
