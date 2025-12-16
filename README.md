# Biotech Lead Qualification Engine

A smart lead generation and scoring tool designed for Business Development teams selling 3D In-Vitro Therapy Models.

This application simulates an AI agent that crawls finding key buyer personas (e.g., Directors of Toxicology), enriches their profiles with high-value signals (Fundraising, Recent Publications), and ranks them by their Propensity to Buy.

## Key Features

*   **Smart Scoring Engine**: Ranks leads from 0-100 based on weighted signals:
    *   **Role Fit (+30)**: Prioritizes decision-makers (Directors, VPs).
    *   **Scientific Intent (+40)**: High score for researchers publishing relevant papers (e.g., Liver Toxicity) in the last 2 years.
    *   **Funding Power (+20)**: Highlights companies with recent Series A/B funding.
    *   **Technographics (+15)**: Identifies teams already using in-vitro models.
    *   **Ecosystem (+10)**: Targets key biotech hubs (Boston, Basel, SF).
*   **Location Intelligence**: Distinguishes between Person Location (Remote) and Company HQ (Hubs).
*   **Search & Filters**: Instantly filter by Oncology, specific locations (e.g., Boston), or specific companies (e.g., Pfizer).
*   **Data Export**: One-click download of your qualified lead list to CSV.

## Tech Stack

*   **Python 3**
*   **Streamlit** (Frontend/Dashboard)
*   **Pandas** (Data Processing)
*   **Faker** (Synthetic Data Generation)

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/manasi582/biotech_lead_engine.git
    cd biotech_lead_engine
    ```

2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the dashboard locally:

```bash
streamlit run app.py
```

1.  **Generate Leads**: Click the "Find & Score Leads" button in the sidebar to simulate a live crawl.
2.  **Filter**: Use the sidebar to set a minimum score threshold.
3.  **Search**: Type "Oncology" or "Boston" in the search bar.
4.  **Analyze**: Sort the table by Rank or Probability.
5.  **Export**: Download the list for outreach.

## Project Structure

```
├── app.py                 # Main Streamlit Dashboard application
├── requirements.txt       # Project dependencies
├── src/
│   ├── data_generator.py  # Simulates identifying & enriching leads
│   └── scoring_engine.py  # Algorithms calculating Propensity to Buy
└── README.md              # Documentation
```

## The Logic Behind the Score

The "Propensity to Buy" model transforms raw data into actionable intelligence:

| Signal | Logic | Weight |
| :--- | :--- | :--- |
| **Role Fit** | Title contains "Director", "Head", "VP" | +30 |
| **Scientific Intent** | Published relevant paper < 2 years | +40 |
| **Funding** | Series A / B / Public Co | +20 |
| **Technographics** | Already uses in-vitro models | +15 |
| **Location** | Company HQ in Biotech Hub | +10 |

---
*Note: This project uses simulated data for demonstration purposes.*
