# First 7-day validation plan — Northsignal Labs MSP Security Reporting Template Pack

Status: post-approval only. This plan is local-only until the reviewer supplies a concrete approved no-spend public URL/account target and the release gates pass after URL cutover.

## Purpose

This plan turns the first approved public week into measurable demand validation instead of vague publishing. It is designed to answer one revenue question quickly: does a privacy-safe public release produce enough aggregate interest in MSP/security reporting templates to justify the next no-spend monetization-learning step?

## Guardrails

- Use only the approved non-personal Northsignal Labs public channel and HTTPS URL.
- Do not buy domains, hosting, ads, tools, marketplace placements, subscriptions, or analytics.
- Do not create payout, tax/KYC, paid listing, quote, invoice, sponsorship, referral-link, purchase, or sales workflows.
- Do not collect emails, IP addresses, usernames for outreach, issue bodies/comments, client names, logs, screenshots, credentials, vulnerability details, private security information, contact details, regulated information, or confidential data.
- Do not invent customers, testimonials, founder identity, certifications, partnerships, revenue, or professional-service claims.
- Treat template-request and commercial-fit issues as public, non-binding aggregate signal only.

## Day 0: launch preflight after approval

1. Complete `APPROVAL-HANDOFF-FIELDS.json` with the approved channel, concrete HTTPS public URL ending in `/`, account/repository display name, metadata constraints, no-spend/no-financial/no-data-collection confirmations, claims/identity approval, and final reviewer.
2. Run `python3 tools/validate_approval_handoff.py` and require `ready_for_reviewer_cutover` before any host replacement.
3. Run `python3 tools/perform_public_url_cutover.py` as a dry run, then `python3 tools/perform_public_url_cutover.py --apply` only if the dry run changes only approved public URL references in `sitemap.xml`, `robots.txt`, and generator JSON Schema `$id` values.
4. Rerun the final gate sequence: approval validation, GitHub labels/workflow validation if applicable, pre-publication check, staging, localhost smoke test via telemetry, staged review, ZIP packaging, launch-packet sync, and bundle validation.
5. Confirm the fresh `GO-LIVE-PACKAGE.json` file count, byte size, SHA-256, and ZIP verification errors=0 before upload.
6. For GitHub, create or verify the exact labels in `.github/labels.yml` before interpreting request/commercial-fit counts.

## Day 1: publish and baseline

- Publish only the verified static package through the approved no-spend channel.
- Fill repository/about metadata from `REPOSITORY-METADATA.md`.
- Run `python3 tools/smoke_test_public_url.py` after the reviewer-controlled upload so the approved HTTPS URL is checked for allowlisted public paths, placeholder leakage, forms, analytics, payment, and contact-capture risk before any signal is interpreted.
- Confirm these public paths load: `index.html`, `README.md`, `DOWNLOAD.md`, `msp-monthly-security-report-template.html`, `.github/ISSUE_TEMPLATE/template-request.yml`, `.github/ISSUE_TEMPLATE/commercial-fit-signal.yml`, `LICENSE`, `SECURITY.md`, and `CONTRIBUTING.md`.
- Record a baseline aggregate snapshot with `tools/collect_public_signal_snapshot.py` for GitHub or guarded manual aggregate mode for an approved equivalent channel.
- Run `tools/decide_next_revenue_validation_action.py` and keep the decision even if all counters are zero.

## Days 2–3: passive signal check

- Check aggregate stars, forks, watchers, open issues, template-request label count, and commercial-fit label count only.
- Do not inspect or store issue bodies, usernames, emails, client names, logs, screenshots, IPs, referrers, or comments.
- If there is no signal, do not build more assets yet; improve distribution metadata or one approved public-safe resource description instead.

## Days 4–5: one careful free-channel share only if appropriate

Only if the approved public page is live and the venue rules clearly allow resource sharing:

- Use one transparent snippet from `DISTRIBUTION-MESSAGE-BANK.md`.
- Share in one directly relevant, non-personal, non-spam venue.
- Do not direct-message people, scrape contacts, post repeatedly, use fake accounts, imply endorsement, or add tracking parameters.
- Ask for public-safe template requests, not private security details or sales conversations.

If no compliant venue is obvious, skip posting and keep measurement passive.

## Day 7: decision rules

Run `tools/collect_public_signal_snapshot.py` and `tools/decide_next_revenue_validation_action.py` again, then choose exactly one next step:

| Aggregate signal | Meaning | Next no-spend action |
|---|---|---|
| 0 stars/forks/issues/requests/commercial-fit signals | No visible demand yet | Improve repository metadata, title/description, README opening, and one approved distribution surface; do not add monetization or more product scope. |
| Any stars/forks/watchers but no request/commercial-fit issues | Low-friction interest | Improve the visitor path to `DOWNLOAD.md` and template-request issue flow; consider one clearer example/output. |
| 1+ template-request issues | Direct demand | Prioritize the most repeated requested template/generator as the next free asset or local generator improvement. |
| 1+ commercial-fit signals | Monetization-learning signal | Draft a no-spend monetization-learning recommendation only; do not create payment/KYC/quote/invoice/sales workflows without separate explicit approval. |
| Multiple template-request/commercial-fit signals | Stronger validation | Recommend the smallest paid-path experiment for reviewer approval, likely manual B2B pilot, paid template pack, or expanded generator bundle, with exact approval requirements and no autonomous financial setup. |

## Dashboard fields to update after each run

- `post-launch-signal-snapshot.json`: aggregate counters only.
- `revenue-validation-decision.json`: weighted score, decision state, recommended next action.
- `status.json`: publication state, latest verified package, aggregate signal, decision state, and remaining blockers.
- `activity-dashboard-data.json`: regenerate after status changes so the dashboard shows current distance to revenue.

## Success metric for week 1

A successful first week is not revenue collection. It is one of:

- public package live with clean aggregate baseline and no guardrail violations;
- at least one fork/star/watch/open issue showing initial interest;
- at least one public-safe template request;
- at least one non-binding commercial-fit signal that justifies a concrete monetization-learning approval request.

If none occur, the next money-first action is distribution/positioning validation, not internal polish or payment setup.
