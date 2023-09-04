import unittest
from apcrt_connections_utils import *

class TestIntegration(unittest.TestCase):
    def setUp(self):
        data = [
            {
                "id": 1,
                "first": "John",
                "last": "Doe",
                "phone": "123-456-7890",
                "experience": [
                    {
                        "company": "Company A",
                        "title": "Role A",
                        "start": "2023-01-01",
                        "end": "2023-02-01"
                    },
                    {
                        "company": "Company B",
                        "title": "Role B",
                        "start": "2023-02-01",
                        "end": "2023-03-01"
                    }
                ]
            }
        ]

        contact_data = [
            {
                "id": 1,
                "owner_id": 1,
                "contact_nickname": "Friend",
                "phone": [
                    {"number": "+11234567890", "type": "mobile"}
                ]
            }
        ]

        self.people = load_person_records(data)
        self.contacts = load_contact_records(contact_data)

    def test_find_connected_person_ids(self):
        colleagues_ids = find_connected_person_ids(self.people, 1)
        self.assertEqual(len(colleagues_ids), 1)

    def test_find_phone_pals_ids(self):
        phone_pals_ids = find_phone_pals_ids(self.contacts, self.people, 1)
        self.assertEqual(len(phone_pals_ids), 1)

    def test_find_all_connections(self):
        all_connections = find_all_connections(self.people, self.contacts, 1)
        self.assertEqual(len(all_connections), 2)
        
if __name__ == "__main__":
    unittest.main()