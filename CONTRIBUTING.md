# Contributing to the Northsignal Labs MSP Security Reporting Template Pack

Status: future public-safe contribution guide; local-only until an approved no-spend, non-personal public channel exists.

Northsignal Labs welcomes practical, generic feedback on MSP/security reporting templates and local generators after the pack is published through an approved channel. The goal is to turn public interest into useful demand-validation signal without collecting sensitive data, exposing private identities, or creating a sales/payment workflow.

## What to contribute

Good public-safe contributions include:

- Requests for a missing MSP/security reporting template or generator.
- Generic wording improvements that make an existing template clearer.
- Synthetic sample-data improvements that do not identify a real organization or person.
- Local-only generator bug reports using toy/sample JSON, not real tenant/client data.
- Suggestions for which asset should be expanded next: monthly report, NIS2 evidence checklist, M365 Secure Score executive report, cyber-insurance evidence/gap register, or vCISO QBR agenda.

## What not to share

Do **not** include any of the following in issues, pull requests, examples, screenshots, or copied text:

- Client, employer, tenant, user, supplier, insurer, broker, auditor, or partner names.
- Private security details, vulnerabilities, incident timelines, control gaps, logs, screenshots, credentials, tokens, tenant IDs, device names, IP addresses, email addresses, or domains.
- Contract terms, pricing, budgets, invoices, purchase requests, tax/KYC details, bank/payment information, or regulated information.
- Personal contact details, private social/profile links, personal account metadata, or confidential information.
- Claims that the templates provide legal, insurance, brokerage, compliance, audit, certification, Microsoft-affiliated, professional-services, or complete-security assurance.

If a useful example would normally require sensitive details, replace it with generic placeholder text or synthetic sample values before posting.

## Best issue type

After an approved GitHub-channel launch:

- Use `.github/ISSUE_TEMPLATE/template-request.yml` for public-safe requests about a missing or improved template/generator.
- Use `.github/ISSUE_TEMPLATE/commercial-fit-signal.yml` only for non-binding market signal about what might justify future monetization work. It is not a quote request, purchase, invoice, sales conversation, or payment workflow.
- Blank issues are intentionally disabled in `.github/ISSUE_TEMPLATE/config.yml` so feedback stays structured and less likely to collect sensitive data.

## Pull-request expectations

Pull requests should be small, static, and local-first:

1. Keep all links relative unless a public URL has already been approved and cut over through `APPROVAL-HANDOFF-FIELDS.json` and `PUBLIC-URL-CUTOVER-CHECKLIST.md`.
2. Do not add analytics, scripts, cookies, forms, email collection, private inbox workflows, payment links, partner-credit links, purchase flows, or paid dependencies.
3. Do not add personal identity details, fake founder/customer/testimonial/certification/revenue claims, or professional-service claims.
4. Keep examples synthetic and mark them as examples.
5. Preserve the MIT `LICENSE` and operational-use notices.
6. Run the local checks before release review:

```bash
python3 tools/validate_approval_handoff.py
python3 tools/pre_publication_check.py
python3 tools/stage_release.py
python3 tools/review_staged_release.py
```

## Revenue-validation reason for this guide

Structured contribution rules make the first public release safer and easier to evaluate: public feedback can become measurable template-request, generator-request, fork, and commercial-fit signal without creating sensitive-data handling, private outreach, payment/KYC, or reputation risk.
