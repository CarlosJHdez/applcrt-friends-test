import unittest
from apcrt_connections_utils import *

class TestIntegration(unittest.TestCase):
    def setUp(self):
        data = [{
            "id": 0,
            "first": "Jane",
            "last": "Doe",
            "phone": "+1 (508)4492121",
            "experience": [{
                "company": "OrangeCart",
                "title": "Director of Marketing",
                "start": "2017-01-01",
                "end": None
            },
            {
                "company": "BlueCart",
                "title": "VP of Marketing",
                "start": "2015-01-01",
                "end": "2017-01-01"
            }]
        },
        {
            "id": 1,
            "first": "Barbie",
            "last": "Matel",
            "phone": "1-2122635415",
                "experience": [{
                "company": "OrangeCart",
                "title": "Marketing Associate",
                "start": "2017-01-01",
                "end": "2018-01-01"
            }]
        },
        {
            "id": 2,
            "first": "Ken",
            "last": "Matel",
            "phone": "1-6462214505",
            "experience": [{
            "company": "OrangeCart",
            "title": "Director of Marketing",
            "start": "2018-01-01",
            "end": None
            }]
            },
        {
            "id": 3,
            "first": "Allan",
            "last": "Matel",
            "phone": None,
            "experience": [{
            "company": "BlueCart",
            "title": "Director of Nothing",
            "start": "2015-06-01",
            "end": "2016-01-01"
            }]
            }
        ]

        contact_data = [{
            "id": 0,
            "owner_id": 0,
            "contact_nickname": "Mom",
            "phone": [{
            "number": "(212) 345-8974",
            "type": "landline"
            }, {
            "number": "+19173454768",
            "type": "cell"
            }]
        },
        {
            "id": 1,
            "owner_id": 3,
            "contact_nickname": "Barbie",
            "phone": [{
            "number": "(212) 263-5415",
            "type": "landline"
            }, {
            "number": "+1(508)2894356",
            "type": "cell"
            }]
        },
        {
            "id": 2,
            "owner_id": 3,
            "contact_nickname": "Ken",
            "phone": [{
            "number": "(212) 2345678",
            "type": "landline"
            }, {
            "number": "+1646-221-4505",
            "type": "cell"
            }]
        },
        {
            "id": 3,
            "owner_id": 1,
            "contact_nickname": "Ken",
            "phone": [{
            "number": "+1(339)3333333",
            "type": "landline"
            }, {
            "number": "+1(646)2214505",
            "type": "cell"
            }]
        },
        {
            "id": 4,
            "owner_id": 2,
            "contact_nickname": "Barbie",
            "phone": [{
            "number": "+1(201)2212222",
            "type": "landline"
            }, {
            "number": "+1(212)2635415",
            "type": "cell"
            }]
        }
        ]

        self.people = load_person_records(data)
        self.contacts = load_contact_records(contact_data)

    def test_find_connected_person_ids(self):
        # On the test data, the following people worked with each other:
        # 0: 1, 2, 3
        # 1: 0
        # 2: 0
        # 3: 0
        colleagues_ids = find_connected_person_ids(self.people, 0)
        self.assertEqual( colleagues_ids, {1, 2, 3})
        colleagues_ids = find_connected_person_ids(self.people, 1)
        self.assertEqual( colleagues_ids, {0})
        colleagues_ids = find_connected_person_ids(self.people, 2)
        self.assertEqual( colleagues_ids, {0})
        colleagues_ids = find_connected_person_ids(self.people, 3)
        self.assertEqual( colleagues_ids, {0})

    def test_find_phone_pals_ids(self):
        # On the test data, the following people have the phone number of one another:
        # 0: None.. she has no phone pals!
        # 3: 1, 2
        # 1: 1
        # 2: 1
        phone_pals_ids = find_phone_pals_ids(self.contacts, self.people, 0)
        self.assertEqual(len(phone_pals_ids), 0)
        phone_pals_ids = find_phone_pals_ids(self.contacts, self.people, 1)
        self.assertEqual(phone_pals_ids, {2, 3})
        phone_pals_ids = find_phone_pals_ids(self.contacts, self.people, 2)
        self.assertEqual(phone_pals_ids, {1, 3})
        phone_pals_ids = find_phone_pals_ids(self.contacts, self.people, 3)
        self.assertEqual(phone_pals_ids, {1, 2})

    def test_find_all_connections(self):
        # This test must be simply the union of the other two.
        all_connections = find_all_connections(self.people, self.contacts, 0)
        self.assertEqual(all_connections, {1, 2, 3})
        all_connections = find_all_connections(self.people, self.contacts, 1)
        self.assertEqual(all_connections, {0, 2, 3})
        all_connections = find_all_connections(self.people, self.contacts, 2)
        self.assertEqual(all_connections, {0, 3, 1})
        all_connections = find_all_connections(self.people, self.contacts, 3)
        self.assertEqual(all_connections, {0, 1, 2})
    
if __name__ == "__main__":
    unittest.main()