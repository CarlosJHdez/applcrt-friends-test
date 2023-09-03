#! /bin/bash python3 
# find_connections.py

from applcrt_connections_utils import *
import json

def load_person_records_from_json_file(file_path):
    people = {}

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for person_data in data:
            person = Person(
                id=person_data['id'],
                first=person_data['first'],
                last=person_data['last'],
                phone=normalize_phone_number(person_data['phone']),
            )
            for experience in person_data['experience']:
                person.add_experience(Experience(person, company=experience['company'], title=experience['title'], start=experience['start'], end=experience['end']))
            people[person.id] = person

    return people
def load_contact_records_from_json_file(file_path):
    contact_records = []

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for contact_data in data:
            id = contact_data['id']
            owner_id = contact_data['owner_id']
            contact_nickname = contact_data['contact_nickname']
            phone_data = contact_data['phone']
            
            # Create a dictionary of phone numbers and their types
            phones = {}
            for phone in phone_data:
                normalized_number = normalize_phone_number(phone['number']) 
                if normalized_number:
                    phones[normalized_number] = {'type': phone['type']}
            
            contact = Contact(id, owner_id, contact_nickname, phones)
            contact_records.append(contact)

    return contact_records



# Example usage:
file_path = 'persons.json'  # Replace with the path to your JSON file
people = load_person_records_from_json_file(file_path)
colleagues_ids = find_connected_person_ids(people, people[0].id)

# Example usage:
file_path = 'contacts.json'  # Replace with the path to your JSON file
contacts = load_contact_records_from_json_file(file_path)
phone_pals_ids = find_phone_pals_ids(contacts, people, people[0].id)

all_connections = colleagues_ids.union(phone_pals_ids)

print(all_connections)