# Request roadmap for first public validation

Status: live public request-roadmap guide on the approved no-spend Northsignal Labs GitHub Pages channel. No public posting, analytics, form, contact capture, payment workflow, quote/invoice path, sales workflow, or spend is created by this file.

## Why this exists

The fastest post-launch revenue-learning path is not more internal asset polish. It is making the next useful request easy to express publicly and safely, then counting only aggregate `template-request` and `commercial-fit` label totals alongside stars, forks, watchers, and open issues.

Use this roadmap on the approved public launch channel to steer visitors toward public-safe requests that reveal which workflow deserves the next no-spend build cycle.

## How to signal interest safely

- Open `.github/ISSUE_TEMPLATE/template-request.yml` for a generic template/generator request when the workflow is unclear.
- Prefer an asset-specific request template when the workflow is known so GitHub can apply the matching `asset:*` label automatically for aggregate workflow scoring: `.github/ISSUE_TEMPLATE/msp-monthly-report-request.yml`, `.github/ISSUE_TEMPLATE/nis2-readiness-request.yml`, `.github/ISSUE_TEMPLATE/m365-secure-score-request.yml`, `.github/ISSUE_TEMPLATE/cyber-insurance-evidence-request.yml`, or `.github/ISSUE_TEMPLATE/vciso-qbr-request.yml`.
- Open `.github/ISSUE_TEMPLATE/commercial-fit-signal.yml` for a non-binding market-signal note about what would make an expanded pack or local workflow bundle worth evaluating later.
- Open `request-signal.html` first if you want a browser-friendly explanation of which request/commercial-fit category to choose and which data must not be shared.
- Do **not** include client names, private security details, credentials, screenshots, logs, personal contact details, contract terms, quote/invoice requests, payment details, regulated information, or confidential information.

## Candidate next requests worth counting

| Candidate request | Best matching current workflow | Why it matters for future revenue validation | Safe signal to count |
|---|---|---|---|
| CSV import examples for monthly MSP reporting | MSP monthly security report | Tests whether operators want lower-friction generator input rather than more static copy | `template-request` with `Local generator or import/export support` |
| One-page executive summary output | MSP monthly security report / M365 Secure Score | Tests whether buyer-facing summary formats are the missing conversion value | `template-request` with `Clearer executive summary or one-page output` |
| Backup/restore evidence checklist | NIS2 / cyber-insurance evidence | Tests an adjacent operational evidence workflow without legal/insurance advice | `template-request` with `Checklist/evidence fields for an adjacent workflow` |
| Vulnerability-management monthly rollup | MSP monthly reporting / vCISO QBR | Tests a common recurring reporting use case that could extend the pack | `template-request` with `New template for the same MSP/security reporting workflow` |
| Repeatable QBR action-register generator | vCISO QBR | Tests whether generator tooling is wanted beyond report writing | `commercial-fit` with `A repeatable local generator bundle` |
| Evidence/QBR/reporting workflow bundle | Cyber-insurance / NIS2 / vCISO | Tests whether users value a packaged workflow, not isolated templates | `commercial-fit` with `Evidence/QBR/reporting workflow packaged together` |

## No-spend decision thresholds

These are first-pass aggregate thresholds only. Asset-specific issue templates should supply `asset:*` label totals automatically after approved GitHub launch, so the decision helper can identify the strongest workflow without reading issue bodies. These thresholds do not authorize payment setup, outreach, quotes, invoices, sales workflows, contact capture, or private data collection.

- **0 high-intent requests after launch:** keep the package stable; improve repository metadata/distribution only if allowed by the first-7-day plan.
- **1–2 template requests in the same workflow:** build the smallest no-spend public template/generator improvement that matches the repeated request type.
- **3+ template requests or any repeated commercial-fit signal in one workflow:** prioritize that workflow for the next public asset cycle and update `tools/decide_next_revenue_validation_action.py` thresholds if needed.
- **Meaningful commercial-fit label count with consistent monetization-trigger selections:** prepare a new blocker recommendation asking the reviewer which separately approved monetization-learning path is acceptable; do not create payment/KYC/quote/invoice/sales infrastructure autonomously.

## Guardrails

- Count aggregate label totals and public repository counters only.
- Do not harvest issue bodies, usernames, emails, IPs, client names, screenshots, logs, vulnerability details, or private/security-sensitive content.
- Treat every commercial-fit issue as non-binding market signal only.
- Keep Northsignal Labs described as a small independent automation lab with no invented founder, customer, testimonial, partnership, certification, revenue, or outcome claims.
