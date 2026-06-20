from ai.candidate_parser import CandidateParser

parser = CandidateParser()

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

candidate = parser.parse_candidate(
    resume
)

print(candidate)