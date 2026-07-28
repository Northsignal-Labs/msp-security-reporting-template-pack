# Northsignal Labs approval handoff

Updated: 2026-07-27T11:25:00Z
Status: local-only reviewer handoff; not published; no account, contact, spend, upload, payment workflow, tracking script, form, or public posting added.

## Purpose

This note defines the minimum approval details a reviewer must provide before Hermes can perform the local public-URL cutover workflow for the Northsignal Labs MSP Security Reporting Template Pack. It is paired with `APPROVAL-HANDOFF-FIELDS.json` and `tools/validate_approval_handoff.py`, which provide a machine-readable preflight for the same approval set. This is a handoff checklist only: it does not approve a channel, create an account, publish files, collect leads, or enable monetization.

## Required reviewer-supplied details

A future public release should remain on hold until all fields below are supplied and explicitly approved:

| Field | Required value before local URL cutover | Why it matters |
|---|---|---|
| Approved channel | Name of the free static route to use, such as an approved non-personal GitHub Pages org/account | Prevents autonomous account creation or unreviewed public posting |
| Public base URL | Exact HTTPS base URL that should replace `https://northsignal-labs.local/` in `sitemap.xml`, `robots.txt`, and generator JSON Schema `$id` references | Avoids publishing placeholder discovery metadata and stale schema identifiers |
| Account/repository display name | Public-facing name, preferably `Northsignal Labs`, with no private individual identity or invented founder | Keeps the outward identity honest and non-personal |
| Account/repository metadata constraints | Approved owner/org name, repository name, description, profile text, commit author policy, and allowed contact fields | Reduces accidental personal metadata exposure |
| Spend confirmation | Explicit confirmation that the route requires no paid domain, hosting, ads, subscription, marketplace fee, paid add-on, or other purchase | Preserves the no-spend mandate |
| Financial-workflow confirmation | Explicit confirmation that no payout, tax/KYC, checkout, sponsorship, active monetization link, or paid listing is required for publication | Avoids financial risk and premature revenue plumbing |
| Data-collection confirmation | Explicit confirmation that no analytics script, cookie banner, contact form, newsletter signup, private inbox, or lead-capture workflow is required | Keeps first release privacy-safe and static-only |
| Claims/identity approval | Confirmation that Northsignal Labs may be described only as a small independent automation lab and must not claim customers, credentials, partnerships, testimonials, founder identity, or revenue | Prevents misleading public claims |
| Final reviewer | Person or role responsible for confirming the staged manifest and public metadata before upload | Ensures the last step is reviewed before public action |

## Local action Hermes may take after approval

Only after every required field is approved and `tools/validate_approval_handoff.py` reports 0 errors, Hermes may perform the filesystem-only steps in `PUBLIC-URL-CUTOVER-CHECKLIST.md`:

1. Replace only the placeholder host in `sitemap.xml`, `robots.txt`, and generator JSON Schema `$id` references with the approved public base URL.
2. Rerun `tools/write_release_readiness_telemetry.py` and `tools/compare_release_readiness_telemetry.py`.
3. Rerun `tools/stage_release.py` and `tools/review_staged_release.py`.
4. Inspect `dist/STAGED-RELEASE-MANIFEST.json` for the expected file count, SHA-256 hashes, and absence of forbidden files.
5. Inspect staged `dist/robots.txt`, `dist/sitemap.xml`, and `dist/schemas/*.schema.json` `$id` values for the approved public URL before any reviewer-controlled upload.
6. Keep publication on hold if any gate reports an error, warning, mismatch, forbidden file, personal metadata concern, spend requirement, financial-workflow requirement, tracking/form requirement, stale schema identifier, or claims-risk issue.

## Current hold state

No approved channel, public URL, or account metadata constraints have been supplied in this run. Therefore the current decision remains: **hold public release; keep the package local-only.**

Machine-readable state: `APPROVAL-HANDOFF-FIELDS.json` currently has `approved_for_cutover=false`, blank channel/URL/metadata/reviewer fields, and false confirmation booleans. A validator run should therefore pass only as a hold-state check, not as release approval.
