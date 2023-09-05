import unittest
from apcrt_connections_utils import *


class TestCompany(unittest.TestCase):
    def setUp(self):
        self.company = Company("Test Company")

    def test_add_experience(self):
        self.assertEqual(len(self.company.experiences), 0, "A company starts with no experiences")
        self.assertEqual(self.company.name, "Test Company", "Check all attributes are set")
        experience1 = Experience(None, self.company, "Tester", 5001, 6000)
        self.company.add_experience(experience1)
        self.assertEqual(len(self.company.experiences), 1)
        experience2 = Experience(None, self.company, "Tester", 4523, 5000)
        self.company.add_experience(experience2)
        self.assertEqual(
            self.company.experiences[0],
            experience2,
            "Experiences should be sorted by start date",
        )


class TestPerson(unittest.TestCase):
    def test_companies_worked_for(self):
        person = Person(1, "John", "Doe", "123-456-7890")
        self.assertEqual(person.id, 1, "Check the id attribute is set")
        self.assertEqual(person.first, "John", "Check the first name attribute is set")
        self.assertEqual(person.last, "Doe", "Check the last name attribute is set")
        self.assertEqual(person.phone, "123-456-7890", "Phone shoud be verbatim.")
        self.assertEqual(len(person.experience), 0)
        exp1 = Experience(person, "Company A", "Role A", "2023-01-01", "2023-02-01")
        exp2 = Experience(person, "Company B", "Role B", "2023-02-01", "2023-03-01")
        person.add_experience(exp1)
        person.add_experience(exp2)
        companies = person.companies_worked_for()
        self.assertEqual(len(companies), 2, "All experiences must be added")
        self.assertIn("Company A", companies)
        self.assertIn("Company B", companies)


class TestExperience(unittest.TestCase):
    def setUp(self):
        self.START = 200  # Useful to make sure the definitions are right, and we can test equality cases
        self.END = 300    # Useful to make sure the definitions are right, and we can test equality cases
        # This bound experience has an end date
        self.bounded_exp = Experience(
            None, None, "Role a", self.START, self.END
        )  # Has a determined end.
        # The unbounded experience does not have an end date ... yet
        self.unbounded_exp = Experience(
            None, None, "Role b", self.START, None
        )  # Does not have an end, is ongoing

    def test_attributes(self):
        person = Person(1, "John", "Doe", "123-456-7890")
        company = Company("Company A")
        start1 = 4000
        end1 = datetime.date.fromisoformat("2023-02-01")
        exp1 = Experience(person, company, "Role A", start1, end1.toordinal())
        self.assertEqual(exp1.person, person)
        self.assertEqual(exp1.company_name, company)
        self.assertEqual(exp1.title, "Role A")
        self.assertEqual(exp1.start, 4000, "Start date should be verbatim.")
        self.assertEqual(datetime.date.fromordinal(exp1.end), end1, "End date should be the same even after datetime transformations.")

    def test_overlaps_at_least(self):
        person = Person(1, "John", "Doe", "123-456-7890")
        # Basic overlap test case. If this doesn't work something is REALLY wrong.
        # uses the fact that the date is saved as an integer to facilitate understanding
        # of the ordering.
        exp1 = Experience(person, "Company A", "Role A", 20230101, 20230201)
        exp2 = Experience(person, "Company A", "Role B", 20230115, 20230301)
        exp3 = Experience(person, "Company A", "Role B", 20230115, None)
        min_days = 15
        self.assertTrue(exp1.overlaps_at_least(exp2, min_days), "The numbers overlap for at least 15")
        self.assertTrue(exp2.overlaps_at_least(exp3, min_days), "The numbers overlap for at least 15, regardless that exp3 is unbounded")


    def test_if_starts_early_vs_bounded(self):
        """Test cases where the experience being compared starts BEFORE
        the bounded (with an end) target experience
        """
        exp = Experience(None, None, "Role A", 1, 100)
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90), "Starts before and ends before")
        exp = Experience(None, None, "Role B", 2, self.START)
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90), "Starts before and ends at the same time as the bounded experience starts")
        exp = Experience(None, None, "Role C", 3, 250)
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90), "Starts before and ends during the bounded experience")
        exp = Experience(None, None, "Role D", 4, 290)
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90), "Starts before and ends after the bounded experience")
        exp = Experience(None, None, "Role E", 5, self.END)
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90), "Starts before and ends at the same time as the bounded experience ends")
        exp = Experience(None, None, "Role F", 6, 400)
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90), "Starts before and ends after the bounded experience ends")
        exp = Experience(None, None, "Role G", 7, None)
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90), "Starts before and the end is unbounded")

    def test_if_starts_early_vs_unbounded(self):
        """Test cases where the experience being compared starts BEFORE
        the bounded (with an end) target experience. This is the same as 
        the previous test, but with the unbounded experience.  
        We leave exactly the same numbers to make sure the logic works, but it could be slightly reduced.
        """
        exp = Experience(None, None, "Role A", 1, 100)
        self.assertFalse(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts before and ends before the unbounded experience starts")
        exp = Experience(None, None, "Role B", 2, self.START)
        self.assertFalse(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts before and ends at the same time as the unbounded experience starts")
        exp = Experience(None, None, "Role C", 3, 250)
        self.assertFalse(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts before and ends during the unbounded experience")
        exp = Experience(None, None, "Role D", 4, 290)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts before and ends during the unbounded experience")
        exp = Experience(None, None, "Role E", 5, self.END)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts before and ends during the unbounded experience")
        exp = Experience(None, None, "Role F", 6, 400)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts before and ends during the unbounded experience")
        exp = Experience(None, None, "Role G", 7, None)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts before and there is no end (is unbounded)")

    def test_if_starts_equal_vs_bounded(self):
        """Test cases where the experience being compared starts at the same time as the bounded experience
        """
        exp = Experience(None, None, "Role eb1", 200, self.END)
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90), "Starts at the same time and ends at the same time as the bounded experience")
        exp = Experience(None, None, "Role eb2", 200, 500)
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90), "Starts at the same time and ends during the bounded experience")
        exp = Experience(None, None, "Role eu1", 200, None)
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90), "Starts at the same time and the end is unbounded")

    def test_if_starts_equal_vs_unbounded(self):
        """Test cases where the experience being compared starts at the same time as the unbounded experience
        We use the same cases as with the bounded experience for consistency, but they could be reduced.
        """
        exp = Experience(None, None, "Role eb1", 200, self.END)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts at the same time as the unbounded experience. The end is irrelevant")
        exp = Experience(None, None, "Role eb2", 200, 500)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts at the same time as the unbounded experience. The end is irrelevant")
        exp = Experience(None, None, "Role eu1", 200, None)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts at the same time as the unbounded experience. The end is unbounded as the compared experience")

    def test_if_starts_included_vs_bounded(self):
        """Test cases where the experience being compared starts during the bounded experience.
        """
        exp = Experience(None, None, "Role lb1", 250, self.END)
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90), "Starts during and ends at the same time as the bounded experience")
        exp = Experience(None, None, "Role lb1", 250, 500)
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90), "Starts during and ends during the bounded experience")
        exp = Experience(None, None, "Role lu1", 250, None)
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90), "Starts during and the end is unbounded")

    def test_if_starts_included_vs_unbounded(self):
        """Test cases where the experience being compared starts during the unbounded experience.
        The test data is the same as before.
        """
        exp = Experience(None, None, "Role lb1", 250, self.END)
        self.assertFalse(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts during the unbounded experience, end is irrelevant")
        exp = Experience(None, None, "Role lb1", 250, 500)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts during the unbounded experience, end is irrelevant")
        exp = Experience(None, None, "Role lu1", 250, None)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90, "Starts during the unbounded experience, is unbounded as well")

    def test_if_starts_late_vs_bounded(self):
        """Test cases where the experience being compared starts after the start of the bounded experience.
        """
        exp = Experience(None, None, "Role lb1", 400, 600)
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90), "Starts after and ends after the bounded experience")
        exp = Experience(None, None, "Role lb1", 400, None)
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90), "Starts after and the end is unbounded")
        exp = Experience(None, None, "Role lb1", 500, 600)
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90), "Starts after and ends after the bounded experience start")

    def test_if_starts_late_vs_unbounded(self):
        """Test cases where the experience being compared starts after the start of the unbounded experience.
        """
        exp = Experience(None, None, "Role lb1", 400, 600)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts after the unbounded experience, end is irrelevant")
        exp = Experience(None, None, "Role lb1", 400, None)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts after the unbounded experience, end is unbounded as well")
        exp = Experience(None, None, "Role lb1", 500, 600)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90), "Starts after the unbounded experience, end is irrelevant")


class TestContact(unittest.TestCase):
    def test_attributes(self):
        person = Person(1, "John", "Doe", "123-456-7890")
        contact = Contact(person, "123-456-7890")
        self.assertEqual(contact.person, person)
        self.assertEqual(contact.phone, "123-456-7890")


class TestNormalizePhoneNumber(unittest.TestCase):
    def test_valid_phone_number(self):
        # Test with a valid phone number
        result = normalize_phone_number("(212) 345-6789")
        self.assertEqual(result, "+12123456789", "A valid phone number will always be normalized to E.164 format")

    def test_valid_phone_number_with_country_code(self):
        # Test with a valid phone number with country code
        result = normalize_phone_number("1-2123458974")
        self.assertEqual(result, "+12123458974", "US Country code will always be preserved in normalized phone numbers")

    def test_other_non_normalized_phone_examples(self):
        result = normalize_phone_number("+19173454768")
        self.assertEqual(result, "+19173454768", "Original data same as normalized data")
        result = normalize_phone_number("+1(917)345-4768")
        self.assertEqual(result, "+19173454768", "() and - are removed")
        result = normalize_phone_number("    (917) 345-  4768")
        self.assertEqual(result, "+19173454768", "Spaces are removed")
        result = normalize_phone_number("    917-345  -  4768   ")
        self.assertEqual(result, "+19173454768, ", "Spaces are removed")

    def test_invalid_phone_number(self):
        # Test with an invalid phone number
        result = normalize_phone_number("invalid_number")
        self.assertIsNone(result, "Invalid phone numbers will be normalized to None")

    def test_empty_phone_number(self):
        # Test with an empty phone number
        result = normalize_phone_number("")
        self.assertIsNone(result, "Empty phone numbers will be normalized to None")

    def test_none_phone_number(self):
        # Test with None as input
        result = normalize_phone_number(None)
        self.assertIsNone(result, "None will be normalized to None")


if __name__ == "__main__":
    unittest.main()
