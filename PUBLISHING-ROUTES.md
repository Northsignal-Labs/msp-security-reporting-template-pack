# Zero-cost publishing and distribution route shortlist

Purpose: prepare safe, no-spend options for publishing Northsignal Labs assets without linking the project to any private individual personally. This is a local decision aid only; no accounts were created and no external publishing was performed in this run.

## Scoring

Scale: 1 = weak / risky, 5 = strong / low-friction. Higher total means better autonomous fit under the current guardrails.

| Rank | Route | Cost | Account/privacy risk | Maintenance burden | Discovery potential | Autonomy fit | Total | Notes |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | GitHub repository + GitHub Pages under a non-personal Northsignal Labs org/account | Free tier | 3 | 4 | 3 | 5 | 15 | Best technical fit for static pages and templates. Main blocker: account creation/privacy and avoiding personal identity exposure. No spend if using free Pages. |
| 2 | Cloudflare Pages free tier connected to repository | Free tier | 3 | 4 | 2 | 4 | 13 | Good static hosting, but account setup and provider terms must be accepted. Avoid paid add-ons/domains. |
| 3 | GitLab Pages under a non-personal project identity | Free tier | 3 | 3 | 2 | 4 | 12 | Similar to GitHub Pages; lower expected discovery but workable if GitHub identity is not acceptable. |
| 4 | dev.to / Hashnode technical posts linking to raw templates | Free | 2 | 3 | 4 | 2 | 11 | Distribution can help discovery, but posting/account identity is more public and may require human tone/review. Avoid fake-person founder language. |
| 5 | Reddit/community posting of individual templates | Free | 1 | 2 | 4 | 1 | 8 | Higher moderation/reputation risk. Should require explicit approval before contact/community posting. Use only if genuinely helpful and transparent. |

## Current recommendation

Use a repository-first publishing path only when an approved privacy-safe, non-personal account route exists. The repository should contain only static assets, generated samples, schema, generator code, README, manifest/checklist context, and conservative disclaimers. GitHub Pages is the strongest first option because it supports static HTML, Markdown files, issue-free downloading, and future search indexing without paid spend.

Local preparation has now been split into two release-support files:

- `GITHUB-PAGES-SETUP.md` — privacy-safe repository layout, account/identity requirements, commit-metadata review, and static pre-release steps for a future approved GitHub Pages or equivalent channel.
- `SIGNAL-TRACKING.md` — manual, aggregate-only signal tracking for stars, forks, watchers, open issue counts, template-request label counts, and commercial-fit label counts without analytics scripts or private-data collection.

## Minimum publish checklist

- [ ] Use Northsignal Labs as the outward identity; do not mention any private individual.
- [ ] Run `tools/pre_publication_check.py` against `RELEASE-MANIFEST.json` and manually review any warnings.
- [ ] No paid domains, ads, marketplace boosts, email tools, or analytics subscriptions.
- [ ] Include clear operational-use disclaimers in README and pages.
- [ ] Review `GITHUB-PAGES-SETUP.md` and `SIGNAL-TRACKING.md` before release.
- [ ] Do not add affiliate/referral placeholders, paid offers, payment links, quote/invoice paths, or sponsorship language before separate explicit monetization approval.
- [ ] Publish the five local assets as static files only; no collection of sensitive client data.
- [ ] Do not add analytics, search-console tooling, forms, cookies, private inboxes, lead capture, or tracking parameters during the validation launch.
- [ ] If community distribution is attempted later, be transparent: "small independent automation lab sharing free templates".

## Distribution snippets to prepare later

### Repository description

Free MSP/cybersecurity reporting templates and local automation aids from Northsignal Labs, a small independent automation lab. Static, no-spend, operational-use resources; not legal, insurance, audit, certification, or vendor-affiliated advice.

### Initial release title

Northsignal Labs MSP Security Reporting Template Pack v0.1

### Initial release summary

This first no-spend batch includes five practical MSP/cybersecurity assets: a monthly security report template, NIS2 evidence checklist, M365 Secure Score executive report generator, cyber-insurance evidence checklist, and vCISO QBR agenda. Everything runs locally or as static HTML/Markdown.
