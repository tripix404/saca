import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import os

from paste import WebScraper, sanitize_filename, get_safe_output_dir

class TestWebScraper(unittest.TestCase):

    def test_sanitize_filename(self):
        url = "https://www.example.com/path/to/file.html?foo=bar"
        result = sanitize_filename(url)
        self.assertIn("path_to_file.html", result)
        self.assertIn("foo_bar", result)

    def test_get_safe_output_dir(self):
        url = "https://www.example.com/path/to/page"
        result = get_safe_output_dir(url)
        self.assertTrue(result.startswith("www.example.com"))
        self.assertIn("path_to_page", result)

    @patch("os.makedirs")
    @patch("paste.get_safe_output_dir", return_value="testdir")
    def test_webscraper_init_creates_dirs(self, mock_dir, mock_makedirs):
        scraper = WebScraper(
            start_url="https://www.example.com",
            download_html=True,
            download_text=True,
            download_images=True,
            download_pdfs=True
        )
        # 1x voor main, 4x voor submappen
        self.assertGreaterEqual(mock_makedirs.call_count, 5)

    @patch("paste.requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_file_image(self, mock_file, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"imgdata"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        scraper = WebScraper("https://www.example.com", download_images=True)
        with patch("os.path.join", return_value="testdir/images/testfile.jpg"):
            result = scraper.download_file("https://www.example.com/img.jpg", "image")
            self.assertTrue(result)
            mock_file.assert_called_with("testdir/images/testfile.jpg", "wb")

    @patch("paste.requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_file_pdf(self, mock_file, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"pdfdata"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        scraper = WebScraper("https://www.example.com", download_pdfs=True)
        with patch("os.path.join", return_value="testdir/pdfs/testfile.pdf"):
            result = scraper.download_file("https://www.example.com/doc.pdf", "pdf")
            self.assertTrue(result)
            mock_file.assert_called_with("testdir/pdfs/testfile.pdf", "wb")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_page_html_and_text(self, mock_file):
        scraper = WebScraper("https://www.example.com", download_html=True, download_text=True)
        with patch("os.path.join", side_effect=lambda *a: "/".join(a)):
            scraper.save_page("https://www.example.com/page", "<html>hi</html>", "hi")
            # Twee keer schrijven: html en txt
            self.assertEqual(mock_file.call_count, 2)

    @patch("paste.requests.get")
    @patch("paste.BeautifulSoup")
    @patch("os.makedirs")
    @patch("paste.allowed_by_robots", return_value=True)
    def test_crawl_visits_and_saves(self, mock_robots, mock_makedirs, mock_bs, mock_get):
        html = "<html><body><a href='/next'>next</a></body></html>"
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.headers = {"Content-Type": "text/html"}
        mock_response.text = html
        mock_get.return_value = mock_response

        soup = MagicMock()
        soup.get_text.return_value = "some text"
        soup.find_all.side_effect = [
            [MagicMock(name="a", href="/next")],  # First call: links
            []  # Second call: no more links
        ]
        mock_bs.return_value = soup

        scraper = WebScraper("https://www.example.com", download_html=True, max_pages=1)
        with patch.object(scraper, "save_page") as mock_save_page:
            scraper.crawl()
            mock_save_page.assert_called_once()

    @patch("paste.requests.get")
    @patch("paste.BeautifulSoup")
    @patch("os.makedirs")
    @patch("paste.allowed_by_robots", return_value=True)
    def test_crawl_handles_exception(self, mock_robots, mock_makedirs, mock_bs, mock_get):
        mock_get.side_effect = Exception("Network error")
        scraper = WebScraper("https://www.example.com", download_html=True, max_pages=1)
        with patch.object(scraper, "save_page") as mock_save_page:
            scraper.crawl()
            mock_save_page.assert_not_called()
            self.assertIn("https://www.example.com", scraper.visited)

if __name__ == "__main__":
    unittest.main(verbosity=2)
