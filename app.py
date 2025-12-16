import streamlit as st
import pandas as pd
from src.data_generator import generate_leads
from src.scoring_engine import ScoringEngine

# Page Config
st.set_page_config(
    page_title="Lead Finder Tool",
    page_icon="None",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and Description
st.title("3D In-Vitro Therapy Models - Lead Qualification Engine")
st.markdown("""
    **Propensity to Buy Scoring System**
    
    This tool identifies and ranks potential biotech researchers based on their likelihood to adopt 3D in-vitro models.
    *Scores are based on Role Fit, Scientific Intent (Publications), Funding Status, Technographics, and Location.*
""")

# Sidebar Controls
st.sidebar.header("Configuration")
num_leads = st.sidebar.slider("Number of Prospects to Find", 10, 200, 50)

if st.sidebar.button("Find & Score Leads"):
    with st.spinner("Simulating data retrieval from LinkedIn, PubMed, and Crunchbase..."):
        # 1. Identification
        raw_leads = generate_leads(num_leads)
        
        # 2. Enrichment & Scoring
        engine = ScoringEngine()
        scored_leads = engine.score_leads(raw_leads)
        
        st.session_state['leads'] = scored_leads
        st.success(f"Found and scored {len(scored_leads)} high-potential leads!")

# Display Logic
if 'leads' in st.session_state:
    df = st.session_state['leads']
    
    # filters
    st.sidebar.subheader("Filters")
    search_query = st.sidebar.text_input("Search (Name, Role, Company)")
    min_score = st.sidebar.slider("Minimum Propensity Score", 0, 100, 50)
    
    # Apply filters
    filtered_df = df[df["Propensity_Score"] >= min_score]
    
    if search_query:
        search_query = search_query.lower()
        filtered_df = filtered_df[
            filtered_df["Name"].str.lower().str.contains(search_query, na=False) |
            filtered_df["Role"].str.lower().str.contains(search_query, na=False) |
            filtered_df["Company"].str.lower().str.contains(search_query, na=False) |
            filtered_df["Person_Location"].str.lower().str.contains(search_query, na=False) |
            filtered_df["Company_HQ"].str.lower().str.contains(search_query, na=False)
        ]
        
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Qualified Leads", len(filtered_df))
    col2.metric("Avg Propensity Score", f"{filtered_df['Propensity_Score'].mean():.1f}" if not filtered_df.empty else "0")
    
    # Main Table
    st.subheader("Lead Dashboard")
    
    if not filtered_df.empty:
        # Prepare display dataframe
        display_df = filtered_df.copy()
        
        # Add "Action" column simulation (Streamlit dataframe doesn't support button clicks inside easily, giving a visual indicator)
        display_df["Action"] = "Email / Connect"
        
        # Reorder columns as requested
        cols = ["Rank", "Propensity_Score", "Name", "Title", "Company", "Person_Location", "Company_HQ", "Email", "Action"]
        
        # Rename Role to Title for consistency with prompt
        display_df = display_df.rename(columns={"Role": "Title"})
        
        # Select and show
        st.dataframe(
            display_df[cols],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No leads match your filter criteria.")
    
    # Export
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Leads as CSV",
        data=csv,
        file_name='qualified_leads.csv',
        mime='text/csv',
    )
    
    # Scoring Breakdown (Educational)
    with st.expander("How the Propensity Score is Calculated"):
        st.markdown("""
        The score (0-100) is a weighted sum of the following signals:
        - **+30 points**: Role Fit (Director, Head, VP)
        - **+40 points**: Scientific Intent (Published relevant paper in last 2 years)
        - **+20 points**: High-growth Funding (Series A/B)
        - **+15 points**: Already using In-Vitro models
        - **+10 points**: Located in key biotech hub (Boston, Basel, SF)
        
        *Scores are capped at 100.*
        """)

else:
    st.info("Click **Find & Score Leads** in the sidebar to start the engine.")

