#!/usr/bin/env python3

from apcrt_connections_utils import *
import json
import argparse

FIXED_PERSONS_FILE_NAME = "persons.json"
FIXED_CONTACTS_FILE_NAME = "contacts.json"


def load_json_data(file_path):
    """Read and parse JSON data from a file."""
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def print_connections(people, connection_ids):
    connections = sorted(
        [people[person_id] for person_id in connection_ids], key=lambda p: p.id
    )
    for person in connections:
        print(f"{person.id}: {person.first} {person.last}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find colleagues and phone pals of a person per ID."
    )
    parser.add_argument(
        "person_id", type=int, help="ID of the person to find colleagues for"
    )
    args = parser.parse_args()

    # Load data from FIXED JSON files
    persons_file_path = FIXED_PERSONS_FILE_NAME
    contacts_file_path = FIXED_CONTACTS_FILE_NAME

    persons_data = load_json_data(persons_file_path)
    contacts_data = load_json_data(contacts_file_path)

    # Parse data
    people = load_person_records(persons_data)
    contact_records = load_contact_records(contacts_data)

    if connections := find_all_connections(people, contact_records, args.person_id):
        print_connections(people, connections)
