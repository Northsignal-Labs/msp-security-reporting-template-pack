# Northsignal Labs release decision note

Updated: 2026-07-25T10:32:48Z
Status: local-only decision aid; not published; no account, contact, spend, payment workflow, analytics, or public upload added.

## Purpose

This note maps the current aligned local release gate into an explicit reviewer go/no-go decision for a future approved no-spend static channel. It is intentionally operational: it does not grant approval, create a public channel, collect money, or replace human review.

## Current local decision

**Recommendation: HOLD for public release until an approved non-personal free channel and public URL exist.**

The package is locally release-ready, but the public action is still blocked because no approved free channel, account metadata review, live URL, or completed `APPROVAL-HANDOFF.md` approval set exists. The safest autonomous action is therefore to keep improving the local package and rerun the gates after each change.

## Go criteria before any future public upload

A reviewer can treat the package as eligible for a no-spend static upload only if all items below are true:

1. `release_gate_alignment.state` is `aligned` in `status.json` after the final file change.
2. `release_readiness.telemetry_regression_alert.state` is `clean` after the final telemetry run.
3. `tools/pre_publication_check.py` reports 0 errors and 0 warnings.
4. `tools/stage_release.py` stages exactly the manifest-approved files with 0 forbidden files.
5. `tools/review_staged_release.py` reports 0 errors and 0 warnings.
6. `RELEASE-SUMMARY.md`, `RELEASE-RISK-DIGEST.md`, `RELEASE-MANIFEST.json`, and `dist/STAGED-RELEASE-MANIFEST.json` agree on version, file count, staged-review command, and local-only boundary.
7. A free public channel is explicitly approved and can use Northsignal Labs honestly as a small independent automation lab.
8. The public URL is known, all required fields in `APPROVAL-HANDOFF.md` / `APPROVAL-HANDOFF-FIELDS.json` are supplied, `tools/validate_approval_handoff.py` reports 0 errors, and `robots.txt` / `sitemap.xml` have been updated away from `northsignal-labs.local` only after approval using `PUBLIC-URL-CUTOVER-CHECKLIST.md`.
9. Public repository/account metadata does not expose any private individual, private contact detail, private account, or invented human founder.
10. No paid service, purchase, ads, domain, subscription, payout, tax, KYC, payment workflow, tracking script, contact form, or active monetization link is added autonomously.
11. Claims remain template-oriented and operational, not legal, insurance, brokerage, compliance, audit, certification, Microsoft-affiliation, customer, partnership, testimonial, revenue, or professional-services claims.

## No-go triggers

Do not publish if any of the following are true:

- Any gate reports an error, warning, count mismatch, forbidden file, stale staged file, or non-aligned release state.
- The only available channel requires a personal account, paid commitment, paid marketplace, public personal attribution, or unclear ownership metadata.
- A public URL is unknown but `robots.txt` or `sitemap.xml` would need to be live.
- Payment, payout, sponsorship, or monetization setup is required before publication.
- Any asset wording implies regulated advice, affiliation, credentials, customer outcomes, or services that Northsignal Labs has not actually provided.

## Minimal reviewer action path

From `/opt/data/business-dashboard/autonomous-lab`:

```bash
python3 tools/validate_approval_handoff.py
python3 tools/write_release_readiness_telemetry.py
python3 tools/compare_release_readiness_telemetry.py
python3 tools/stage_release.py
python3 tools/review_staged_release.py
```

Then review, in this order:

1. `RELEASE-DECISION-NOTE.md`
2. `RELEASE-RISK-DIGEST.md`
3. `RELEASE-SUMMARY.md`
4. `PUBLICATION-CHECKLIST.md`
5. `DISTRIBUTION-READINESS-SCOREBOARD.md`
6. `APPROVAL-HANDOFF.md`
7. `APPROVAL-HANDOFF-FIELDS.json` and `tools/validate_approval_handoff.py`
8. `PUBLIC-URL-CUTOVER-CHECKLIST.md`
9. `GITHUB-PAGES-SETUP.md` or the notes for the approved free channel
10. `dist/STAGED-RELEASE-MANIFEST.json`
11. The staged `dist/` files themselves

## Revenue interpretation

This decision note improves revenue readiness by reducing review friction: it turns a clean local build into a concrete hold/go decision. It does not make the project revenue-active. The next no-spend revenue step remains selecting an approved privacy-safe channel using `DISTRIBUTION-READINESS-SCOREBOARD.md`, completing the required approval fields in `APPROVAL-HANDOFF.md` and `APPROVAL-HANDOFF-FIELDS.json`, validating them with `tools/validate_approval_handoff.py`, then using `PUBLIC-URL-CUTOVER-CHECKLIST.md` for the local sitemap/robots host switch after approval, then public signal validation through that approved channel, followed later by compliant monetization only if account, payout, identity, and risk constraints are resolved.
