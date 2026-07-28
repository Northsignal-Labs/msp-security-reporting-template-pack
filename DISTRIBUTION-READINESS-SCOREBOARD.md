# Northsignal Labs distribution-readiness scoreboard

Updated: 2026-07-25T10:32:48Z
Status: local-only distribution review aid; not published; no account, contact, spend, upload, payment workflow, tracking script, or external posting added.

## Purpose

This scoreboard compares free distribution candidates against the go/no-go criteria in `RELEASE-DECISION-NOTE.md` and the approval fields in `APPROVAL-HANDOFF.md`. It is intentionally local and conservative: it does not approve a channel, create an account, publish files, collect leads, or start monetization.

## Scoring method

Each route is scored from 0-2 on the criteria below. A route is **eligible for reviewer consideration** only when every hard gate is marked `yes` and total score is at least 12/14.

| Criterion | Score meaning |
|---|---|
| No-spend fit | 0 = paid/unclear, 1 = free tier with caveats, 2 = free static route possible without spend |
| Northsignal identity fit | 0 = requires personal identity, 1 = metadata risk needs review, 2 = non-personal lab identity can be used honestly |
| Static-file fit | 0 = cannot host static bundle, 1 = partial/manual conversion, 2 = can host the staged static pack |
| Public URL clarity | 0 = no stable URL, 1 = generated URL after setup, 2 = predictable URL once approved |
| Privacy/metadata risk | 0 = likely exposes private details, 1 = manageable only with careful setup, 2 = low if configured correctly |
| Signal value | 0 = no practical traffic/signal path, 1 = weak passive discovery, 2 = useful passive discovery or community search |
| Automation/review friction | 0 = high manual workflow, 1 = moderate setup/review, 2 = simple copy/upload after gate checks |

## Candidate channel scores

| Rank | Candidate route | Hard gates clear? | Score | Reviewer recommendation | Main reason / caveat |
|---:|---|---|---:|---|---|
| 1 | GitHub Pages under an approved non-personal Northsignal Labs org/account | partial | 12/14 | Best first reviewer candidate | Strong static-file and discoverability fit, but account/org ownership, public commit metadata, and generated URL require explicit approval before use. |
| 2 | GitLab Pages under an approved non-personal Northsignal Labs namespace | partial | 11/14 | Backup static host candidate | Similar no-spend static path; still needs namespace/account metadata review and slightly higher setup friction. |
| 3 | Cloudflare Pages free tier under an approved non-personal account, using platform subdomain only | partial | 10/14 | Possible later candidate | Can host static files without a paid domain, but account setup and provider metadata need approval; avoid paid add-ons and custom domains. |
| 4 | Itch.io free project page for downloadable template pack | partial | 8/14 | Distribution-only backup | Useful for downloadable assets, but less natural for SEO/static pages and may imply marketplace/payment settings that must remain disabled. |
| 5 | Reddit/Hacker News/community posting | no | 5/14 | Do not use autonomously | Contact/posting and reputation risk; requires explicit human approval and careful non-promotional framing. |
| 6 | Paid-download marketplace listing | no | 3/14 | Blocked for now | Marketplace/payout/KYC/payment expectations conflict with the no-spend/no-financial-risk autonomous mandate. |

## Hard-gate checklist before any route can move from local review to public action

- `release_gate_alignment.state` is `aligned` after the final file change.
- `release_readiness.telemetry_regression_alert.state` is `clean` after the final telemetry run.
- `robots.txt`, `sitemap.xml`, and generator JSON Schema `$id` values still use `northsignal-labs.local` until a public URL is explicitly approved; after approval, all three target types must use the same approved HTTPS public base URL.
- The route can publish as Northsignal Labs without exposing a private individual, a private personal account, private contact details, or an invented human founder.
- The route requires no paid domain, hosting, ads, subscription, marketplace fee, payout setup, tax/KYC setup, tracking script, contact form, or active monetization link.
- The staged `dist/` package contains only `RELEASE-MANIFEST.json` approved files and no internal telemetry/cache files.
- `APPROVAL-HANDOFF.md` and `APPROVAL-HANDOFF-FIELDS.json` have all required reviewer-supplied details completed before any URL cutover, `tools/validate_approval_handoff.py` reports 0 errors, and `PUBLIC-URL-CUTOVER-CHECKLIST.md` is used for the final local sitemap/robots host switch after, and only after, the channel and public URL are approved.

## Current conclusion

The strongest no-spend route remains **GitHub Pages with an approved non-personal Northsignal Labs org/account**, but it is not autonomously actionable yet. The local package should stay in **hold public release** state until a reviewer approves the channel/account metadata, public URL, required `APPROVAL-HANDOFF.md` fields, and the machine-readable `APPROVAL-HANDOFF-FIELDS.json` preflight. After approval, `tools/validate_approval_handoff.py` should pass first and `PUBLIC-URL-CUTOVER-CHECKLIST.md` should be used for the local placeholder-host switch and final gate reruns. This scoreboard advances revenue readiness by making the distribution decision explicit without spending money, contacting anyone, creating accounts, or publishing externally.
