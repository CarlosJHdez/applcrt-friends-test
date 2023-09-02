# I wrote this code using chatgpt. Is the second version of the code.
# I did not add any error handling at first nor any unit testing.
# the second version took about 120 minutes to write and debug with the example1.json file.
# i used bisect because I have a structure in mind for part 2 but wanted to keep it simple at first.
# if the number of persons is P and the total number of experiences is E, 
# the time complexity is O(P+E) and memory size is proportional to P+2E+C.
import json
import bisect
import datetime
        

class Company:
    """ A company is a list of the people that had experiences at that company.
    """
    def __init__(self, name):
        self.name = name
        self.experiences = []  # Initialize an empty list for people experiences
    
    def add_experience(self, experience):
        # Use bisect.insort to insert the experience in the correct date order
        bisect.insort_left(self.experiences, experience)

    def __str__(self) -> str:
        return f"{self.name}"
class Person:
    def __init__(self, id, first, last, phone):
        self.id = id
        self.first = first
        self.last = last
        self.phone = phone
        self.experience = []
    
    def add_experience(self, experience):
        self.experience.append(experience)
        
    def __str__(self) -> str:
        return f"{self.first} {self.last}"

class Experience:
    """ An Experience is a period (posibly still ongoing) where a person worked for a company.
    """
    def __init__(self, person:Person, company:Company, title, start, end):
        self.person = person
        self.company = company
        self.title = title
        self.start = datetime.date.fromisoformat(start).toordinal() # convert to ordinal date
        if end is not None:
            self.end = datetime.date.fromisoformat(end).toordinal() # convert to ordinal date  
        else:
            self.end = None  
            
    def __lt__(self, other):
        """Comparison method to compare experiences based on start dates."""
        if not isinstance(other, Experience):
            raise ValueError("Comparison with non-Experiences object is not supported.")
        return self.start < other.start
    
    def __str__(self) -> str:
        if self.end is None:
            end = "ongoing"
        else:
            end = datetime.date.fromordinal(self.end)
        return f"{self.person} is {self.title} @ {self.company} starting {datetime.date.fromordinal(self.start)}, End: {end}"


            
def load_person_records_from_json_file(file_path):
    people = []
    companies = {}

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for person_data in data:
            person = Person(
                id=person_data['id'],
                first=person_data['first'],
                last=person_data['last'],
                phone=person_data['phone'],
            )
            for experience in person_data['experience']:
                company_name = experience['company']
                if company_name not in companies:
                    company = Company(company_name)
                    companies[company_name] = company
                else:
                    company = companies[company_name]
                experience = Experience(person, company, title=experience['title'], start=experience['start'], end=experience['end'])
                person.add_experience(experience)
                company.add_experience(experience)
            people.append(person)

    return people, companies

# Example usage:
file_path = 'example-1.json'  # Replace with the path to your JSON file
persons, companies = load_person_records_from_json_file(file_path)

# Iterate through the persons in order
for person in persons:
    print(f"Person: {person.first} {person.last}, Phone: {person.phone}")
    for experience in person.experience:
        print(experience)
    
for company in companies:
    print(f"Company: {company}")
    for experience in companies[company].experiences:
        print(experience)
    
