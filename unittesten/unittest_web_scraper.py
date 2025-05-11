import unittest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open, call

# Voeg parent directory toe aan Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'web_scraper')))

import web_scraper

class TestWebScraper(unittest.TestCase):
    @patch('os.makedirs')
    def test_get_safe_output_dir(self, mock_makedirs):
        url = "https://www.example.com/path/to/page"
        result = web_scraper.get_safe_output_dir(url)
        self.assertIn("www.example.com", result)
        self.assertIn("path_to_page", result)

    def test_sanitize_filename(self):
        url = "https://www.example.com/path/to/file.html?foo=bar"
        result = web_scraper.sanitize_filename(url)
        self.assertIn("path_to_file.html", result)
        self.assertIn("foo_bar", result)

    @patch('os.makedirs')
    def test_webscraper_init(self, mock_makedirs):
        scraper = web_scraper.WebScraper(
            start_url="https://www.example.com",
            download_html=True,
            download_text=True
        )
        mock_makedirs.assert_any_call(scraper.output_dir, exist_ok=True)

    @patch('web_scraper.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_file(self, mock_file, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"test content"
        mock_get.return_value = mock_response

        scraper = web_scraper.WebScraper("https://www.example.com", download_images=True)
        result = scraper.download_file("https://www.example.com/image.jpg", "image")
        
        self.assertTrue(result)
        mock_file.assert_called_once()

    @patch('web_scraper.requests.get')
    @patch('web_scraper.BeautifulSoup')
    def test_crawl_success(self, mock_bs, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><a href='/next'></a></html>"
        mock_response.headers = {"Content-Type": "text/html"}
        mock_get.return_value = mock_response

        soup = MagicMock()
        soup.find_all.return_value = []
        mock_bs.return_value = soup

        scraper = web_scraper.WebScraper("https://www.example.com", max_pages=1)
        scraper.crawl()
        
        self.assertGreater(len(scraper.visited), 0)

    @patch('web_scraper.requests.get', side_effect=Exception("Error"))
    def test_crawl_failure(self, mock_get):
        scraper = web_scraper.WebScraper("https://www.example.com", max_pages=1)
        scraper.crawl()
        
        self.assertIn("https://www.example.com", scraper.visited)

    @patch('web_scraper.glob.glob')
    def test_report(self, mock_glob):
        mock_glob.return_value = ["file1", "file2"]
        scraper = web_scraper.WebScraper("https://www.example.com")
        scraper.report()  # Alleen output verificatie, geen asserts

if __name__ == '__main__':
    unittest.main(verbosity=2)
