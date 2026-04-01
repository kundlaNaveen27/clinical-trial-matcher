import os
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# Connect to Groq AI
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)


def fetch_trials(condition, max_results=10):
    """
    Fetches clinical trials from clinicaltrials.gov API
    """
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.cond": condition,
        "filter.overallStatus": "RECRUITING",
        "pageSize": max_results,
        "format": "json"
    }

    print(f"Fetching trials for: {condition}")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"API Error: {response.status_code}")
        return []

    data = response.json()
    studies = data.get("studies", [])
    print(f"Found {len(studies)} trials")
    return studies


def extract_trial_info(study):
    """
    Extracts useful parts from raw API data
    """
    protocol = study.get("protocolSection", {})
    identification = protocol.get("identificationModule", {})
    status = protocol.get("statusModule", {})
    description = protocol.get("descriptionModule", {})
    eligibility = protocol.get("eligibilityModule", {})

    return {
        "id": identification.get("nctId", "Unknown"),
        "title": identification.get("briefTitle", "No title"),
        "status": status.get("overallStatus", "Unknown"),
        "summary": description.get("briefSummary", "No summary"),
        "eligibility": eligibility.get("eligibilityCriteria", "Not specified"),
        "url": f"https://clinicaltrials.gov/study/{identification.get('nctId', '')}"
    }


def match_trials(patient_condition, trials_info):
    """
    Uses AI to match patient condition to relevant trials
    """
    trials_text = ""
    for i, trial in enumerate(trials_info):
        trials_text += f"""
Trial {i+1}:
ID: {trial['id']}
Title: {trial['title']}
Summary: {trial['summary'][:300]}
Eligibility: {trial['eligibility'][:300]}
URL: {trial['url']}
---"""

    messages = [
        SystemMessage(content="""You are a clinical trial matching assistant.
        Given a patient's condition, analyze the provided trials and:
        1. Identify the TOP 3 most relevant trials
        2. Explain WHY each trial matches the patient's condition
        3. Highlight key eligibility requirements
        4. Be concise and medically precise
        Format your response clearly with trial numbers."""),

        HumanMessage(content=f"""
Patient condition: {patient_condition}

Available trials:
{trials_text}

Please identify the top 3 matching trials and explain why they match.""")
    ]

    response = llm.invoke(messages)
    return response.content


def run_matcher(patient_condition, max_results=10):
    """
    Main function — fetches trials and finds matches
    """
    # step 1 — fetch trials from API
    studies = fetch_trials(patient_condition, max_results)

    if not studies:
        return None, "No trials found for this condition."

    # step 2 — extract clean info
    trials_info = [extract_trial_info(study) for study in studies]

    # step 3 — AI matching
    ai_analysis = match_trials(patient_condition, trials_info)

    return trials_info, ai_analysis