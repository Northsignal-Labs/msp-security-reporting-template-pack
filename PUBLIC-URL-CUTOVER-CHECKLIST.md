# Northsignal Labs public-URL cutover checklist

Updated: 2026-07-27T11:25:00Z
Status: local-only cutover aid; use only after an approved no-spend, non-personal public channel and concrete public URL exist. No publishing, account creation, upload, spend, payment workflow, analytics, form, or external contact is authorized by this file.

## Purpose

This checklist defines the narrow file and metadata changes needed when a reviewer has already approved a free public route for the Northsignal Labs MSP Security Reporting Template Pack. It prevents premature replacement of the placeholder host and makes the final URL switch reviewable without linking the project to any private individual.

## Preconditions before using this checklist

Do not start the cutover unless every item below is true:

1. A reviewer has explicitly approved a free public channel for Northsignal Labs.
2. The channel can be used without paid hosting, domain purchase, ads, subscriptions, marketplace fees, payout, tax/KYC setup, analytics scripts, tracking pixels, forms, or active monetization links.
3. The channel/account/repository metadata can present Northsignal Labs honestly as a small independent automation lab without exposing any private individual, private account, private email, personal background, fake founder, credentials, customers, testimonials, partnerships, or revenue claims.
4. The final public base URL is known, stable enough for `robots.txt`, `sitemap.xml`, and generator JSON Schema `$id` references, and does not require a paid custom domain.
5. `RELEASE-DECISION-NOTE.md` still recommends hold until these conditions are satisfied; this checklist does not itself approve publication.
6. `APPROVAL-HANDOFF-FIELDS.json` has been completed and `tools/validate_approval_handoff.py` reports 0 errors for the approved cutover state.

## Cutover steps after approval

Run these steps locally before any upload:

1. Record the approved channel, approved public base URL, approval timestamp, and reviewer initials/handle in private review notes outside the public release package if needed; do not add private personal data to public files.
2. Complete `APPROVAL-HANDOFF-FIELDS.json` and run `python3 tools/validate_approval_handoff.py`; stop unless it reports 0 errors.
3. Dry-run the validator-gated replacement with `python3 tools/perform_public_url_cutover.py`; confirm it reports the approved public base URL and no file changes.
4. Apply the local replacement with `python3 tools/perform_public_url_cutover.py --apply`, which replaces only `https://northsignal-labs.local/` in `sitemap.xml`, `robots.txt`, and generator JSON Schema `$id` references and writes `PUBLIC-URL-CUTOVER-LOG.json` for private review.
5. Confirm every internal link remains relative unless a canonical public URL is explicitly required by the approved channel.
6. Re-check public-facing copy for Northsignal Labs identity only: no private individual, no invented human founder, no personal contact route, no customer/credential/revenue claims.
7. Re-check that referral, payment, contact, analytics, sponsorship, quote, invoice, and sales-workflow paths are absent from first-validation public copy unless a later monetization workflow is separately approved after meaningful aggregate demand signal.
8. Run the release gates from `/opt/data/business-dashboard/autonomous-lab`:

```bash
python3 tools/validate_approval_handoff.py
python3 tools/write_release_readiness_telemetry.py
python3 tools/compare_release_readiness_telemetry.py
python3 tools/stage_release.py
python3 tools/review_staged_release.py
```

9. Inspect `dist/STAGED-RELEASE-MANIFEST.json` for the final file count, byte counts, and SHA-256 hashes.
10. Inspect the staged `dist/robots.txt`, `dist/sitemap.xml`, and `dist/schemas/*.schema.json` `$id` values and confirm they contain the approved URL, not `northsignal-labs.local`.
11. Confirm `status.json` reports `release_readiness.telemetry_regression_alert.state=clean` and `release_readiness.release_gate_alignment.state=aligned` after the cutover.
12. Only then can a reviewer consider copying the staged static files to the approved free channel.

## Rollback / no-go triggers

Stop and keep the release local if any of the following occurs:

- The approved public URL is unclear, unstable, personal, paid, or unavailable.
- The channel requires personal attribution, private account metadata exposure, payment setup, analytics, tracking scripts, contact forms, marketplace settings, or paid add-ons.
- Any checker, telemetry, staging, staged-review, or alignment step reports an error, warning, mismatch, stale file, forbidden file, or regression.
- `robots.txt`, `sitemap.xml`, or any `schemas/*.schema.json` `$id` contains a non-approved public URL or stale `northsignal-labs.local` value after an approved cutover.
- Public-facing copy implies legal, insurance, brokerage, compliance, audit, certification, Microsoft affiliation, professional services, credentials, customers, testimonials, partnerships, or revenue claims.

## Current autonomous conclusion

This file improves release readiness but does not change the current public-release decision. Until a reviewer approves a non-personal no-spend channel and public URL, keep `northsignal-labs.local` in `robots.txt`, `sitemap.xml`, and generator JSON Schema `$id` references, keep the package local, and continue using `DISTRIBUTION-READINESS-SCOREBOARD.md`, `RELEASE-DECISION-NOTE.md`, and the local release gates for review.
