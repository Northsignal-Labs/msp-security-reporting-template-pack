# GitHub signal-label setup handoff

Updated: 2026-07-28T02:18:00Z
Status: local-only; use only after a concrete no-spend non-personal GitHub repository/channel is approved.

## Purpose

The future GitHub issue templates use labels to turn public feedback into aggregate demand signal:

- `template-request` counts requests for another template or generator.
- `commercial-fit` counts non-binding monetization-learning signal.
- `demand-signal` marks public-safe feedback that can be counted only in aggregate.
- `asset:*` labels let a reviewer tag public-safe issues by workflow so the next no-spend revenue-validation decision can identify the strongest asset category without reading issue bodies, authors, comments, emails, IPs, or private text.

If those labels are absent in the approved repository, GitHub may not apply the template labels consistently, and `tools/collect_public_signal_snapshot.py` can undercount the strongest post-launch revenue-validation signals. The optional asset-category labels also let `tools/decide_next_revenue_validation_action.py` prioritize the workflow with the strongest aggregate demand signal automatically. This handoff keeps the label setup explicit without calling GitHub, creating accounts, uploading files, collecting issue bodies, starting payments, or spending money.

## Guardrails

Do not use this file to infer a repository, create an account, upload the package, contact communities, start analytics, collect contact details, add payment/KYC/quote/invoice workflows, or spend money. It is only a post-approval repository-setup checklist for the reviewer-controlled GitHub channel named in `APPROVAL-HANDOFF-FIELDS.json`.

Before applying labels, confirm all of the following:

1. A concrete approved no-spend GitHub repository/channel exists under the Northsignal Labs identity.
2. The approved repository metadata does not expose any private individual, personal account, private email, or unsupported founder/customer/certification/revenue claim.
3. `APPROVAL-HANDOFF-FIELDS.json` is complete enough for reviewer-controlled GitHub setup, even if sitemap/robots cutover has not yet been applied.
4. `.github/labels.yml`, `.github/ISSUE_TEMPLATE/template-request.yml`, and `.github/ISSUE_TEMPLATE/commercial-fit-signal.yml` are included in the staged public package.
5. Blank issues remain disabled by `.github/ISSUE_TEMPLATE/config.yml`.

## Label records to create or verify

Create or verify exactly these public-safe labels in the approved repository:

| Label | Color | Description |
|---|---|---|
| `template-request` | `0E8A16` | Aggregate demand signal for a requested template or generator; no client/private data. |
| `commercial-fit` | `5319E7` | Non-binding market signal for future monetization learning; not a sale or quote. |
| `demand-signal` | `1D76DB` | Public-safe issue-template feedback that can be counted in aggregate only. |
| `asset:msp-monthly-report` | `BFDADC` | Aggregate asset-category signal for MSP monthly reporting; count label totals only. |
| `asset:nis2-readiness` | `C5DEF5` | Aggregate asset-category signal for NIS2/evidence readiness; count label totals only. |
| `asset:m365-secure-score` | `D4C5F9` | Aggregate asset-category signal for M365 Secure Score reporting; count label totals only. |
| `asset:cyber-insurance-evidence` | `F9D0C4` | Aggregate asset-category signal for cyber-insurance evidence workflows; count label totals only. |
| `asset:vciso-qbr` | `FEF2C0` | Aggregate asset-category signal for vCISO/QBR workflows; count label totals only. |

## Optional reviewer-side GitHub CLI commands

Only run these after the approved GitHub repository exists and the reviewer is authenticated to the approved non-personal account/org. Replace `OWNER/REPO` with the approved repository target; do not use a personal account/repository unless explicitly approved.

```bash
gh label create template-request \
  --repo OWNER/REPO \
  --color 0E8A16 \
  --description "Aggregate demand signal for a requested template or generator; no client/private data."

gh label create commercial-fit \
  --repo OWNER/REPO \
  --color 5319E7 \
  --description "Non-binding market signal for future monetization learning; not a sale or quote."

gh label create demand-signal \
  --repo OWNER/REPO \
  --color 1D76DB \
  --description "Public-safe issue-template feedback that can be counted in aggregate only."

gh label create asset:msp-monthly-report --repo OWNER/REPO --color BFDADC \
  --description "Aggregate asset-category signal for MSP monthly reporting; count label totals only."
gh label create asset:nis2-readiness --repo OWNER/REPO --color C5DEF5 \
  --description "Aggregate asset-category signal for NIS2/evidence readiness; count label totals only."
gh label create asset:m365-secure-score --repo OWNER/REPO --color D4C5F9 \
  --description "Aggregate asset-category signal for M365 Secure Score reporting; count label totals only."
gh label create asset:cyber-insurance-evidence --repo OWNER/REPO --color F9D0C4 \
  --description "Aggregate asset-category signal for cyber-insurance evidence workflows; count label totals only."
gh label create asset:vciso-qbr --repo OWNER/REPO --color FEF2C0 \
  --description "Aggregate asset-category signal for vCISO/QBR workflows; count label totals only."
```

If a label already exists, update it manually in the GitHub UI or with reviewer-controlled commands so the name stays identical. The aggregate snapshot helper depends on exact label names, not colors.

## Local preflight commands

Run from `autonomous-lab/` before upload and again after any label/template file change:

```bash
python3 tools/validate_github_signal_labels.py
python3 tools/collect_public_signal_snapshot.py
python3 tools/decide_next_revenue_validation_action.py
```

Expected local hold-state result before a public URL is supplied:

```text
Northsignal Labs GitHub signal label validation
errors: 0
warnings: 0

collection_state=blocked_until_approved_github_pages_public_base_url
decision_state=blocked_until_public_url
```

After approved launch, count only aggregate public counters and label totals: stars, forks, watchers, open issues, `template-request` issues, `commercial-fit` issues, and the five `asset:*` workflow-label totals. Do not collect issue bodies, authors, comments, emails, IPs, screenshots, logs, client names, credentials, contact details, contract terms, or confidential/security-sensitive information.
