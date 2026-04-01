import streamlit as st
from matcher import run_matcher

# ── PAGE SETUP ──────────────────────────────────────
# This configures the browser tab and page layout
st.set_page_config(
    page_title="Clinical Trial Matcher",
    page_icon="🏥",
    layout="wide"
)

# ── HEADER ──────────────────────────────────────────
st.title("🏥 Clinical Trial Matcher")
st.markdown("""
Find relevant clinical trials for any medical condition instantly.
Data sourced from **clinicaltrials.gov** — updated in real time.
""")

st.divider()

# ── INPUT SECTION ───────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    # text input where doctor types patient condition
    patient_condition = st.text_input(
        "Enter patient condition:",
        placeholder="e.g. Type 2 diabetes, breast cancer, hypertension..."
    )

with col2:
    # number selector for how many trials to fetch
    max_results = st.selectbox(
        "Number of trials:",
        options=[5, 10, 15, 20],
        index=1
    )

# search button
search_clicked = st.button("🔍 Find Matching Trials", type="primary")

# ── RESULTS SECTION ─────────────────────────────────
if search_clicked:

    # check if user typed something
    if not patient_condition:
        st.warning("Please enter a patient condition first.")

    else:
        # show spinner while processing
        with st.spinner("Searching clinical trials and analyzing matches..."):
            trials_info, ai_analysis = run_matcher(patient_condition)

        if trials_info is None:
            st.error("No trials found. Try a different condition.")

        else:
            # ── AI ANALYSIS ─────────────────────────────
            st.subheader("🤖 AI Match Analysis")
            st.markdown(ai_analysis)

            st.divider()

            # ── RAW TRIAL DATA ──────────────────────────
            st.subheader(f"📋 All Fetched Trials ({len(trials_info)} found)")

            # show each trial in an expandable card
            for i, trial in enumerate(trials_info):
                with st.expander(f"Trial {i+1}: {trial['title']}"):

                    # status badge
                    if trial['status'] == 'RECRUITING':
                        st.success(f"Status: {trial['status']}")
                    else:
                        st.info(f"Status: {trial['status']}")

                    st.markdown(f"**Trial ID:** {trial['id']}")
                    st.markdown(f"**Summary:** {trial['summary'][:500]}")
                    st.markdown(f"**Eligibility:** {trial['eligibility'][:500]}")
                    st.markdown(f"**More info:** [{trial['url']}]({trial['url']})")

            st.divider()

            # ── DISCLAIMER ──────────────────────────────
            st.caption("""
            ⚠️ This tool is for informational purposes only.
            Always consult a qualified healthcare professional
            before enrolling in any clinical trial.
            """)

# ── SIDEBAR ─────────────────────────────────────────
with st.sidebar:
    st.header("ℹ️ How to Use")
    st.markdown("""
    1. Enter a medical condition
    2. Select number of trials
    3. Click **Find Matching Trials**
    4. Review AI analysis
    5. Click any trial to expand details
    """)

    st.divider()

    st.header("💡 Example Conditions")
    examples = [
        "Type 2 diabetes",
        "Breast cancer",
        "Hypertension",
        "Alzheimer's disease",
        "COVID-19",
        "Heart failure"
    ]

    # clicking an example fills the search box
    for example in examples:
        if st.button(example):
            st.session_state.condition = example