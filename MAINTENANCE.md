# Website maintenance

## Repository contents

| File | Purpose |
| --- | --- |
| `index.html` | Single-page website with embedded styles and JavaScript. Google Fonts are loaded externally. |
| `CNAME` | GitHub Pages custom domain: `andrewjourdan.com`. |
| `robots.txt` | Crawler instructions and sitemap reference. |
| `sitemap.xml` | Published sitemap containing the homepage. |
| `scripts/automated_checks.py` | Dependency-free checks for the site's metadata and publishing files. |
| `.github/workflows/automated-checks.yml` | GitHub Actions workflow that runs the checks. |
| `.github/workflows/README.md` | Additional explanation of the automated checks. |
| `SECURITY.md` | Security reporting policy. |

## Hosting and contact

GitHub Pages publishes the root of `main` at https://andrewjourdan.com/.
HTTPS is enforced in Pages settings. No dependency installation or build step is
required. Keep the root `CNAME` as the single publishing-domain file; the automated
checks reject an additional `docs/CNAME`.

The website's contact links open the visitor's email app. This repository does not
contain a contact-form submission backend. The separate NTI Sales form and its
Cloudflare Worker are maintained in `andrewjourdan/ntisales`.

## Local preview

From the repository root, run:

```sh
python3 -m http.server 8000
```

Open http://localhost:8000/. Stop the preview with Ctrl+C. Loading the external
Google Fonts requires an internet connection.

## Validation and publishing

Run:

```sh
python3 scripts/automated_checks.py
```

The script checks:

- The homepage has an HTML5 doctype, language, title, description and expected canonical URL.
- At least one JSON-LD block is present, and each block parses as JSON.
- The sitemap is well-formed XML, includes the homepage and uses HTTPS URLs.
- `robots.txt` references the expected sitemap.
- `CNAME` matches the canonical domain and `docs/CNAME` is absent.

The **Automated Site Checks** workflow runs on pull requests, pushes to `main`, and
manual dispatches. The branch rules require a pull request and the **HTML and SEO
basics** check to pass before merging.

These are baseline checks, not a full HTML validator, structured-data schema
validator, accessibility audit or live link checker. Review desktop and mobile
layouts and contact links separately. DNS, domain renewal, HTTPS certificate
status and actual email delivery require separate verification.
