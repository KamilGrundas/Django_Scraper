# articles/scraping.py
from __future__ import annotations

import logging
import re
from datetime import datetime
from zoneinfo import ZoneInfo

import dateparser
from bs4 import BeautifulSoup
from django.conf import settings
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)


UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/127 Safari/537.36"
)

# From most specific to least specific
ARTICLE_SELECTORS = [
    "div[itemprop='articleBody']",
    "div.post-content",
    "div.article-content",
    "div.table-post",
    "div.main--content--body",
    "article",
    "main",
]


TZ_INFO = ZoneInfo(settings.TIME_ZONE)

TIME_PATTERNS = [
    r"\b\d{1,2}:\d{2}(?::\d{2})?\b",  # 14:05 lub 14:05:30
    r"\b\d{1,2}:\d{2}(?::\d{2})? ?(am|pm)\b",  # 2:30 pm
    r"T\d{2}:\d{2}(?::\d{2})?",  # ISO: T14:05[:30]
]
TIME_RE = re.compile("|".join(TIME_PATTERNS), re.IGNORECASE)


def has_time(candidate: str) -> bool:
    return bool(TIME_RE.search(candidate))


def parse_date(candidate: str) -> datetime | None:
    if not candidate:
        return None
    dt = dateparser.parse(
        candidate,
        settings={
            "RELATIVE_BASE": datetime.now(TZ_INFO),
            "TIMEZONE": settings.TIME_ZONE,
            "RETURN_AS_TIMEZONE_AWARE": True,
            "PREFER_DATES_FROM": "past",
            "PARSERS": ["absolute-time", "relative-time"],
            "NORMALIZE": True,
            "SKIP_TOKENS": ["o", "r.", "roku"],
        },
        languages=["pl", "en"],
    )
    if not dt:
        return None
    # Ensure timezone-aware datetime before manipulating
    dt = normalize_datetime(dt)
    if has_time(candidate):
        return dt
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def normalize_datetime(dt: datetime | None) -> datetime:
    if not dt:
        return datetime.now(TZ_INFO)
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=TZ_INFO)
    return dt.astimezone(TZ_INFO)


def fetch_html(url: str, timeout: int = 15) -> str | None:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            ctx = browser.new_context(user_agent=UA, timezone_id=settings.TIME_ZONE)
            page = ctx.new_page()
            page.set_default_timeout(timeout * 1000)
            page.goto(url, wait_until="domcontentloaded")

            selectors = ", ".join(ARTICLE_SELECTORS)
            page.wait_for_selector(selectors, timeout=3000)

            html = page.content()
            ctx.close()
            browser.close()
            return html
    except Exception as e:
        logger.error("Playwright render failed for %s: %s", url, e)

    return None


def extract_title(soup: BeautifulSoup) -> str:
    og = soup.select_one('meta[property="og:title"]')
    if og and og.get("content"):
        return og["content"].strip()  # type: ignore
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else "Untitled"


def extract_original_article(soup: BeautifulSoup) -> str | None:
    for selector in ARTICLE_SELECTORS:
        element = soup.select_one(selector)
        if element:
            return str(element)  # HTML string
    return str(soup.body) if soup.body else None


def extract_text(soup: BeautifulSoup) -> str:
    for selector in ARTICLE_SELECTORS:
        element = soup.select_one(selector)
        if element:
            return element.get_text(separator="\n", strip=True)
    return soup.get_text(separator="\n", strip=True)


def extract_date(soup: BeautifulSoup) -> datetime | None:
    # Search for time tags
    time_tag = soup.find("time")
    if time_tag:
        for candidate in (
            time_tag.get("datetime"),
            time_tag.get("content"),
            time_tag.get("title"),
            time_tag.get_text(strip=True),
        ):
            if candidate and (dt := parse_date(str(candidate))):
                return dt

    # Search for publication classes/ids
    publish_like_css = '[id*="publi" i], [class*="publi" i]'
    seen = set()
    nodes = list(soup.select(publish_like_css))

    uniq_nodes = []
    for n in nodes:
        if id(n) not in seen:
            seen.add(id(n))
            uniq_nodes.append(n)

    # Search for typical attributes and text content
    for el in uniq_nodes:
        for attr in ("datetime", "content", "data-published", "data-pubdate", "data-date", "title"):
            val = el.get(attr)
            if val and (dt := parse_date(val)):
                return dt
        txt = el.get_text(strip=True)
        if txt and (dt := parse_date(txt)):
            return dt

    # Search all elements text content
    for el in soup.find_all(True):
        text = el.get_text(strip=True)
        if text and len(text) <= 80:
            if dt := parse_date(text):
                return dt

    return None
