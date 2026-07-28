# Approved GitHub Pages launch runbook

Status: post-approval handoff only. This file does not approve a public URL, create an account, upload files, run GitHub Actions, contact anyone, add analytics/forms, create payment/KYC/quote/invoice workflows, or spend money.

## Purpose

Use this only after the reviewer supplies the concrete non-personal GitHub Pages repository/account and HTTPS `public_base_url` fields in `APPROVAL-HANDOFF-FIELDS.json` and `tools/validate_approval_handoff.py` reaches `ready_for_reviewer_cutover`.

The goal is to turn an approved GitHub Pages channel into measurable no-spend validation quickly: public static package live, structured template-request/commercial-fit hooks working, aggregate counters collectable, and first-week revenue-learning started without personal identity exposure or monetization friction.

## Required inputs before any action

Do not proceed unless all are true:

1. `APPROVAL-HANDOFF-FIELDS.json` contains a real approved HTTPS `public_base_url` ending in `/`.
2. The approved channel is a no-spend, non-personal GitHub Pages repository/account/org for Northsignal Labs.
3. Public account, repository, profile, release, issue-template, and commit metadata do not expose private individual identity/private contact details or invented founder/customer/testimonial/certification/partnership/revenue claims.
4. No paid domain, hosting, ads, subscription, marketplace fee, paid add-on, analytics, forms, newsletter, private inbox, lead capture, payout, tax/KYC, sponsorship, quote, invoice, sales outreach, partner-tracking, commission, or payment workflow is introduced.
5. The reviewer has access to create/verify labels and upload only the manifest-approved static files.

## Day-0 approved launch sequence

Run from `/opt/data/business-dashboard/autonomous-lab` after the approved fields are present:

```bash
python3 tools/validate_approval_handoff.py
python3 tools/perform_public_url_cutover.py
python3 tools/perform_public_url_cutover.py --apply
python3 tools/validate_github_signal_labels.py
python3 tools/validate_github_pages_workflow.py
python3 tools/pre_publication_check.py
python3 tools/stage_release.py
python3 tools/review_staged_release.py
python3 tools/package_go_live_zip.py
python3 tools/validate_public_launch_packet_sync.py
python3 tools/validate_public_release_bundle.py
```

Equivalent guarded local orchestrator after the reviewer confirms the approved URL/account fields:

```bash
python3 tools/run_approved_launch_preflight.py --apply-cutover
```

This still does not upload, create accounts, authenticate, post publicly, collect data, add analytics/forms, start payment/KYC/quote/invoice workflows, or spend money; it only prepares local `dist/`, `public-repo-export/`, `GO-LIVE-PACKAGE.json`, and ZIP artifacts for reviewer-controlled upload.

Healthy result before upload:

- approval validation reaches `ready_for_reviewer_cutover` before public URL reference replacement
- URL cutover changes only `robots.txt`, `sitemap.xml`, and generator JSON Schema `$id` references from `northsignal-labs.local` to the approved HTTPS URL
- GitHub label validation reports 3 declared labels, 3 issue-template labels, 3 required signal labels, 0 errors, 0 warnings
- GitHub Pages workflow validation reports 4 allowed actions, 0 errors, 0 warnings
- pre-publication, staging, staged review, public launch packet sync, and public release bundle validation all report 0 errors and 0 warnings
- `GO-LIVE-PACKAGE.json` and the ZIP checksum are reviewed after the post-cutover package is built

## Repository setup checklist for the approved reviewer

Use only the approved non-personal repository/account:

1. Set repository display/about fields from `REPOSITORY-METADATA.md`.
2. Keep MIT selected and leave `LICENSE` at the root.
3. Import or create labels exactly as listed in `.github/labels.yml` / `GITHUB-LABEL-SETUP.md` before interpreting issue counts.
4. Keep `.github/ISSUE_TEMPLATE/config.yml` so blank issues stay disabled.
5. Keep `.github/workflows/static-pages.yml` only if the approved repository uses GitHub Actions Pages deployment from the static root.
6. Upload/copy only files listed in `RELEASE-MANIFEST.json` or the staged `dist/` folder; do not upload internal status, telemetry, approval packet, generated ZIP metadata, caches, private notes, or cron/dashboard files.
7. Verify GitHub Pages serves `index.html`, `README.md`, `DOWNLOAD.md`, `SAMPLE-OUTPUTS.md`, `LICENSE`, and the five landing pages over the approved HTTPS URL; then run `python3 tools/smoke_test_public_url.py` so placeholder leakage, broken allowlisted paths, forms, analytics, payment, or contact-capture risk is caught before signal collection.

## First measurement after launch

After the approved public URL is live:

```bash
python3 tools/smoke_test_public_url.py
python3 tools/collect_public_signal_snapshot.py
python3 tools/decide_next_revenue_validation_action.py
```

First confirm the live static paths pass the approved-HTTPS smoke check, then measure only aggregate public counts: stars, forks, watchers, open issues, `template-request` issue-label count, and `commercial-fit` issue-label count. Do not collect issue bodies, authors, emails, usernames, IPs, referrers, contact details, client names, confidential/security-sensitive details, quote requests, invoice data, or payment data.

Then follow `FIRST-7-DAY-VALIDATION-PLAN.md`:

- Day 1: record baseline aggregate signal.
- Days 2-6: do no more than one directly relevant, rules-compliant, transparent free-channel resource share if the repository metadata is live and the venue permits it.
- Day 7: rerun the aggregate snapshot and `tools/decide_next_revenue_validation_action.py`; weak/no signal means distribution metadata work, some signal means conversion/request-path improvement, meaningful template-request/commercial-fit signal means monetization-learning research only. Payment/KYC/quotes/invoices/sales workflows still require separate explicit approval.

## Stop conditions

Stop before upload or sharing if any of these appear:

- public URL is missing, placeholder, non-HTTPS, or not approved
- repository/account metadata exposes private individual identity or unsupported claims
- any gate reports errors or unexpected warnings
- the requested setup requires spend, paid add-ons, custom domains, analytics, contact capture, payment/payout/KYC, quotes, invoices, sales outreach, partner-tracking/commission links, or sensitive-data intake
- the ZIP/checksum changed after reviewer approval and has not been rechecked
