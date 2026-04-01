# 🏥 Clinical Trial Matcher

AI-powered tool that instantly matches patient conditions to relevant 
clinical trials from clinicaltrials.gov.

## 🚀 Live Demo
👉 [Try it here](https://clinical-trial-matcher-ut8jeazvrng3ewb8dzhe2z.streamlit.app/)

## The Problem
Doctors spend hours manually searching clinicaltrials.gov to find 
trials for their patients. This tool automates that process using AI 
— reducing search time from hours to seconds.

## How It Works
1. Enter any medical condition
2. App fetches real-time recruiting trials from clinicaltrials.gov
3. LLaMA 3.3 70B analyzes all trials
4. Returns top 3 matches with eligibility explanation
5. All trials shown as expandable cards with direct links

## Tech Stack
- **Streamlit** — web interface
- **LangChain + Groq** — AI analysis
- **LLaMA 3.3 70B** — matching intelligence
- **clinicaltrials.gov API** — real-time trial data
- **Python** — backend logic

## Setup
```bash
pip install streamlit langchain-groq langchain-core requests python-dotenv
```

Create `.env` file:
```
GROQ_API_KEY=your_key_here
```

Run locally:
```bash
streamlit run app.py
```

## Example
```
Input:  "breast cancer"
Output: Top 3 matching recruiting trials with:
        - Trial ID and title
        - Why it matches
        - Key eligibility requirements
        - Direct link to trial
```

## Real World Impact
- Reduces manual trial search from hours to seconds
- Surfaces trials doctors might have missed
- Directly applicable to healthcare systems like IU Health

## Disclaimer
⚠️ For informational purposes only. Always consult a qualified 
healthcare professional before enrolling in any clinical trial.
