import unittest
from unittest.mock import patch, MagicMock
import os
import re
import shutil
import requests  # Cruciale import toegevoegd
from urllib.parse import urlparse
from web_scraper import WebScraper, sanitize_filename, allowed_by_robots

class MockResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code
    
    def raise_for_status(self):
        if 400 <= self.status_code < 600:
            raise requests.exceptions.HTTPError(f"HTTP Error {self.status_code}")

class TestWebScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = "./test_output"
        os.makedirs(cls.test_dir, exist_ok=True)
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)

    def setUp(self):
        self.start_url = "http://example.com"
        self.scraper = WebScraper(
            start_url=self.start_url,
            output_dir=self.test_dir,
            pattern="test",
            max_pages=10,
            text_only=False
        )

    def test_sanitize_filename(self):
        self.assertEqual(
            sanitize_filename("http://example.com/path?query=1#frag"),
            "path_query_1"
        )
        self.assertEqual(
            sanitize_filename("http://example.com/"),
            "index"
        )

    @patch('urllib.robotparser.RobotFileParser')
    def test_allowed_by_robots(self, mock_rp):
        """Test robots.txt checks (basisimplementatie)"""
        instance = MagicMock()
        instance.can_fetch.side_effect = lambda agent, url: "private" not in url
        mock_rp.return_value = instance

        cache = {}
        self.assertFalse(
            allowed_by_robots("http://example.com/private/", cache, self.start_url),
            "Moet geweigerd worden door robots.txt"
        )
        self.assertTrue(
            allowed_by_robots("http://example.com/public/", cache, self.start_url),
            "Moet toegestaan worden door robots.txt"
        )

    @patch('web_scraper.requests.get')
    def test_crawl_basic(self, mock_get):
        mock_get.return_value = MockResponse(
            '<html><a href="/page1">Link1</a><a href="/page2">Link2</a></html>'
        )
        self.scraper.max_pages = 2
        self.scraper.crawl()
        
        self.assertEqual(len(self.scraper.visited), 2)
        self.assertIn(f"{self.start_url}/page1", self.scraper.visited)

    @patch('web_scraper.requests.get')
    def test_max_pages(self, mock_get):
        mock_get.return_value = MockResponse(
            '<html><a href="/page1"></a><a href="/page2"></a></html>'
        )
        self.scraper.max_pages = 3
        self.scraper.crawl()
        self.assertEqual(len(self.scraper.visited), 3)

    @patch('web_scraper.requests.get')
    def test_retry_logic(self, mock_get):
        mock_get.side_effect = [
            requests.exceptions.ConnectionError("Temporary error"),
            MockResponse("Success", 200)
        ]
        self.scraper.crawl()
        self.assertEqual(mock_get.call_count, 2)

if __name__ == '__main__':
    unittest.main(verbosity=2)
