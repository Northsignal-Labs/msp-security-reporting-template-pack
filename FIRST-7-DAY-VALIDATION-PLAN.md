# First 7-day validation plan — Northsignal Labs MSP Security Reporting Template Pack

Status: live public validation. GitHub Pages is already live at `https://northsignal-labs.github.io/msp-security-reporting-template-pack/`; the remaining high-ROI blocker is one concrete approved no-spend external/manual post path, followed by 24–48h aggregate-only measurement.

## Purpose

This plan turns the first approved public week into measurable demand validation instead of vague publishing. It is designed to answer one revenue question quickly: does a privacy-safe public release produce enough aggregate interest in MSP/security reporting templates to justify the next no-spend monetization-learning step?

## Guardrails

- Use only the approved non-personal Northsignal Labs public channel and HTTPS URL.
- Do not buy domains, hosting, ads, tools, marketplace placements, subscriptions, or analytics.
- Do not create payout, tax/KYC, paid listing, quote, invoice, sponsorship, referral-link, purchase, or sales workflows.
- Do not collect emails, IP addresses, usernames for outreach, issue bodies/comments, client names, logs, screenshots, credentials, vulnerability details, private security information, contact details, regulated information, or confidential data.
- Do not invent customers, testimonials, founder identity, certifications, partnerships, revenue, or professional-service claims.
- Treat template-request and commercial-fit issues as public, non-binding aggregate signal only.

## Day 0: launch preflight after approval — completed for the live GitHub Pages route

1. Completed: `APPROVAL-HANDOFF-FIELDS.json` contains the approved GitHub Pages target and guardrail confirmations.
2. Completed: public URL smoke tests have passed against the live HTTPS Pages URL.
3. Completed: aggregate-only GitHub signal collection is available through `tools/collect_public_signal_snapshot.py`.
4. Still open: the prepared visitor-copy improvement is local-only until RP/reviewer pushes commit `f840c22` or restores approved non-personal repository write access.
5. Still open: active validation needs exactly one approved external/manual post path in `EXTERNAL-DISTRIBUTION-VENUE-APPROVAL-REQUEST.md`; do not post elsewhere or retry blocked venues without that concrete approval.
6. For GitHub signal interpretation, continue using aggregate counts only from stars/forks/watchers/open issues and labeled `template-request` / `commercial-fit` issues.

## Day 1: publish and baseline — completed

- Public GitHub Pages route is live and has passed the public URL smoke test.
- Baseline aggregate snapshot has been recorded and currently remains zero.
- `tools/decide_next_revenue_validation_action.py` keeps the current state as `weak_or_no_signal_prioritize_distribution_metadata`, which means distribution/positioning validation is higher ROI than more templates or payment setup.

## Days 2–3: passive signal check

- Check aggregate stars, forks, watchers, open issues, template-request label count, and commercial-fit label count only.
- Do not inspect or store issue bodies, usernames, emails, client names, logs, screenshots, IPs, referrers, or comments.
- If there is no signal, do not build more assets yet; improve distribution metadata or one approved public-safe resource description instead.

## Days 4–5: one careful free-channel share only after concrete dashboard approval

Only if the approved public page is live, the venue rules clearly allow resource sharing, and `external-distribution-venue-access` has a completed approval/change note naming one concrete venue/account/manual-post path:

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
