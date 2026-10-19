#!/usr/bin/env python3
"""Dependency-free checks for the site's core HTML and SEO files."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://andrewjourdan.com"
errors = []

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title = ""
        self.description = ""
        self.canonical = ""
        self.title_open = False
        self.json_open = False
        self.json_buffer = ""
        self.json_blocks = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang") or ""
        if tag == "title": self.title_open = True
        if tag == "meta" and (a.get("name") or "").lower() == "description":
            self.description = a.get("content") or ""
        if tag == "link" and "canonical" in (a.get("rel") or "").lower().split():
            self.canonical = a.get("href") or ""
        if tag == "script" and a.get("type") == "application/ld+json":
            self.json_open, self.json_buffer = True, ""
    def handle_endtag(self, tag):
        if tag == "title": self.title_open = False
        if tag == "script" and self.json_open:
            self.json_blocks.append(self.json_buffer)
            self.json_open = False
    def handle_data(self, data):
        if self.title_open: self.title += data
        if self.json_open: self.json_buffer += data

def fail(message):
    errors.append(message)
    print("FAIL:", message)

def check_html():
    path = ROOT / "index.html"
    if not path.is_file():
        fail("index.html is missing"); return
    source = path.read_text(encoding="utf-8")
    if not source.lstrip().lower().startswith("<!doctype html>"):
        fail("index.html should start with an HTML5 doctype")
    page = Inspector()
    try:
        page.feed(source); page.close()
    except Exception as exc:
        fail(f"index.html parsing failed: {exc}"); return
    if not page.lang.strip(): fail("html element is missing lang")
    if not page.title.strip(): fail("page title is missing")
    if not page.description.strip(): fail("meta description is missing")
    elif len(page.description) > 320: fail("meta description exceeds 320 characters")
    if page.canonical != BASE + "/": fail(f"canonical URL should be {BASE}/")
    if not page.json_blocks: fail("JSON-LD structured data is missing")
    for i, block in enumerate(page.json_blocks, 1):
        try: json.loads(block)
        except json.JSONDecodeError as exc: fail(f"JSON-LD block {i} is invalid: {exc}")

def check_sitemap():
    path = ROOT / "sitemap.xml"
    if not path.is_file(): fail("sitemap.xml is missing"); return
    try: root = ElementTree.parse(path).getroot()
    except ElementTree.ParseError as exc: fail(f"sitemap.xml is invalid XML: {exc}"); return
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [n.text.strip() for n in root.findall(".//sm:loc", ns) if n.text and n.text.strip()]
    if not urls: fail("sitemap.xml must contain at least one loc URL")
    if BASE + "/" not in urls: fail(f"sitemap must include {BASE}/")
    for url in urls:
        if not url.startswith("https://"): fail(f"sitemap URL must use HTTPS: {url}")

def check_robots():
    path = ROOT / "robots.txt"
    if not path.is_file(): fail("robots.txt is missing"); return
    lines = [line.split(":", 1)[1].strip() for line in path.read_text(encoding="utf-8").splitlines()
             if line.strip().lower().startswith("sitemap:")]
    if BASE + "/sitemap.xml" not in lines: fail(f"robots.txt must reference {BASE}/sitemap.xml")

if __name__ == "__main__":
    print("Running static-site automated checks…")
    check_html(); check_sitemap(); check_robots()
    if errors:
        print(f"\\n{len(errors)} check(s) failed.")
        sys.exit(1)
    print("PASS: HTML SEO metadata, JSON-LD syntax, sitemap XML, and robots.txt sitemap reference.")
