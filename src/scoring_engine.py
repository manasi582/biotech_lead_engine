import pandas as pd

class ScoringEngine:
    def __init__(self):
        # Configuration for scoring weights
        self.weights = {
            "ROLE_FIT": 30,
            "SCIENTIFIC_INTENT": 40,
            "FUNDING": 20,
            "TECHNOGRAPHICS": 15,
            "LOCATION": 10
        }
        
    def calculate_score(self, lead):
        """
        Calculates the Propensity to Buy score for a single lead.
        """
        score = 0
        
        # 1. Role Fit
        role = lead.get("Role", "")
        if any(keyword in role for keyword in ["Director", "Head", "VP"]):
            score += self.weights["ROLE_FIT"]
        elif "Senior Scientist" in role or "Principal Investigator" in role:
            score += 20 # Partial score
            
        # 2. Scientific Intent
        if lead.get("Has_Published_Recently", False):
            score += self.weights["SCIENTIFIC_INTENT"]
            
        # 3. Funding Status
        funding = lead.get("Funding_Status", "")
        if funding in ["Series A", "Series B", "Public"]:
            score += self.weights["FUNDING"]
        elif funding == "Series C":
            score += 15 # Slightly less urgent/agile?
        elif funding == "Grant Funded":
            score += 10
            
        # 4. Technographics
        if lead.get("Uses_InVitro_Models", False):
            score += self.weights["TECHNOGRAPHICS"]
            
        # 5. Location (Hubs)
        # Using Company HQ as the primary indicator for "Hub" status (funding/ecosystem)
        hq = lead.get("Company_HQ", "")
        person_loc = lead.get("Person_Location", "")
        
        hubs = ["Boston, MA", "Cambridge, MA", "San Francisco, CA", "Basel, Switzerland", "Cambridge, UK", "London, UK", "San Diego, CA"]
        
        if any(hub in hq for hub in hubs):
            score += self.weights["LOCATION"]
        
        # Small bonus if person is also in a hub (easier for meetings)
        if any(hub in person_loc for hub in hubs):
            score += 5
            
        return min(score, 100) # Cap at 100

    def score_leads(self, df):
        """
        Applies scoring to a DataFrame of leads.
        """
        # Create a copy to avoid SettingWithCopy warnings
        scored_df = df.copy()
        
        # Apply the scoring function row by row
        scored_df["Propensity_Score"] = scored_df.apply(lambda row: self.calculate_score(row), axis=1)
        
        # Rank by score
        scored_df = scored_df.sort_values(by="Propensity_Score", ascending=False)
        scored_df.reset_index(drop=True, inplace=True)
        scored_df["Rank"] = scored_df.index + 1
        
        return scored_df

if __name__ == "__main__":
    # Test the engine
    from data_generator import generate_leads
    
    print("Generating leads...")
    df = generate_leads(10)
    
    print("Scoring leads...")
    engine = ScoringEngine()
    scored = engine.score_leads(df)
    
    print(scored[["Name", "Role", "Funding_Status", "Propensity_Score", "Rank"]].head())
