from ai.candidate_parser import CandidateParser
from ai.candidate_scorer import CandidateScorer
from ai.job_parser import JobParser


candidate_parser = CandidateParser()
job_parser = JobParser()
scorer = CandidateScorer()


resume = """
John Doe

Python Developer

5 years experience

Python

FastAPI

Docker

AWS

john@gmail.com
"""


job = """
Senior Python Developer

Requirements

Python

FastAPI

Docker

AWS

5 years experience

Bachelor Degree

Remote

Salary 4000 USD
"""


candidate = candidate_parser.parse_candidate(
    resume
)

job = job_parser.parse_job_description(
    job
)

score = scorer.score_candidate(
    candidate,
    job
)

print(score)