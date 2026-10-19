# Automated Checks

This directory contains the GitHub Actions workflow for routine static-site checks.

## What runs

The `Automated Site Checks` workflow runs for pull requests, pushes to `main`, and manual dispatches. It uses read-only repository permissions and runs `scripts/automated_checks.py` without installing third-party Python packages.

The script checks:
- `index.html` has an HTML5 doctype, language, title, meta description, and expected canonical URL.
- Embedded JSON-LD structured data is valid JSON.
- `sitemap.xml` is well-formed XML, includes the homepage, and lists HTTPS URLs.
- `robots.txt` points to the site's sitemap.

These are baseline regression checks, not a full HTML validator, live link crawler, vulnerability scanner, or a guarantee of search ranking. A failed check should be reviewed before merging.
