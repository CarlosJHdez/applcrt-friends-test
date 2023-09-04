import unittest
from apcrt_connections_utils import *

class TestCompany(unittest.TestCase):
    def setUp(self):
        self.company = Company("Test Company")
        
    def test_add_experience(self):
        self.assertEqual(len(self.company.experiences), 0)
        self.assertEqual(self.company.name, "Test Company")
        experience1 = Experience(None, self.company, "Tester", 4523, 5000)
        self.company.add_experience(experience1)
        self.assertEqual(len(self.company.experiences), 1)
        experience2 = Experience(None, self.company, "Tester", 5001, 6000)
        self.company.add_experience(experience2)
        self.assertEqual(self.company.experiences[0], experience2, "Experiences should be sorted by start date")

class TestPerson(unittest.TestCase):
    def test_companies_worked_for(self):
        person = Person(1, "John", "Doe", "123-456-7890")
        self.assertEqual(person.id, 1)
        self.assertEqual(person.first, "John")
        self.assertEqual(person.last, "Doe")
        self.assertEqual(person.phone, "123-456-7890")
        self.assertEqual(len(person.experience), 0)
        exp1 = Experience(person, "Company A", "Role A", "2023-01-01", "2023-02-01")
        exp2 = Experience(person, "Company B", "Role B", "2023-02-01", "2023-03-01")
        person.add_experience(exp1)
        person.add_experience(exp2)
        companies = person.companies_worked_for()
        self.assertEqual(len(companies), 2)
        self.assertIn( "Company A", companies)
        self.assertIn( "Company B", companies)

class TestExperience(unittest.TestCase):
    def setUp(self):
        self.START = 200
        self.END = 300
        self.bounded_exp = Experience(None, None, "Role a",  self.START, self.END)  # Has a determined end.
        self.unbounded_exp = Experience(None, None, "Role b",  self.START, None) # Does not have an end, is ongoing

    
    def test_attributes(self):
        person = Person(1, "John", "Doe", "123-456-7890")
        company = Company("Company A")
        start1 = 4000
        end1 = datetime.date.fromisoformat("2023-02-01")
        exp1 = Experience(person, company, "Role A", start1 , end1.toordinal())     
        self.assertEqual(exp1.person, person)
        self.assertEqual(exp1.company, company)
        self.assertEqual(exp1.title, "Role A")
        self.assertEqual(exp1.start, 4000)
        self.assertEqual(datetime.date.fromordinal(exp1.end), end1)
    
    
    def test_overlaps_at_least(self):
        person = Person(1, "John", "Doe", "123-456-7890")
        exp1 = Experience(person, "Company A", "Role A", 20230101, 20230201)
        exp2 = Experience(person, "Company A", "Role B", 20230115, 20230301)
        exp2 = Experience(person, "Company A", "Role B", 20230115, None)
        min_days = 15
        self.assertTrue(exp1.overlaps_at_least(exp2, min_days))
     
        
    def test_if_starts_early_vs_bounded(self):
        """Test cases where the experience being compared starts BEFORE 
        the bounded (with an end) target experience
        """
        exp = Experience(None, None, "Role A",  1, 100)    
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role B",  2, self.START)    
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role C",  3, 250)    
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role D",  4, 290)    
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role E",  5, self.END)   
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role F",  6, 400) 
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90))        
        exp = Experience(None, None, "Role G",  7, None)
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90)) 
 
         
    def test_if_starts_early_vs_unbounded(self):
        """Test cases where the experience being compared starts BEFORE 
        the bounded (with an end) target experience
        """
        exp = Experience(None, None, "Role A",  1, 100)    
        self.assertFalse(self.unbounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role B",  2, self.START)    
        self.assertFalse(self.unbounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role C",  3, 250)    
        self.assertFalse(self.unbounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role D",  4, 290)    
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role E",  5, self.END)   
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role F",  6, 400) 
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90))        
        exp = Experience(None, None, "Role G",  7, None)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90))    
            
            
    def test_if_starts_equal_vs_bounded(self):
        exp = Experience(None, None, "Role eb1",  200, self.END) 
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role eb2",  200, 500) 
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role eu1",  200, None)
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90))
        
    def test_if_starts_equal_vs_unbounded(self):
        exp = Experience(None, None, "Role eb1",  200, self.END) 
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role eb2",  200, 500) 
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role eu1",  200, None)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90))
        
    def test_if_starts_included_vs_bounded(self):
        exp = Experience(None, None, "Role lb1",  250, self.END)
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role lb1",  250, 500)
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90))        
        exp = Experience(None, None, "Role lu1",  250, None)
        self.assertTrue(self.bounded_exp.overlaps_at_least(exp, 90))
 
        
    def test_if_starts_included_vs_unbounded(self):
        exp = Experience(None, None, "Role lb1",  250, self.END)
        self.assertFalse(self.unbounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role lb1",  250, 500)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90))        
        exp = Experience(None, None, "Role lu1",  250, None)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90))

               
    def test_if_starts_late_vs_bounded(self):
        exp = Experience(None, None, "Role lb1",  400, 600)    
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role lb1",  400, None)    
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role lb1",  500, 600)
        self.assertFalse(self.bounded_exp.overlaps_at_least(exp, 90))

             
    def test_if_starts_late_vs_unbounded(self):
        exp = Experience(None, None, "Role lb1",  400, 600)    
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role lb1",  400, None)    
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90))
        exp = Experience(None, None, "Role lb1",  500, 600)
        self.assertTrue(self.unbounded_exp.overlaps_at_least(exp, 90))
        
class TestContact(unittest.TestCase):
    def test_normalize_phone_number(self):
        pass




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