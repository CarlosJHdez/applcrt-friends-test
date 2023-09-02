import bisect

class Company:
    """A company is a list of start job days with the people that started on that day."""
    def __init__(self, name):
        self.name = name
        self.job_starts = []  # Initialize an empty list for start job dates

    def add_job_start(self, job_start_date, person):
        numeric_date = job_start_date.toordinal()

        # Use bisect.insort to insert the date in the correct position
        bisect.insort_left(self.job_starts, (numeric_date, person))

    def get_job_starts(self):
        return [(date.fromordinal(numeric_date), person) for numeric_date, person in self.job_starts]

# Example usage:
from datetime import date

company1 = Company("OrangeCorp")
company1.add_job_start(date(2023, 1, 15), "Alice")
company1.add_job_start(date(2023, 2, 5), "Bob")
company1.add_job_start(date(2023, 3, 10), "Charlie")
company1.add_job_start(date(2023, 1, 15), "David")

# Get the ordered list of job start dates and associated people
job_starts = company1.get_job_starts()

# Iterate through the job starts in order
for job_start_date, person in job_starts:
    print(f"Date: {job_start_date}, Person: {person}")