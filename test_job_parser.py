from ai.job_parser import JobParser

parser = JobParser()

job_description = """
Senior Python Developer

Requirements:
- Python
- FastAPI
- Docker
- AWS
- PostgreSQL
- 5 years experience
- Bachelor's Degree

Location:
Remote

Salary:
4000 USD
"""

result = parser.parse_job_description(job_description)

print(result)