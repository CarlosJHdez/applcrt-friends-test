# Description: 
# Read a json file that contains people, and its jobs at various companies.
# Organize it in a way that is easy to find people related to each other because:
# - They worked at the same company for a minimum period of 90 days.
import json
import bisect
import datetime
        
COLLEAGUE_LIMIT = 90  # Minimum number of days to be considered a colleague

class Company:
    """ A company is a list of the people that had experiences at that company.
    """
    def __init__(self, name):
        self.name = name
        self.experiences = []  # Initialize an empty list for people experiences
    
    def add_experience(self, experience):
        """Add the experience of a person to the company.
        The complexity of this function is O(log(E)) where E is the number of experiences.
        """
        # Use bisect.insort to insert the experience in the correct date order
        bisect.insort_left(self.experiences, experience)

    def __str__(self) -> str:
        return f"{self.name}"
    
    def colleagues(self, target, min_days):
        """Returns a list of people that worked at the same company as this person for at least 90 days.
        The complexity of this function is O(Ec) where Ec is the number of experiences in company c.
        """
        colleagues = set()
        if target.end and (target.end - target.start) < min_days:
            # No colleagues if the target experience is less than min_days.
            return colleagues
        
        for other in self.experiences:
            if other != target: # Do not compare with itself!
                if target.overlaps_at_least(other, min_days):
                    colleagues.add(other.person.id)
        return colleagues
    
class Person:
    def __init__(self, id, first, last, phone):
        self.id = id
        self.first = first
        self.last = last
        self.phone = phone
        self.experience = []
    
    def add_experience(self, experience):
        self.experience.append(experience)
        
    def companies_worked_for(self):
        """Returns a list of companies that this person worked for."""
        companies = set()
        for experience in self.experience:
            companies.add(experience.company)
        return companies
        
    def __str__(self) -> str:
        return f"{self.first} {self.last}"

class Experience:
    """ An Experience is a period (posibly still ongoing) where a person worked for a company.
    """
    def __init__(self, person:Person, company, title, start, end):
        self.person = person
        self.company = company
        self.title = title
        # convert to ordinal date to facilitate comparisons
        self.start = datetime.date.fromisoformat(start).toordinal() 
        self.end = None if end is None else datetime.date.fromisoformat(end).toordinal()
  
    def overlaps_at_least(self, other, min_days):
        # Warning! that if target_experience == None we will consider it as ongoing and
        # All the people that are still working at the company will be considered colleagues.
        # This might lead to colleagues that have know each other for less than min_days, if 
        # Today is less than min_days after the start of those experiences.
        if self.end and self.end - self.start < min_days:
            # No overlap if the experience is less than min_days.
            return False
        if other.end and other.end - other.start < min_days:
            # No overlap if the experience is less than min_days.
            return False
        assert not self.end or (self.end - self.start > min_days), f"self experience should be at least {min_days} long."
        assert not other.end or (other.end - other.start > min_days), f"other experience should be at least {min_days} long."
        # By now we know BOTH experiences are at least min_days long.
        if other.start <= self.start:
            if not other.end:
                return True
            elif other.end <= self.start:
                return False
            elif other.end - self.start >= min_days:
                return True
            else:
                return False
        else:
            if not self.end:
                return True
            elif not other.end:
                return True
            elif self.end - other.start >= min_days:
                return True
            
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
    people = {}

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
                person.add_experience(Experience(person, company=experience['company'], title=experience['title'], start=experience['start'], end=experience['end']))
            people[person.id] = person

    return people

def update_experience_with_references(people, companies_short_list):
    """Takes the people structure and updates the experience with references to the company object.
    complexity: O(P+E+size(companies_short_list)*AvgEc*log(AvgEc)) where 
        P is the number of people 
        E is the number of experiences.
        size(companies_short_list) is the number of companies in the short list
        AvgEc is the average number of experiences per company
    ------
    people: dict
        A dictionary of people keyed by id.
    companies_short_list: list
        A list of companies to focus on. If None, all companies are considered.
    """
    companies = {}
    for id in people:
        for experience in people[id].experience:
            if experience.company not in companies_short_list:
                continue  # Shortcut to save time by focusing only on the companies of interest.
            if experience.company not in companies:
                company = Company(experience.company)
                companies[str(experience.company)] = company
            else:
                company = companies[str(experience.company)] 
            company.add_experience(experience)
            experience.company = company  # changing the object reference!
    return companies


def find_connected_person_ids(people, target_id):
    """Returns a list of people that worked at the same company as the target person for at least 90 days.
    The complexity of this function is O(update_experience_with_references) + Et*O(company.colleages) where
    Et is the number of experiences of the target person.
    in other words the complexity is
    O(P+E+AvgCt*AvgEc*log(AvgEc)) + O(Et*AvgEc) where
        P is the number of people
        E is the number of experiences.
        AvgCt is the average number of companies per person. < 10^2
        AvgEc is the average number of experiences per company < 10^4
        Et is the number of experiences of the target person = AvgCt because we assume each experience is in a different company.
    so finally the complexity is
    O(P+E+AvgCt*AvgEc*log(AvgEc)) + O(Et*vgCt)
    """
    connected_ids = set()

    target_person = people[target_id]
    if target_person is None:
        return None
    
    target_companies = target_person.companies_worked_for()
    companies = update_experience_with_references(people, target_companies)

    for target_experience in target_person.experience:
        connected_ids.update(target_experience.company.colleagues(target_experience, COLLEAGUE_LIMIT))
    return connected_ids


# Example usage:
file_path = 'example-1.json'  # Replace with the path to your JSON file
people = load_person_records_from_json_file(file_path)
connected_ids = find_connected_person_ids(people, people[0].id)
print(connected_ids)


