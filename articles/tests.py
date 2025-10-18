from bs4 import BeautifulSoup
from django.test import SimpleTestCase

from articles import scraping

HTML_1 = """
<html>
  <head>
    <meta property="og:title" content="Przykładowy tytuł" />
    <title>Przykładowy tytuł</title>
  </head>
  <body>
    <article class="entry-content">
      <h1>Nagłówek</h1>
      <p>Data publikacji:
      <span>15.05.2025</span></p>
      <p>To jest akapit treści artykułu. Ten tekst jest celowo dłuższy, aby przekroczyć próg długości.</p>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum non dui in lorem malesuada
      laoreet. Integer congue, sapien quis efficitur dignissim, erat orci ultrices dui, et fermentum
      neque lectus at arcu.</p>
    </article>
  </body>
</html>
"""

HTML_2 = """
<html>
  <head>
  </head>
  <body>
    <article class="entry-content">
      <p>Data publikacji:
      <span>2 dni temu</span></p>
      <p>To jest akapit treści artykułu. Ten tekst jest celowo dłuższy, aby przekroczyć próg długości.</p>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum non dui in lorem malesuada
      laoreet. Integer congue, sapien quis efficitur dignissim, erat orci ultrices dui, et fermentum
      neque lectus at arcu.</p>
    </article>
  </body>
</html>
"""

HTML_3 = """
<html>
  <head>
    <meta property="og:title" content="Przykładowy tytuł" />
    <title>Przykładowy tytuł</title>
  </head>
  <body>
    <article class="entry-content">
      <h1>Nagłówek</h1>
      <p>Data publikacji:
      <span>13.05.2024 - 15:30</span></p>
      <p>To jest akapit treści artykułu. Ten tekst jest celowo dłuższy, aby przekroczyć próg długości.</p>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum non dui in lorem malesuada
      laoreet. Integer congue, sapien quis efficitur dignissim, erat orci ultrices dui, et fermentum
      neque lectus at arcu.</p>
    </article>
  </body>
</html>
"""


class ScrapingUnitTests(SimpleTestCase):
    def test_extract_title(self):
        soup = BeautifulSoup(HTML_1, "html.parser")
        self.assertEqual(scraping.extract_title(soup), "Przykładowy tytuł")

    def test_extract_title_without_title(self):
        soup = BeautifulSoup(HTML_2, "html.parser")
        self.assertEqual(scraping.extract_title(soup), "Untitled")

    def test_extract_text_min_length(self):
        soup = BeautifulSoup(HTML_1, "html.parser")
        txt = scraping.extract_text(soup)
        self.assertGreaterEqual(len(txt), 200)

    def test_extract_date_normalizes_to_midnight(self):
        soup = BeautifulSoup(HTML_1, "html.parser")
        dt = scraping.extract_date(soup)
        self.assertEqual(
            scraping.normalize_datetime(dt).strftime("%d.%m.%Y %H:%M:%S"), "15.05.2025 00:00:00"
        )

    def test_extract_relative_date(self):
        soup = BeautifulSoup(HTML_2, "html.parser")
        dt = scraping.extract_date(soup)
        self.assertEqual(
            scraping.normalize_datetime(dt).strftime("%d.%m.%Y %H:%M:%S"), "16.10.2025 00:00:00"
        )

    def test_extract_date_with_time(self):
        soup = BeautifulSoup(HTML_3, "html.parser")
        dt = scraping.extract_date(soup)
        self.assertEqual(
            scraping.normalize_datetime(dt).strftime("%d.%m.%Y %H:%M:%S"), "13.05.2024 15:30:00"
        )
