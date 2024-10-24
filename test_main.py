import unittest
from io import StringIO
import csv
import copy
from itertools import combinations
from main import similarity, extract_username, match_score, find_potential_duplicates

class TestContactDuplicateDetection(unittest.TestCase):
    # Some contacts that represent edge cases
    contacts = [
        {'contactID': 1, 'name': 'Ciara', 'name1': 'French',
         'email': 'ciara.french@gmail.com', 'address': '123 Main St'},
        {'contactID': 2, 'name': 'Ciara', 'name1': 'French',
         'email': 'ciara.french@outlook.com', 'address': '123 Main St'},
        {'contactID': 3, 'name': 'Victor', 'name1': 'Savage',
         'email': 'victor.savage@protonmail.net', 'address': '456 Elm St'},
        {'contactID': 4, 'name': 'John', 'name1': 'Doe',
         'email': 'john.doe@gmail.com', 'address': '789 Oak St'},
        {'contactID': 5, 'name': 'C', 'name1': 'French',
         'email': 'mollis.lectus.pede@yahoo.net', 'address': '449-6990 Tellus. Rd.'},
        {'contactID': 6, 'name': 'C', 'name1': 'Pacheco',
         'email': 'nulla.eget@att.couk', 'address': 'Ap #312-8611 Lacus. Ave'},
        {'contactID': 7, 'name': 'V', 'name1': 'Savage',
         'email': 'orci@att.net', 'address': 'P.O. Box 775, 8910 Arcu. Road'},
        {'contactID': 8, 'name': 'C', 'name1': 'F',
         'email': 'sociosqu.ad@yahoo.edu', 'address': 'Ap #963-2867 Nulla St.'},
        {'contactID': 9, 'name': 'P', 'name1': 'H',
         'email': 'odio.sagittis.semper@google.ca', 'address': 'P.O. Box 948, 7688 Consequat Av.'},
        {'contactID': 10, 'name': 'C', 'name1': 'S',
         'email': 'lorem@comcast.couk', 'address': 'P.O. Box 776, 7009 Dictum Av.'},
        {'contactID': 11, 'name': 'D', 'name1': 'T',
         'email': 'nam.nulla@yahoo.edu', 'address': '642-974 Sed St.'},
        {'contactID': 12, 'name': 'Gar', 'name1': 'Lonpucci',
         'email': 'glonpucci@gmail.com', 'address': '123 Main St'},
        {'contactID': 13, 'name': 'Garfield', 'name1': 'Lonpucci',
         'email': 'glonpucci@outlook.com', 'address': '123 Main St'}
    ]

    def test_similarity(self):
        """Test the similarity function with various strings."""
        self.assertAlmostEqual(similarity('abc', 'abc', {}), 1.0)
        self.assertAlmostEqual(similarity('abc', 'ab', {}), 0.8, delta=0.1)
        self.assertAlmostEqual(similarity('abc', 'xyz', {}), 0.0)

    def test_extract_username(self):
        """Test extracting usernames from email addresses."""
        self.assertEqual(extract_username('test@example.com'), 'test')
        self.assertEqual(extract_username('user@domain.com'), 'user')
        self.assertEqual(extract_username(''), '')

    def test_match_score_exact_email(self):
        """Test that exact email matches return a score of 1.0."""
        contact1 = self.contacts[0]
        contact2 = self.contacts[0]
        self.assertEqual(match_score(contact1, contact2, {}), 1.0)

    def test_match_score_similar_name(self):
        """Test that similar names and addresses give a good score."""
        contact1 = self.contacts[11]
        contact2 = self.contacts[12]
        score = match_score(contact1, contact2, {})
        self.assertGreaterEqual(score, 0.75)
        self.assertLess(score, 1.0)

    def test_near_coincidence_not_match(self):
        """Test cases where there are some similarities but no match."""
        contact1 = self.contacts[4]
        contact2 = self.contacts[8]
        score = match_score(contact1, contact2, {})
        self.assertLess(score, 0.7)  # Ensure they are not marked as duplicates




    def test_read_write_csv(self):
        """Test reading from and writing to a CSV."""
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=self.contacts[0].keys())
        writer.writeheader()
        writer.writerows(self.contacts)

        input_data = StringIO(output.getvalue())
        reader = csv.DictReader(input_data)
        read_contacts = [row for row in reader]

        self.assertEqual(len(read_contacts), len(self.contacts))
        self.assertEqual(read_contacts[0]['name'], self.contacts[0]['name'])


    def test_find_potential_duplicates(self):
        """Test the duplicate detection logic for all contacts."""
        matches = find_potential_duplicates(copy.deepcopy(self.contacts))
        # Extract all 'High' and 'Low' matches
        high_matches = [(a, b) for a, b, accuracy in matches if accuracy == 'High']
        low_matches = [(a, b) for a, b, accuracy in matches if accuracy == 'Low']

        # Ensure specific duplicates are detected
        self.assertIn((1, 2, 'High'), matches)
        self.assertIn((12, 13, 'High'), matches)
        self.assertNotIn((5, 8, 'High'), matches)
        self.assertEqual(len(high_matches), 2, f"Expected 17 high matches, but got {len(high_matches)}")
        self.assertEqual(len(low_matches), 15, f"Expected 15 low matches, but got {len(low_matches)}")

        # Verify that every contact is correctly assigned

if __name__ == '__main__':
    unittest.main()
