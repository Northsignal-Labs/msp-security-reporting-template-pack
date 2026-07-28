# Lightweight manual signal tracking notes

Purpose: define safe, no-spend measurements for a future approved public Northsignal Labs static release. This file is a local planning asset only; it does not enable analytics, contact forms, payments, affiliate links, cookies, tracking pixels, or external publishing.

## Measurement principles

- Prefer platform-native public counters and manual observations over tracking scripts.
- Do not collect personal data, client data, email addresses, IP addresses, or uploaded files.
- Do not add analytics services unless a privacy-safe free account/channel is explicitly approved later.
- Keep all measurements aggregate and directional; the goal is to decide which asset deserves the next autonomous improvement.
- Treat any monetization signal as exploratory until payout/KYC/payment constraints are explicitly resolved.

## Manual weekly metrics to record after a public release

| Metric | Source | Frequency | Why it matters | Risk control |
|---|---|---:|---|---|
| Repository stars | Public repository UI | Weekly | Lightweight usefulness/bookmark signal | Public aggregate only |
| Repository forks | Public repository UI | Weekly | Reuse signal for templates/tools | Public aggregate only |
| Repository watchers | Public repository UI | Weekly | Ongoing interest signal | Public aggregate only |
| Template-request issues | Public repository label count (`template-request`) | Weekly | Direct request signal for the next template/generator | Count labels only; do not collect issue authors, bodies, comments, or contact details |
| Commercial-fit issues | Public repository label count (`commercial-fit`) | Weekly | Non-binding signal for future monetization path selection | Count labels only; do not treat as purchase, quote, invoice, or sales lead |
| Asset workflow labels | Public repository label counts for `asset:msp-monthly-report`, `asset:nis2-readiness`, `asset:m365-secure-score`, `asset:cyber-insurance-evidence`, and `asset:vciso-qbr` | Weekly | Identifies which workflow deserves the next no-spend conversion or monetization-learning step | Count label totals only; do not read or store issue bodies, usernames, emails, contact details, or client/private data |

## Simple scorecard

Score each asset from 0 to 3 per week:

- 0 = no observable signal
- 1 = weak signal, such as one star, fork, watcher, open issue, template request, commercial-fit signal, or public mention
- 2 = repeated signal from more than one source
- 3 = strongest weekly signal or direct request for that asset type

Assets to score:

1. MSP monthly security report template
2. NIS2 readiness checklist
3. M365 Secure Score executive report template and generator
4. Cyber-insurance evidence checklist and gap-register generator
5. vCISO QBR agenda template

## Decision rules

- If one asset leads for two consecutive weeks, improve that asset first with another local tool, example, or clearer landing-page copy.
- If no asset receives signal for four weeks, improve distribution metadata and snippets before creating more assets.
- If questions repeatedly ask for paid help, templates, or customization, log it as monetization evidence but do not sell, quote, invoice, or collect payments until no-spend and payout constraints are explicitly resolved.
- If a channel produces moderation, privacy, or identity risk, stop using that channel and keep the project local/static.

## Aggregate snapshot helper after launch

After `APPROVAL-HANDOFF-FIELDS.json` has a concrete approved GitHub Pages `public_base_url` and the static pack is actually public, run this local-only helper to create a weekly aggregate snapshot without analytics or personal-data collection:

```bash
python3 tools/collect_public_signal_snapshot.py
```

The helper writes `post-launch-signal-snapshot.json` with public aggregate counters only: stars, forks, watchers, open issue count, `template-request` issue count, `commercial-fit` issue count, and optional `asset:*` workflow-label totals under `asset_label_counts`. It does **not** persist issue bodies, comments, author names, emails, IPs, cookies, analytics, forms, private inboxes, payment/KYC data, or contact details. If the approval handoff is still in hold state, it writes a blocked snapshot instead of guessing a URL or creating a public workflow.

If an approved reviewer selects an equivalent free static host where GitHub repository counters cannot be derived, use reviewer-supplied aggregate counters only after the approved public URL exists:

```bash
cp manual-aggregate-counters.example.json manual-aggregate-counters.json
# Edit manual-aggregate-counters.json to contain public aggregate integers only.
python3 tools/collect_public_signal_snapshot.py \
  --manual-aggregate manual-aggregate-counters.json
```

The included `manual-aggregate-counters.example.json` is a safe copy/edit fixture for this fallback. The manual JSON may contain only non-negative integer counters under `aggregate_signal` for `stars`, `forks`, `watchers`, `open_issues`, `template_requests`, and `commercial_fit_signals`. This keeps non-GitHub/equivalent-channel validation usable without analytics, referrer logs, issue bodies, usernames, emails, IP addresses, contact details, quote requests, payment data, or lead capture. Manual aggregate mode also stays blocked until `APPROVAL-HANDOFF-FIELDS.json` has an approved public URL, so pre-launch or guessed signal is not recorded.

For offline regression checks only:

```bash
python3 tools/test_collect_public_signal_snapshot.py
```

Use the snapshot only to decide the next revenue-validation action:

- Meaningful early signal: prioritize monetization-path selection and the strongest requested asset before new distribution.
- Some signal: improve the asset/request path that generated it and continue no-spend distribution carefully.
- No/weak signal: improve distribution metadata/snippets before building payment, payout, or sales workflows.

To make that choice machine-readable after each snapshot, run:

```bash
python3 tools/decide_next_revenue_validation_action.py
```

It writes `revenue-validation-decision.json` with a weighted aggregate signal score, automatic `asset:*` label-count handling when available, optional manual asset-score handling, and one recommended next no-spend action. In the current local hold state it recommends unblocking the concrete public URL/account fields first. After launch, it keeps the path money-first: weak/no signal points to distribution metadata, some signal points to conversion/request-path improvement, and meaningful signal points to monetization-learning work before any payment/KYC/quote/invoice workflow.

If the approved public channel exposes only aggregate request/commercial-fit category totals, copy `asset-signal-scores.example.json` to `asset-signal-scores.json`, set each asset to 0..3 from aggregate public-safe category counts only, then run:

```bash
python3 tools/decide_next_revenue_validation_action.py \
  --asset-scores-file asset-signal-scores.json
```

Do not include issue bodies, comments, authors, usernames, emails, IPs, client names, contact details, quotes, invoices, payment data, logs, screenshots, or confidential/security-sensitive details in that file. It is only a compact aggregate scoring hint so meaningful post-launch demand points to the highest-ROI asset or monetization-learning path.

## Manual log template

```text
Week starting: YYYY-MM-DD
Public URL or channel: placeholder until approved
Aggregate snapshot: post-launch-signal-snapshot.json collection_state + stars/forks/watchers/open_issues/template_requests/commercial_fit_signals
MSP monthly report: 0/1/2/3 — notes:
NIS2 checklist: 0/1/2/3 — notes:
M365 executive report: 0/1/2/3 — notes:
Cyber-insurance evidence: 0/1/2/3 — notes:
vCISO QBR: 0/1/2/3 — notes:
Best next autonomous improvement:
Blockers or risk notes:
```
