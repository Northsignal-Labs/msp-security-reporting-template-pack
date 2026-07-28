# Privacy-safe GitHub Pages setup notes

Purpose: local, no-spend setup notes for a future approved Northsignal Labs static release. These notes do not create accounts, publish files, buy domains, enable paid services, or collect visitor data.

> Operational-use notice: this repository would share templates and local automation aids only. It must not present legal, insurance, audit, certification, vendor-affiliated, or professional-services advice.

## Recommended release shape

- Use the outward project identity **Northsignal Labs**.
- Use a repository dedicated to the template pack, for example `northsignal-labs-msp-security-template-pack`.
- Publish only static files listed in `RELEASE-MANIFEST.json`.
- Keep `.nojekyll` at the repository root so GitHub Pages serves the manifest-approved static pack directly instead of running Jekyll processing.
- Keep `.github/workflows/static-pages.yml` only in the approved non-personal repository if the reviewer wants GitHub Actions to deploy Pages from the static repository root; validate it with `python3 tools/validate_github_pages_workflow.py` before upload.
- Keep generated samples synthetic and clearly marked as examples.
- Keep `status.json`, caches, bytecode, private notes, dashboard telemetry, and local cron history out of the public repository.
- Do not add payment links, affiliate links, forms, analytics scripts, email capture, tracking pixels, or paid add-ons.

## Privacy and identity requirements before any public push

- Confirm that the account or organization can be operated under the Northsignal Labs project identity without exposing a private individual in public profile text.
- Do not invent a human founder, employee, customer, testimonial, credential, partner, or certification.
- Use neutral attribution such as: "Northsignal Labs is a small independent automation lab sharing free operational templates and local tooling."
- Review public commit metadata before release. If commits are made, author name and email should be project-safe and approved; no private personal metadata should be exposed.
- Do not connect a custom domain unless a no-spend domain path is explicitly approved later. The current sitemap/robots/schema `$id` host must remain a placeholder until a real public URL is approved.

## Static repository layout

```text
/
  README.md
  .nojekyll
  index.html
  robots.txt
  sitemap.xml
  asset-scores.json
  CHANGELOG.md
  PUBLISHING-ROUTES.md
  PUBLICATION-CHECKLIST.md
  RELEASE-MANIFEST.json
  CONTRIBUTING.md
  SIGNAL-TRACKING.md
  GITHUB-PAGES-SETUP.md
  .github/workflows/static-pages.yml
  msp-monthly-security-report-template.html
  nis2-readiness-checklist.html
  m365-secure-score-executive-report-template.html
  cyber-insurance-evidence-checklist.html
  vciso-qbr-agenda-template.html
  assets/
  .github/ISSUE_TEMPLATE/
  generated/
  samples/
  schemas/
  tools/
```

## Pre-release local checklist

1. Confirm no public file contains private identity, personal account, or private contact details.
2. Confirm `robots.txt`, `sitemap.xml`, and generator JSON Schema `$id` values still use the placeholder host unless a real public URL is approved.
3. Run `python3 tools/pre_publication_check.py` from inside the `autonomous-lab` tree or by absolute path.
4. Review any warnings manually. Do not publish if errors remain.
5. Copy only manifest-approved files to the public repository.
6. Run `python3 tools/validate_github_pages_workflow.py` if the GitHub Pages workflow will be included in the approved repository.
7. Open `index.html` locally and verify the five landing pages and downloads work with relative links.
8. If a public channel is approved, update only `sitemap.xml`, `robots.txt`, and generator JSON Schema `$id` discovery references through `tools/perform_public_url_cutover.py` after the final URL is known, then rerun the release gates.

## Suggested repository description

Free MSP/cybersecurity reporting templates and local automation aids from Northsignal Labs, a small independent automation lab. Static, no-spend, operational-use resources; not legal, insurance, audit, certification, or vendor-affiliated advice.

## Minimal first public release note

Northsignal Labs MSP Security Reporting Template Pack v0.1 includes five static MSP/cybersecurity workflow assets and three local JSON-to-Markdown/HTML generator examples. It is designed for offline operational use, with no tracking, forms, no payment links, no affiliate links, or paid dependencies.
