# Description:
# Read a json file that contains people, and its jobs at various companies.
# Organize it in a way that is easy to find people related to each other because:
# - They worked at the same company for a minimum period of 90 days.
import bisect
import datetime
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

COLLEAGUE_LIMIT = 90  # Minimum number of days to be considered a colleague


class Company:
    """A company is a list of the people that had experiences at that company."""

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
            if other != target and target.overlaps_at_least(other, min_days):
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
        return {experience.company_name for experience in self.experience}

    def __str__(self) -> str:
        return f"{self.first} {self.last}"


class Experience:
    """An Experience is a period (possibly still ongoing) where a person worked for a company."""

    def __init__(self, person: Person, company_name, title, start, end):
        self.person = person
        self.company_name = company_name
        self.title = title
        # convert to ordinal date to facilitate comparisons
        assert start is not None, "start date should not be None"
        self.start = start
        self.end = end
        assert (
            self.end is None or self.end >= self.start
        ), "end date should be after start date after the conversion to ordinal date."

    def overlaps_at_least(self, other, min_days):
        # We first figure out when was the first day they worked together.
        start_meet = max(self.start, other.start)
        # If one of the experiences is ongoing, we go to special cases.
        if not self.end and not other.end:
            # If both experiences are ongoing, we assume there is overlap.
            return True
        elif not self.end:
            end_meet = other.end
        elif not other.end:
            end_meet = self.end
        else:
            end_meet = min(self.end, other.end)
        if end_meet - start_meet >= min_days:
            return True

    def __lt__(self, other):
        """Comparison method to compare experiences based on start dates."""
        if not isinstance(other, Experience):
            raise ValueError("Comparison with non-Experiences object is not supported.")
        return self.start < other.start

    def __str__(self) -> str:
        end = "ongoing" if self.end is None else datetime.date.fromordinal(self.end)
        return f"{self.person} is {self.title} @ {self.company_name} starting {datetime.date.fromordinal(self.start)}, End: {end}"


class Contact:
    def __init__(self, id, owner_id, contact_nickname, phones):
        self.contact_id = id
        self.owner_id = owner_id
        self.contact_nickname = contact_nickname
        self.phones = phones


def get_companies_with_history(people, companies_short_list):
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
            if experience.company_name not in companies_short_list:
                continue  # Shortcut to save time by focusing only on the companies of interest.
            if experience.company_name not in companies:
                company = Company(experience.company_name)
                companies[experience.company_name] = company
            else:
                company = companies[experience.company_name]
            company.add_experience(experience)
    return companies


def find_connected_person_ids(people, target_id):
    """Returns a list of people that worked at the same company as the target person for at least 90 days.
    The complexity of this function is O(update_experience_with_references) + Et*O(company.colleagues) where
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
    companies = get_companies_with_history(people, target_companies)

    for target_experience in target_person.experience:
        company = companies[target_experience.company_name]
        connected_ids.update(company.colleagues(target_experience, COLLEAGUE_LIMIT))
    return connected_ids


def find_phone_pals_ids(contacts, people, target_id):
    """Returns a set of people that are phone pals with the target person. The key is the target person phone number.
    The complexity of this function is O(P*log(P)+C+log(P)) where C is the number of contacts and P is the number of people.
    """
    target_phone = people[target_id].phone

    # Create a directory of people's phones, because it will be needed
    phone_book = {}
    for id in people:
        person = people[id]
        if person.phone is not None and person.phone not in phone_book:
            phone_book[person.phone] = person

    phone_pals_ids = set()
    for contact in contacts:
        if contact.owner_id == target_id:
            for phone in contact.phones:
                if phone in phone_book:
                    phone_pals_ids.add(phone_book[phone].id)
        elif target_phone in contact.phones:
            phone_pals_ids.add(contact.owner_id)
    return phone_pals_ids


def normalize_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, "US")
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(
                parsed_number, phonenumbers.PhoneNumberFormat.E164
            )
        else:
            return None  # Invalid phone number
    except NumberParseException:
        return None  # Invalid phone number format


def load_person_records(data):
    """Parse JSON data to create person records."""
    people = {}
    for person_data in data:
        person = Person(
            id=person_data["id"],
            first=person_data["first"],
            last=person_data["last"],
            phone=normalize_phone_number(person_data["phone"]),
        )
        for experience in person_data["experience"]:
            start = datetime.date.fromisoformat(experience["start"]).toordinal()
            end = (
                None
                if experience["end"] is None
                else datetime.date.fromisoformat(experience["end"]).toordinal()
            )
            person.add_experience(
                Experience(
                    person,
                    company_name=experience["company"],
                    title=experience["title"],
                    start=start,
                    end=end,
                )
            )
        people[person.id] = person
    return people


def load_contact_records(data):
    """Parse JSON data to create contact records."""
    contact_records = []
    for contact_data in data:
        contact_id = contact_data["id"]
        owner_id = contact_data["owner_id"]
        contact_nickname = contact_data["contact_nickname"]
        phone_data = contact_data["phone"]

        phones = {}
        for phone in phone_data:
            if normalized_number := normalize_phone_number(phone["number"]):
                phones[normalized_number] = {"type": phone["type"]}

        contact = Contact(contact_id, owner_id, contact_nickname, phones)
        contact_records.append(contact)
    return contact_records


def find_all_connections(people, contacts, person_id):
    """Find colleagues and phone pals using pre-loaded data."""
    target_person = people.get(person_id)
    if target_person is None:
        print(f"Person with ID {person_id} not found.")
        return

    colleagues_ids = find_connected_person_ids(people, person_id)
    phone_pals_ids = find_phone_pals_ids(contacts, people, person_id)
    return colleagues_ids.union(phone_pals_ids)
