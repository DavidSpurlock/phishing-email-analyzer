import unittest
from analyzer import parse_email, extract_links, check_links

class TestPhishingAnalyzer(unittest.TestCase):
    def test_parse_email(self):
        headers, body, attachments = parse_email("test_email.eml")
        self.assertIn("From", headers)
        self.assertIn("To", headers)

    def test_extract_links(self):
        body = "Check out this link: http://example.com"
        links = extract_links(body)
        self.assertEqual(links, ["http://example.com"])

    def test_check_links(self):
        links = ["http://example.com"]
        results = check_links(links)
        self.assertIn("http://example.com", results)

if __name__ == "__main__":
    unittest.main()
