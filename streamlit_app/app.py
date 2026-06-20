import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from ai.candidate_import import import_candidate
from ai.candidate_parser import CandidateParser
from ai.job_parser import JobParser
from ai.candidate_scorer import CandidateScorer
from ai.candidate_explainer import CandidateExplainer

from ai.readers.pdf_reader import read_pdf
from ai.readers.docx_reader import read_docx

from ai.utils import save_uploaded_file


st.set_page_config(
    page_title="AI Recruitment Dashboard",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Recruitment Dashboard")

st.markdown("---")


# -----------------------------
# Session State
# -----------------------------

DEFAULT_KEYS = [
    "candidate",
    "job",
    "score",
    "explanation",
]

for key in DEFAULT_KEYS:
    if key not in st.session_state:
        st.session_state[key] = None


# -----------------------------
# Upload Section
# -----------------------------

left, right = st.columns(2)

with left:

    st.subheader("Candidate CV")

    candidate_file = st.file_uploader(
        "Upload Candidate CV",
        type=[
            "pdf",
            "docx",
            "csv",
            "xlsx",
            "xls",
        ],
    )


with right:

    st.subheader("Job Description")

    job_file = st.file_uploader(
        "Upload Job Description",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
    )

    job_text = st.text_area(
        "Or Paste Job Description",
        height=250,
    )


st.markdown("---")

analyze = st.button(
    "🚀 Analyze Candidate",
    use_container_width=True,
)


# -----------------------------
# AI Pipeline
# -----------------------------

if analyze:

    if candidate_file is None:
        st.error("Please upload a Candidate CV.")
        st.stop()

    candidate_path = save_uploaded_file(
        candidate_file,
        "outputs",
    )

    candidate_source = candidate_path.suffix.replace(".", "")

    candidate_text = import_candidate(
        candidate_path,
        candidate_source,
    )

    if job_file is not None:

        job_path = save_uploaded_file(
            job_file,
            "outputs",
        )

        extension = job_path.suffix.lower()

        if extension == ".pdf":
            job_text = read_pdf(job_path)

        elif extension == ".docx":
            job_text = read_docx(job_path)

        elif extension == ".txt":

            with open(
                job_path,
                "r",
                encoding="utf-8",
            ) as file:

                job_text = file.read()

    if not job_text.strip():

        st.error(
            "Please upload or paste a Job Description."
        )

        st.stop()

    with st.spinner("Parsing Candidate..."):

        candidate = CandidateParser().parse_candidate(
            candidate_text
        )

    with st.spinner("Parsing Job Description..."):

        job = JobParser().parse_job_description(
            job_text
        )

    with st.spinner("Scoring Candidate..."):

        score = CandidateScorer().score_candidate(
            candidate,
            job,
        )

    with st.spinner("Generating AI Explanation..."):

        explanation = CandidateExplainer().generate_explanation(
            score
        )

    st.session_state["candidate"] = candidate
    st.session_state["job"] = job
    st.session_state["score"] = score
    st.session_state["explanation"] = explanation

    st.success("Analysis Completed Successfully!")


    # -----------------------------
# Show Results
# -----------------------------

if st.session_state["candidate"] is not None:

    candidate = st.session_state["candidate"]
    job = st.session_state["job"]
    score = st.session_state["score"]
    explanation = st.session_state["explanation"]

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "👤 Candidate",
            "💼 Job",
            "📊 AI Score",
            "🧠 AI Explanation",
        ]
    )

    # ---------------------------------
    # Candidate
    # ---------------------------------

    with tab1:

        st.subheader("Candidate Profile")

        st.json(
            candidate.model_dump()
        )

    # ---------------------------------
    # Job
    # ---------------------------------

    with tab2:

        st.subheader("Job Description")

        st.json(
            job.model_dump()
        )

    # ---------------------------------
    # Score
    # ---------------------------------

    with tab3:

        st.subheader("AI Candidate Score")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Overall Score",
            f"{score.overall_score:.1f}"
        )

        c2.metric(
            "Fit Category",
            str(score.fit_category)
        )

        c3.metric(
            "AI Confidence",
            f"{score.ai_confidence:.1f}%"
        )

        st.divider()

        st.subheader("Matching Details")

        metrics = [
            ("Skills Match", score.skills_match),
            ("Experience Match", score.experience_match),
            ("Education Match", score.education_match),
            ("Salary Alignment", score.salary_alignment),
            ("Location Alignment", score.location_alignment),
            ("Language Match", score.language_match),
            ("Certification Match", score.certification_match),
        ]

        for title, item in metrics:

            icon = "✅" if item.matched else "❌"

            with st.expander(
                f"{icon} {title}"
            ):

                st.write(
                    f"**Score:** {item.score}%"
                )

                st.write(
                    f"**Reason:** {item.reason}"
                )

        st.divider()

        st.subheader("Recruiter Summary")

        st.info(
            score.recruiter_summary
        )

        st.success(
            score.recommended_next_action
        )

    # ---------------------------------
    # Explanation
    # ---------------------------------

    with tab4:

        st.subheader("AI Explanation")

        st.write("### Key Strengths")

        if explanation.key_strengths:

            for item in explanation.key_strengths:
                st.success(item)

        else:

            st.info("No strengths available.")

        st.write("### Missing Requirements")

        if explanation.missing_requirements:

            for item in explanation.missing_requirements:
                st.warning(item)

        else:

            st.success("None")

        st.write("### Red Flags")

        if explanation.red_flags:

            for item in explanation.red_flags:
                st.error(item)

        else:

            st.success("None")

        st.write("### Recruiter Summary")

        st.info(
            explanation.recruiter_summary
        )

        st.write("### Overall Reasoning")

        st.write(
            explanation.overall_reasoning
        )



        # ---------------------------------
# Download Section
# ---------------------------------

    st.markdown("---")

    st.subheader("Download Results")

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="⬇ Download Candidate JSON",
            data=candidate.model_dump_json(indent=4),
            file_name="candidate.json",
            mime="application/json",
            use_container_width=True,
        )

        st.download_button(
            label="⬇ Download Job JSON",
            data=job.model_dump_json(indent=4),
            file_name="job_description.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:

        st.download_button(
            label="⬇ Download Score JSON",
            data=score.model_dump_json(indent=4),
            file_name="candidate_score.json",
            mime="application/json",
            use_container_width=True,
        )

        st.download_button(
            label="⬇ Download Explanation JSON",
            data=explanation.model_dump_json(indent=4),
            file_name="candidate_explanation.json",
            mime="application/json",
            use_container_width=True,
        )

else:

    st.info(
        """
Upload a Candidate CV and a Job Description,
then click **Analyze Candidate** to begin the AI analysis.
        """
    )