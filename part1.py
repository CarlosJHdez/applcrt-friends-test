# I wrote this code using chatgpt. Is the first version of the code.
# I did not add any error handling at first nor any unit testing.
# This took about 30 minutes to write and test with the example1.json file.
# if the number of persons is P and the total number of experiences is E, 
# the time complexity is O(P+E) and it uses memory O(P+E) as well.
import json

class Person:
    def __init__(self, id, first, last, phone, experience):
        self.id = id
        self.first = first
        self.last = last
        self.phone = phone
        self.experience = experience

def load_person_records_from_json_file(file_path):
    person_records = []

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for person_data in data:
            person = Person(
                id=person_data['id'],
                first=person_data['first'],
                last=person_data['last'],
                phone=person_data['phone'],
                experience=person_data['experience']
            )
            person_records.append(person)

    return person_records

# Example usage:
file_path = 'example1.json'  # Replace with the path to your JSON file
persons = load_person_records_from_json_file(file_path)

# Now you have a list of Person objects in the 'persons' variable.
# You can iterate through this list and work with the data as needed.
for person in persons:
    print(f"Name: {person.first} {person.last}")
    print(f"Phone: {person.phone}")
    for exp in person.experience:
        print(f"Experience at {exp['company']}: {exp['title']} ({exp['start']} - {'Present' if exp['end'] is None else exp['end']})")
    print()