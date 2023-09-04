#!/usr/bin/env python3

from apcrt_connections_utils import *
import json
import argparse

FIXED_PERSONS_FILE_NAME = 'persons.json' 
FIXED_CONTACTS_FILE_NAME = 'contacts.json'

def load_json_data(file_path):
    """Read and parse JSON data from a file."""
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

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
                person.add_experience(Experience(person, company_name=experience['company'], title=experience['title'], start=experience['start'], end=experience['end']))
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

def print_connections(people, connection_ids):
    connections = sorted([people[person_id] for person_id in connection_ids], key=lambda p: p.id)
    for person in connections:
        print(f"{person.id}: {person.first} {person.last}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find colleagues and phone pals of a person per ID.')
    parser.add_argument('person_id', type=int, help='ID of the person to find colleagues for')
    args = parser.parse_args()

    # Load data from FIXED JSON files
    persons_file_path = FIXED_PERSONS_FILE_NAME
    contacts_file_path = FIXED_CONTACTS_FILE_NAME

    persons_data = load_json_data(persons_file_path)
    contacts_data = load_json_data(contacts_file_path)

    # Parse data
    people = load_person_records(persons_data)
    contact_records = load_contact_records(contacts_data)

    # Find connections
    connections = find_all_connections(people, contact_records, args.person_id)

    if connections:
        print_connections(people, connections)





