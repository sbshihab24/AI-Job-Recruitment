# AI Recruitment

AI Recruitment is a Streamlit application that imports a candidate resume, parses a job description, compares the candidate with the role, and produces a structured score and recruiter-facing explanation using OpenAI.

## Main Features

- Upload candidate CVs in PDF, DOCX, CSV, XLSX, or XLS format.
- Upload a job description in PDF, DOCX, or TXT format.
- Paste a job description directly into the dashboard.
- Extract structured candidate and job information with Pydantic models.
- Score skills, experience, education, salary, location, languages, and certifications.
- Generate strengths, missing requirements, red flags, recruiter summaries, and recommended actions.
- Download candidate, job, score, and explanation results as JSON.

## Application Flow

```text
Candidate file --> File reader --> CandidateParser --+
                                                     +--> CandidateScorer
Job file/text ------------------> JobParser ----------+          |
                                                               v
                                                    CandidateExplainer
                                                               |
                                                               v
                                                    Streamlit dashboard
```

The OpenAI Responses API is used with Pydantic schemas so each AI step returns structured data.

## Project Structure

```text
.
|-- ai/
|   |-- candidate_import.py       # Routes candidate files to readers
|   |-- candidate_parser.py       # Converts resume text into CandidateProfile
|   |-- job_parser.py             # Converts job text into JobDescription
|   |-- candidate_scorer.py       # Scores candidate against job requirements
|   |-- candidate_explainer.py    # Produces detailed recruiter explanations
|   |-- clients/
|   |   `-- openai_client.py      # Cached OpenAI client
|   |-- models/                   # Pydantic output schemas
|   |-- prompts/                  # AI system prompts
|   |-- readers/                  # PDF, DOCX, CSV, ATS, LinkedIn, and email readers
|   |-- config.py                 # Environment-based application settings
|   `-- utils.py                  # File and JSON utilities
|-- streamlit_app/
|   `-- app.py                    # Web dashboard
|-- test_candidate_parser.py      # Candidate parser smoke script
|-- test_job_parser.py            # Job parser smoke script
|-- test_candidate_scorer.py      # End-to-end scoring smoke script
|-- test_openai.py                # OpenAI client smoke script
`-- requirements.txt
```

## Requirements

- Python 3.10 or newer
- An OpenAI API key
- Internet access for OpenAI API requests

The repository was syntax-checked with Python 3.13.5.

## Installation

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1
TEMPERATURE=0
MAX_TOKENS=4000
APP_NAME=AI Recruitment
APP_VERSION=1.0.0
DEBUG=true
OUTPUT_FOLDER=outputs
TEMP_FOLDER=temp
LOG_FOLDER=logs
```

Only `OPENAI_API_KEY` is required. The remaining variables have defaults in `ai/config.py`.

## Run the Dashboard

From the project root:

```powershell
python -m streamlit run streamlit_app/app.py
```

Then open the local address printed by Streamlit, normally:

```text
http://localhost:8501
```

## Using the Application

1. Upload a candidate CV.
2. Upload or paste a job description.
3. Select **Analyze Candidate**.
4. Review the candidate profile, parsed job, score, and explanation tabs.
5. Download the generated JSON files if needed.

Each analysis currently makes four OpenAI requests:

1. Parse the candidate.
2. Parse the job description.
3. Score the candidate.
4. Generate the explanation.

## Output Models

### CandidateProfile

Contains contact information, current role, experience, salary expectations, skills, languages, certifications, employment history, education, and parsing metadata.

### JobDescription

Contains job details, experience and salary ranges, required and preferred skills, education, responsibilities, requirements, benefits, and parsing metadata.

### CandidateScore

Contains an overall score, fit category, AI confidence, category-level match scores, strengths, missing requirements, red flags, recruiter summary, and next action.

### AIExplanation

Expands the score into recruiter-readable reasoning for each matching category and an overall recommendation.

## Supported Import Sources

The reader layer supports:

- PDF and DOCX resume text extraction
- CSV files
- RecruitCRM CSV/Excel exports
- Bullhorn CSV/Excel exports
- LinkedIn profile PDF exports
- PDF/DOCX email attachments
- Manual candidate dictionaries through `import_manual_candidate`

## Current Limitations and Risks

The following issues were found during project review:

- `parser_prompt.txt` only describes job extraction, but it is also used by `CandidateParser`. A dedicated candidate prompt should be added.
- The dashboard accepts XLSX and XLS candidate files, but `import_candidate` does not route those extensions.
- CSV and Excel readers return a `pandas.DataFrame`, while `CandidateParser.parse_candidate` expects a string. These formats require row selection or conversion before parsing.
- Uploaded files are saved in `outputs/` and are not automatically deleted.
- There is no `.gitignore`. The current repository includes `.env`, generated PDFs, virtual-environment files, and Python cache files in Git staging. API keys and candidate data must not be committed.
- The root test files are executable smoke scripts rather than isolated automated tests. They make real API calls and may incur cost.
- AI calls do not currently have application-level retry handling, timeout messages, or user-friendly exception handling.
- The configured `temperature` and `max_tokens` settings are not passed to the OpenAI requests.
- Some dashboard emoji text appears to have character-encoding corruption.
- Candidate scoring is AI-generated and should support recruiter decisions, not make final employment decisions automatically.

## Recommended Next Improvements

1. Add `.gitignore` and remove secrets, uploaded CVs, caches, and `venv` from version control.
2. Add a candidate-specific parsing prompt.
3. Normalize every supported import source into candidate text or structured candidate records.
4. Add robust Streamlit error handling and delete temporary uploads after analysis.
5. Replace smoke scripts with mocked `pytest` tests.
6. Add deterministic scoring rules or configurable weighting alongside the AI evaluation.
7. Add logging, request tracing, cost controls, and batch-candidate processing.
8. Add privacy controls and a candidate-data retention policy.

## Security and Privacy

Resumes contain personally identifiable information. Before production use:

- Never commit `.env` or uploaded candidate files.
- Rotate the OpenAI API key if it has ever been committed or shared.
- Restrict access to uploaded and generated files.
- Define data retention and deletion rules.
- Inform users when candidate information is sent to an external AI provider.
- Require human review of every hiring recommendation.

## Validation Performed

The Python source was checked with:

```powershell
python -m compileall ai streamlit_app
```

The source compiled successfully. Live OpenAI integration tests were not run because they require network access, a valid API key, and may incur API charges.
