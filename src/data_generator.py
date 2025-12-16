import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

# Configuration for data generation

ROLES = [
    "Director of Toxicology",
    "Head of Preclinical Safety",
    "VP Safety Assessment",
    "Senior Scientist, Toxicology",
    "Principal Investigator",
    "Research Scientist",
    "Postdoc Researcher",
    "Lab Manager",
    "Director of Oncology", 
    "Head of Oncology Research"
]


COMPANIES = {
    "Pfizer": "New York, NY",
    "Novartis": "Basel, Switzerland",
    "Roche": "Basel, Switzerland", 
    "Merck": "Rahway, NJ",
    "AstraZeneca": "Cambridge, UK",
    "GSK": "London, UK",
    "Vertex Pharmaceuticals": "Boston, MA",
    "Moderna": "Cambridge, MA", 
    "Biogen": "Cambridge, MA",
    "Gilead Sciences": "Foster City, CA",
    "Nexus Bio": "San Francisco, CA", 
    "Apex Therapeutics": "San Diego, CA",
    "GeneSys Labs": "Boston, MA",
    "Cellular Dynamics": "Madison, WI"
}

PERSON_LOCATIONS = [
    "Boston, MA", "Cambridge, MA", "San Francisco, CA", "San Diego, CA",
    "Basel, Switzerland", "London, UK", "Research Triangle Park, NC",
    "Seattle, WA", "Austin, TX", "Denver, CO", "Remote (Colorado)", "Remote (Florida)"
]

def generate_leads(num_leads=50):
    """
    Generates a DataFrame of synthetic leads for the Lead Finder Tool.
    """
    leads = []
    
    for _ in range(num_leads):
        role = random.choice(ROLES)
        company_name = random.choice(list(COMPANIES.keys()))
        company_hq = COMPANIES[company_name]
        
        # 20% chance of being remote/different from HQ
        if random.random() < 0.2:
            person_location = random.choice(PERSON_LOCATIONS)
        else:
            person_location = company_hq
        
        # Correlate funding with company size/name slightly for realism
        if company_name in ["Pfizer", "Novartis", "Roche", "Merck", "AstraZeneca", "GSK"]:
            funding = "Public"
        else:
            funding = random.choice(["Series A", "Series B", "Series C", "Public", "Grant Funded"])

        # Random boolean signals
        has_published = random.random() > 0.6  # 40% chance
        uses_invitro = random.random() > 0.5   # 50% chance
        
        # Create lead object
        lead = {
            "Name": fake.name(),
            "Role": role,
            "Company": company_name,
            "Company_HQ": company_hq,
            "Person_Location": person_location,
            "Email": f"{fake.first_name().lower()}.{fake.last_name().lower()}@{company_name.replace(' ', '').lower()}.com",
            "Funding_Status": funding,
            "Has_Published_Recently": has_published,
            "Uses_InVitro_Models": uses_invitro,
            "LinkedIn_Profile": f"linkedin.com/in/{fake.slug()}",
            "Last_Active": f"{random.randint(1, 30)} days ago"
        }
        leads.append(lead)
        
    return pd.DataFrame(leads)

if __name__ == "__main__":
    df = generate_leads(5)
    print(df.head())
