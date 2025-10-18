from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from articles.models import Article
from articles.scraping import (
    extract_date,
    extract_original_article,
    extract_text,
    extract_title,
    fetch_html,
    normalize_datetime,
)
from articles.services import save_article

URLS = [
    "https://galicjaexpress.pl/ford-c-max-jaki-silnik-benzynowy-wybrac-aby-zaoszczedzic-na-paliwie",
    "https://galicjaexpress.pl/bmw-e9-30-cs-szczegolowe-informacje-o-osiagach-i-historii-modelu",
    "https://take-group.github.io/example-blog-without-ssr/jak-kroic-piers-z-kurczaka-aby-uniknac-suchych-kawalkow-miesa",
    "https://take-group.github.io/example-blog-without-ssr/co-mozna-zrobic-ze-schabu-oprocz-kotletow-5-zaskakujacych-przepisow",
]


class Command(BaseCommand):
    help = "Scrape predefined articles and store them in DB"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            dest="url",
            help="Scrape a single URL instead of the predefined list.",
        )

    def handle(self, *args, **options):
        urls = [options["url"]] if options.get("url") else URLS

        total = len(urls)
        for i, url in enumerate(urls, start=1):
            self.stdout.write(self.style.NOTICE(f"Scraping article {i}/{total}: {url}"))
            if Article.objects.filter(source_url=url).exists():
                self.stdout.write(self.style.WARNING(" → already exists, skipping"))
                continue

            html = fetch_html(url)
            if not html:
                self.stderr.write(self.style.ERROR(" → fetch failed"))
                continue

            soup = BeautifulSoup(html, "html.parser")
            title = extract_title(soup)
            text = extract_text(soup)
            dt_raw = extract_date(soup)
            dt = normalize_datetime(dt_raw)

            html_article = extract_original_article(soup) or html
            save_article(url.strip(), title, html_article, text, dt)
            self.stdout.write(self.style.SUCCESS(" → saved"))
