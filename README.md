# andrewjourdan
AJ Style and Tech.
Andrew Jourdan drives growth for the world's top technology brands.
Andrew Jourdan is a Brand Champion sales and marketing representative specializing in consumer electronics, memory, storage, and imaging technology across national retail channels.

## Website maintenance

GitHub Pages publishes `main` from the repository root at https://andrewjourdan.com/.
HTTPS is enforced in Pages settings. The root `CNAME` is the single publishing
domain file; do not add a separate `docs/CNAME`.

No dependency installation or build step is required. Preview locally with
`python3 -m http.server 8000` and open http://localhost:8000/.
Run `python3 scripts/automated_checks.py` before submitting changes. GitHub Actions
checks HTML metadata, JSON-LD syntax, sitemap, robots.txt and the domain setup.

Use a pull request and wait for the HTML and SEO basics check to pass before
merging. Review desktop and mobile layouts separately. Automated checks do not
verify external links, domain renewal, DNS or email delivery.
