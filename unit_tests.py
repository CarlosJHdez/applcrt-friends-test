import unittest
import phonenumbers
from applcrt_connections_utils import *

class TestNormalizePhoneNumber(unittest.TestCase):
    def test_valid_phone_number(self):
        # Test with a valid phone number
        result = normalize_phone_number("(212) 345-6789")
        self.assertEqual(result, "+12123456789")

    def test_valid_phone_number_with_country_code(self):
        # Test with a valid phone number with country code
        result = normalize_phone_number("1-2123458974")
        self.assertEqual(result, "+12123458974")
        
    def test_other_non_normalized_phone_examples(self):
        result = normalize_phone_number("+19173454768")
        self.assertEqual(result, "+19173454768")
        result = normalize_phone_number("+1(917)345-4768")
        self.assertEqual(result, "+19173454768")
        result = normalize_phone_number("    (917) 345-  4768")
        self.assertEqual(result, "+19173454768")
        result = normalize_phone_number("    917-345  -  4768   ")
        self.assertEqual(result, "+19173454768")
        

    def test_invalid_phone_number(self):
        # Test with an invalid phone number
        result = normalize_phone_number("invalid_number")
        self.assertIsNone(result)

    def test_empty_phone_number(self):
        # Test with an empty phone number
        result = normalize_phone_number("")
        self.assertIsNone(result)

    def test_none_phone_number(self):
        # Test with None as input
        result = normalize_phone_number(None)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()