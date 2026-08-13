# Northsignal Labs repository metadata handoff

Status: local-only launch metadata; not published; no account, upload, contact, analytics, payment workflow, or spend.

## Purpose

This page gives a future reviewer copy/paste-safe public repository metadata for the MSP Security Reporting Template Pack after a concrete no-spend, non-personal public channel and HTTPS URL are approved. It reduces approval-to-launch delay and keeps the first public impression focused on measurable aggregate demand signals: stars/forks/watchers/open issues, labeled template requests, and non-binding labeled commercial-fit issues. The same handoff is available in machine-readable form as `REPOSITORY-METADATA.json` so a reviewer can compare repository settings without retyping free-form copy.

## Recommended repository settings

- **Repository display name:** `Northsignal Labs MSP Security Reporting Template Pack`
- **Short description:** `Free MSP/client security reporting templates and local generators for monthly reports, NIS2 evidence scoping, M365 Secure Score summaries, cyber-insurance evidence, and vCISO QBRs.`
- **Visibility:** public only after `APPROVAL-HANDOFF-FIELDS.json` validates a concrete no-spend, non-personal channel and reviewer approval.
- **Homepage URL:** use the approved HTTPS `public_base_url` only after local sitemap/robots cutover has been applied and release gates rerun.
- **Topics/tags:** `msp`, `cybersecurity`, `security-reporting`, `m365`, `nis2`, `vciso`, `qbr`, `templates`, `static-site`, `python`
- **License selector:** MIT License; keep `LICENSE` in the root with Northsignal Labs attribution.
- **Issues:** enabled only with `.github/ISSUE_TEMPLATE/config.yml` present so blank issues remain disabled and feedback routes through public-safe templates.
- **Labels:** create or import the labels in `.github/labels.yml` before launch so `template-request`, `commercial-fit`, and `demand-signal` issue-template signals can be counted in aggregate by `tools/collect_public_signal_snapshot.py`.
- **Discussions/Wiki/Projects:** leave disabled for first validation unless separately approved; they add moderation surface before signal exists.
- **Sponsorships/funding:** disabled; do not add `FUNDING.yml`, payment links, quote requests, invoice paths, commission links, or partner-tracking links.

## Machine-readable metadata

Use `REPOSITORY-METADATA.json` as the copy/paste-safe source of truth for the display name, short description, topics, pinned launch copy, issue/label/Pages settings, aggregate first-validation metrics, and forbidden pre-approval workflows. It is intentionally local/static metadata only: it does not approve a public URL, create an account, call GitHub, upload files, add analytics/forms/contact capture, create payment/KYC/quote/invoice/sales workflows, or spend money.

## Pinned launch copy

Use this concise summary in a release description, repository about text, or first approved no-spend resource share:

> Northsignal Labs MSP Security Reporting Template Pack v0.1 is a static, no-tracking set of MSP/client-facing security reporting templates plus local Python generators. It includes monthly security reporting, NIS2 evidence scoping, M365 Secure Score executive summaries, cyber-insurance evidence preparation, and vCISO QBR planning. Use the files locally, fork/copy under MIT, and request the next useful template through the structured GitHub issue templates without sharing client names, credentials, personal contact details, or confidential information.

## Search/social preview guidance

- Lead with "Free MSP Security Reporting Template Pack" rather than the lab name alone.
- Mention "templates + local generators" in the first sentence; that is the clearest differentiator versus a generic checklist.
- Avoid professional-service, compliance, insurance, Microsoft-affiliation, customer, certification, partnership, revenue, or outcome-guarantee claims.
- Do not use a founder/person profile photo or personal biography. If a logo/avatar is needed, use a neutral Northsignal Labs mark only after approval.

## First-validation measurement checklist

After approved launch, measure only aggregate public signals:

1. Repository stars, forks, watchers, open issue counts, `template-request` issue counts, and `commercial-fit` issue counts via `tools/collect_public_signal_snapshot.py`.
2. Confirm `.github/labels.yml` labels exist in the approved repository before measuring; missing labels would undercount the highest-intent request/commercial-fit signal.
3. Treat template-request and commercial-fit labels as aggregate counts only, without collecting issue authors, private text, emails, client names, or confidential details.
4. Manual aggregate counters only if the approved platform exposes public-safe integer counts without private visitor tracking; do not add download, clone, release, referrer, or visitor analytics just to fill a metric.
5. If the approved free channel is not GitHub Pages or the repository counters cannot be derived, use `tools/collect_public_signal_snapshot.py --manual-aggregate manual-aggregate-counters.json` with aggregate-only integer counters after launch; do not record referrers, user handles, emails, issue bodies, IPs, contact details, quote requests, or payment data.
6. Feed the snapshot into `tools/decide_next_revenue_validation_action.py` before doing more asset work or any monetization-path work.

## Guardrails

- No paid domain, hosting, ads, subscription, marketplace, analytics, or promoted post.
- No payout, tax/KYC, checkout, sponsorship, quote, invoice, sales outreach, commission/partner-tracking link, or payment workflow.
- No personal identity exposure, private contact details, invented founder, fake human, customer, testimonial, certification, partnership, or revenue claim.
- No forms, cookies, tracking scripts, newsletter, contact capture, private inbox, or sensitive-data collection.
- No public posting, community sharing, or upload until concrete public-channel fields exist and the release gates pass again.
