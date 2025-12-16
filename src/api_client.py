import requests
import pandas as pd
import streamlit as st

class ProxycurlClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {'Authorization': 'Bearer ' + api_key}
        self.base_url = "https://nubela.co/proxycurl/api"

    def search_people(self, query, limit=10):
        """
        Searches for people on LinkedIn using Proxycurl's Person Search API.
        NOTE: This is a simulated wrapper if the user API key is not valid or for demo purposes
        because the Search API is expensive/restricted. 
        
        For this implementation, we will try to reach the endpoint.
        """
        # Endpoint for person search (Note: verify documentation for exact endpoint)
        # Using a hypothetical search endpoint structure or profile implementation
        # Real implementation would often use Google Search API + Profile Endpoint
        # For this tool, we will assume we are fetching profile details given a LinkedIn URL
        # But since we need to FIND them first, we will implement a mock search that returns
        # valid profile IDs if no robust search API is available, or use the real one if configured.
        
        # PROXYCURL SEARCH API (Requires formatting)
        # For simplicity in this demo, we will warn the user about credit usage.
        
        # NOTE: Since we cannot guarantee the user has the Search API enabled,
        # we will implement a safer "Enrichment" flow where they input a LinkedIn URL,
        # OR we try to simulate the search if the API fails.
        pass

    def mock_live_response(self):
        """
        Returns a structured response that LOOKS like a real API response
        for testing the UI without burning credits.
        """
        # This acts as a bridge between the simulator and the "Live" structure
        return [
            {
                "full_name": "Dr. Sarah Chen",
                "occupation": "Director of Toxicology at Genentech",
                "country_full_name": "United States",
                "city": "South San Francisco",
                "state": "California",
                "headline": "Safety Assessment Leader | In-Vitro Models Expert",
                "public_identifier": "sarah-chen-genentech",
                "company": "Genentech",
                "company_hq": "San Francisco, CA" 
            },
             {
                "full_name": "Michael Ross",
                "occupation": "VP Preclinical Safety at Moderna",
                "country_full_name": "United States",
                "city": "Cambridge",
                "state": "Massachusetts",
                "headline": "mRNA Toxicology | Drug Safety",
                "public_identifier": "michael-ross-moderna",
                "company": "Moderna",
                "company_hq": "Cambridge, MA"
            }
        ]
    
    def normalize_to_internal_format(self, raw_data):
        """
        Converts API response data into the format expected by ScoringEngine.
        """
        normalized_leads = []
        
        for person in raw_data:
            # Extract location
            city = person.get("city", "")
            state = person.get("state", "")
            country = person.get("country_full_name", "")
            location = f"{city}, {state}" if city and state else country
            
            # Basic parsing of occupation to get Role/Company if separate fields aren't tight
            # Proxycurl usually gives structured job history, but search results are lighter.
            
            lead = {
                "Name": person.get("full_name", "Unknown"),
                # "Title" removed to avoid duplicates when app.py renames Role -> Title
                "Company": person.get("company", "Unknown Company"),
                "Person_Location": location,
                "Company_HQ": person.get("company_hq", "Unknown HQ"), # Often requires 2nd lookup
                "Email": "Hidden (Requires Enrichment)", # APIs often hide email in basic tier
                "Funding_Status": "Unknown", # Requires Crunchbase API lookup
                "Has_Published_Recently": False, # Requires PubMed lookup
                "Uses_InVitro_Models": False,
                "LinkedIn_Profile": f"linkedin.com/in/{person.get('public_identifier', '')}",
                "Role": person.get("occupation", "Unknown Role") # Compatibility
            }
            
            # Simple keyword check for signals if we don't have deep enrichment
            headline = person.get("headline", "").lower()
            if "in-vitro" in headline or "3d model" in headline:
                lead["Uses_InVitro_Models"] = True
            
            normalized_leads.append(lead)
            
        return pd.DataFrame(normalized_leads)
