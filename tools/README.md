# Local report generators

Northsignal Labs local generators convert JSON inputs into Markdown and optional HTML reports. They use only Python standard library modules: no network, no paid APIs, no accounts, and no client data leaves the machine.

## Inputs and outputs

### M365 Secure Score executive report

- Input sample: `../samples/m365-secure-score-report.sample.json`
- JSON schema/reference: `../schemas/m365-secure-score-report.schema.json`
- Generator: `m365_secure_score_report_generator.py`
- Sample Markdown output: `../generated/m365-secure-score-report.sample.md`
- Sample HTML output: `../generated/m365-secure-score-report.sample.html`

### MSP monthly security report

- Input sample: `../samples/msp-monthly-security-report.sample.json`
- JSON schema/reference: `../schemas/msp-monthly-security-report.schema.json`
- Generator: `msp_monthly_security_report_generator.py`
- Sample Markdown output: `../generated/msp-monthly-security-report.sample.md`
- Sample HTML output: `../generated/msp-monthly-security-report.sample.html`

### NIS2 readiness evidence summary

- Input sample: `../samples/nis2-readiness-summary.sample.json`
- JSON schema/reference: `../schemas/nis2-readiness-summary.schema.json`
- Generator: `nis2_readiness_summary_generator.py`
- Sample Markdown output: `../generated/nis2-readiness-summary.sample.md`
- Sample HTML output: `../generated/nis2-readiness-summary.sample.html`

### Cyber-insurance evidence gap register

- Input sample: `../samples/cyber-insurance-gap-register.sample.json`
- JSON schema/reference: `../schemas/cyber-insurance-gap-register.schema.json`
- Generator: `cyber_insurance_gap_register_generator.py`
- Sample Markdown output: `../generated/cyber-insurance-gap-register.sample.md`
- Sample HTML output: `../generated/cyber-insurance-gap-register.sample.html`

### vCISO QBR summary

- Input sample: `../samples/vciso-qbr-summary.sample.json`
- JSON schema/reference: `../schemas/vciso-qbr-summary.schema.json`
- Generator: `vciso_qbr_summary_generator.py`
- Sample Markdown output: `../generated/vciso-qbr-summary.sample.md`
- Sample HTML output: `../generated/vciso-qbr-summary.sample.html`

## Run locally

From `autonomous-lab/`:

To regenerate every sample Markdown/HTML output in one local proof run:

```bash
python3 tools/run_all_sample_generators.py
```

Expected result:

```text
Northsignal Labs all-sample generator runner
workflows: 5
state: regenerated
errors: 0
```

Use `python3 tools/run_all_sample_generators.py --check-only` to verify all generator/sample/output paths without rewriting sample outputs. The runner is filesystem-only and does not use a network, publish, create accounts, add analytics/forms/contact capture, create payment/KYC/quote/invoice workflows, or spend money.

Single-generator examples:

```bash
python3 tools/m365_secure_score_report_generator.py \
  samples/m365-secure-score-report.sample.json \
  --markdown-out generated/m365-secure-score-report.sample.md \
  --html-out generated/m365-secure-score-report.sample.html
```

Expected result:

```text
wrote generated/m365-secure-score-report.sample.md
wrote generated/m365-secure-score-report.sample.html
```

Cyber-insurance gap register example:

```bash
python3 tools/cyber_insurance_gap_register_generator.py \
  samples/cyber-insurance-gap-register.sample.json \
  --markdown-out generated/cyber-insurance-gap-register.sample.md \
  --html-out generated/cyber-insurance-gap-register.sample.html
```

Expected result:

```text
wrote generated/cyber-insurance-gap-register.sample.md
wrote generated/cyber-insurance-gap-register.sample.html
```

MSP monthly security report example:

```bash
python3 tools/msp_monthly_security_report_generator.py \
  samples/msp-monthly-security-report.sample.json \
  --markdown-out generated/msp-monthly-security-report.sample.md \
  --html-out generated/msp-monthly-security-report.sample.html
```

Expected result:

```text
wrote generated/msp-monthly-security-report.sample.md
wrote generated/msp-monthly-security-report.sample.html
```

NIS2 readiness evidence summary example:

```bash
python3 tools/nis2_readiness_summary_generator.py \
  samples/nis2-readiness-summary.sample.json \
  --markdown-out generated/nis2-readiness-summary.sample.md \
  --html-out generated/nis2-readiness-summary.sample.html
```

Expected result:

```text
wrote generated/nis2-readiness-summary.sample.md
wrote generated/nis2-readiness-summary.sample.html
```

vCISO QBR summary example:

```bash
python3 tools/vciso_qbr_summary_generator.py \
  samples/vciso-qbr-summary.sample.json \
  --markdown-out generated/vciso-qbr-summary.sample.md \
  --html-out generated/vciso-qbr-summary.sample.html
```

Expected result:

```text
wrote generated/vciso-qbr-summary.sample.md
wrote generated/vciso-qbr-summary.sample.html
```

## Pre-publication check

Before any approved static release, run the local checker from `autonomous-lab/`:

```bash
python3 tools/pre_publication_check.py
```

The checker reads `RELEASE-MANIFEST.json`, confirms required files exist, checks local relative links, blocks configured analytics/tracker patterns, and fails if a private project shorthand appears in release files. It is filesystem-only: no network access, no publishing, no accounts, no spend, and no data upload.

## Approval handoff validation

Before any approved sitemap/robots URL cutover, validate the machine-readable approval fields from `autonomous-lab/`:

```bash
python3 tools/validate_approval_handoff.py
```

Expected result while no channel/URL has been approved:

```text
Northsignal Labs approval handoff validation
approved_for_cutover: False
errors: 0
warnings: 0
cutover_state: hold_public_release
```

The validator reads `APPROVAL-HANDOFF-FIELDS.json`, keeps the current package in a safe hold state while approval fields are blank, and requires a completed HTTPS public URL plus no-spend, no-financial-workflow, no-data-collection, and claims/identity confirmations before any future cutover. It is filesystem-only and does not publish, upload, create accounts, contact services, spend money, replace hosts, enable analytics, or create payment workflows.

### Apply reviewer-supplied public channel fields

After the reviewer supplies a completed JSON object from `PUBLIC-CHANNEL-FIELDS-TEMPLATE.json`, dry-run the copy into `APPROVAL-HANDOFF-FIELDS.json`:

```bash
python3 tools/apply_public_channel_fields.py --source completed-public-channel-fields.json
```

Only if the dry-run is clean and the fields were explicitly supplied/approved, apply the local handoff update:

```bash
python3 tools/apply_public_channel_fields.py --source completed-public-channel-fields.json --apply
python3 tools/validate_approval_handoff.py
```

The helper refuses template placeholders, non-HTTPS URLs, missing no-spend/no-financial/no-data/claims confirmations, and unsafe metadata wording. It updates only `APPROVAL-HANDOFF-FIELDS.json`; it does not infer a URL, replace sitemap/robots hosts, publish, upload, authenticate, create accounts, contact services, collect data, add analytics/forms, create payment/KYC/quote/invoice workflows, or spend money.

Fixture test:

```bash
python3 tools/test_apply_public_channel_fields.py
```

Expected result:

```text
PASS: template/hold-state source blocks
PASS: approved dry-run does not modify target
PASS: approved apply updates and validates ready
PASS: placeholder or unsafe URL fails closed
public channel fields apply fixture tests: all passed
```

### Validator-gated public URL cutover helper

After `tools/validate_approval_handoff.py` reports `cutover_state: ready_for_reviewer_cutover`, dry-run the local public URL reference replacement:

```bash
python3 tools/perform_public_url_cutover.py
```

Then, only after confirming the approved public base URL, apply the local replacement:

```bash
python3 tools/perform_public_url_cutover.py --apply
```

The helper replaces only `https://northsignal-labs.local/` in `sitemap.xml`, `robots.txt`, and generator JSON Schema `$id` references, writes `PUBLIC-URL-CUTOVER-LOG.json` after an applied cutover, and keeps the release local-only. It does not publish, upload, create accounts, contact services, spend money, add analytics, collect data, or create payment/KYC/quote/invoice workflows.

### Approved launch preflight orchestrator

After reviewer-supplied public channel fields are applied and `tools/validate_approval_handoff.py` reaches `ready_for_reviewer_cutover`, run a dry-run-only local precheck:

```bash
python3 tools/run_approved_launch_preflight.py --precheck-only
```

Only after the reviewer confirms the approved HTTPS URL/account fields, run the full local preflight:

```bash
python3 tools/run_approved_launch_preflight.py --apply-cutover
```

The orchestrator validates approval fields, dry-runs the public URL reference cutover, applies it only when `--apply-cutover` is passed, reruns label/workflow/telemetry/regression gates, prepares `public-repo-export/`, packages the verified ZIP, validates packet/bundle/dashboard honesty, and writes `APPROVED-LAUNCH-PREFLIGHT.json`. It does not infer a URL, create accounts, authenticate, upload, publish, post publicly, contact anyone, collect analytics/forms/contact data, create payment/KYC/quote/invoice/sales workflows, or spend money; upload remains reviewer-controlled.

Fixture test:

```bash
python3 tools/test_perform_public_url_cutover.py
```

Expected result:

```text
PASS: hold-state approval fields block cutover
PASS: approved dry run validates without modifying files
PASS: approved apply replaces public URL placeholders
PASS: approved placeholder public URL fails closed
public URL cutover fixture tests: all passed
```

### Approval handoff fixture tests

To prove the approval validator fails closed on incomplete/unsafe future cutover records and still accepts the current local hold state, run:

```bash
python3 tools/test_approval_handoff_validator.py
```

Expected result:

```text
PASS: blank hold-state fixture stays blocked without errors
PASS: approved fixture with missing confirmations fails closed
PASS: approved fixture with placeholder URL host fails closed
PASS: complete approved HTTPS fixture reaches ready state before host replacement
approval handoff validator fixture tests: all passed
```

The test helper builds disposable local fixtures in a temporary directory and copies the validator there. It does not modify the live `APPROVAL-HANDOFF-FIELDS.json`, `sitemap.xml`, or `robots.txt`, and it does not publish, upload, create accounts, contact services, spend money, replace hosts, enable analytics, or create payment workflows.

## GitHub signal label validation

Before an approved GitHub-channel launch, confirm the public-safe issue-template labels used for aggregate demand measurement are declared:

```bash
python3 tools/validate_github_signal_labels.py
```

Expected result:

```text
Northsignal Labs GitHub signal label validation
declared labels: 8
issue-template labels: 3
required signal labels: 3
required asset signal labels: 5
errors: 0
warnings: 0
```

The checker is filesystem-only. It reads `.github/labels.yml` and `.github/ISSUE_TEMPLATE/*.yml` so a future approved GitHub release does not lose `template-request`, `commercial-fit`, or aggregate `asset:*` workflow signal because labels were missing. It does not call GitHub, create labels, publish, upload, authenticate, collect data, create accounts, start payment/KYC workflows, or spend money.

After a concrete approved non-personal GitHub repository exists, use `../GITHUB-LABEL-SETUP.md` as the reviewer-side handoff for creating or verifying the exact labels in the approved repository. That handoff is not upload authorization and should not be used to infer a repository, create an account, authenticate as a personal identity, collect data, start analytics, add payment/KYC/quote/invoice workflows, or spend money.

## GitHub Pages workflow validation

For a future approved GitHub Pages channel, validate that the static deployment workflow remains a no-spend Pages-only handoff:

```bash
python3 tools/validate_github_pages_workflow.py
```

Expected local hold output:

```text
Northsignal Labs GitHub Pages workflow validation
workflow: .github/workflows/static-pages.yml
allowed actions checked: 4
errors: 0
warnings: 0
```

The checker is filesystem-only. It verifies `.github/workflows/static-pages.yml` uses only the approved GitHub Pages actions, has explicit read/Pages/OIDC permissions, keeps the artifact path at the static repository root, and avoids secrets, paid-hosting adapters, analytics, payment or purchase-flow references, and contact-capture references. It does not call GitHub, authenticate, enable Actions, create a repository, upload, publish, collect data, start payment/KYC/quote/invoice workflows, or spend money.

## Public launch approval packet sync validation

Before asking a reviewer to approve the concrete public URL/account fields from the one-screen packet, confirm the packet still reflects the latest locally verified ZIP:

```bash
python3 tools/validate_public_launch_packet_sync.py
```

Expected local output after `tools/package_go_live_zip.py` and packet resync:

```text
Northsignal Labs public launch packet sync validation
package file count: 75
zip verified: True
errors: 0
warnings: 0
```

The validator reads only `GO-LIVE-PACKAGE.json` and `PUBLIC-LAUNCH-APPROVAL-PACKET.md`. It blocks stale approval handoffs when the packet file count, byte size, or SHA-256 no longer matches the current verified ZIP, and it does not publish, upload, create accounts, contact services, collect data, add analytics, create payment/KYC/quote/invoice workflows, or spend money.

## HTML conversion route validation

Before an approved static upload, verify that every public HTML entry and asset page still routes visitors toward proof-of-value and countable request/commercial-fit signal:

```bash
python3 tools/validate_html_conversion_routes.py
```

Expected result:

```text
Northsignal Labs HTML conversion route validation
html pages checked: 9
required route links checked: 57
errors: 0
warnings: 0
```

The checker is filesystem-only. It verifies that index, download, sample-output, request-signal, and all five asset landing pages link to the start/download guide, generated sample previews, request-signal guide, and structured template-request/commercial-fit workflows where applicable. It does not publish, upload, add analytics/forms/contact capture, collect issue bodies or user data, create payment/KYC/quote/invoice workflows, or spend money.

## Public release bundle completeness validation

Before a final approved upload review, confirm the manifest-approved bundle still contains the files needed to move from launch to measurable demand signal:

```bash
python3 tools/validate_public_release_bundle.py
```

Expected local output after a clean bundle review:

```text
Northsignal Labs public release bundle validation
errors: 0
warnings: 0
```

The validator checks that visitor entry points, `DOWNLOAD.md`, `LICENSE`, `.nojekyll`, `CHECKSUMS.txt`, repository metadata, structured GitHub request/commercial-fit hooks, label setup, GitHub Pages handoff, aggregate-only signal tools, post-upload live URL smoke testing, public-safe contribution/security boundaries, and URL-cutover tools remain manifest-approved, and that internal approval packets, generated ZIP/status/telemetry/signal files are not accidentally included in the public manifest. It is filesystem-only and does not publish, upload, authenticate, create accounts, contact services, collect data, add analytics, create payment/KYC/quote/invoice workflows, or spend money.

## Live public URL smoke test after approved upload

After a reviewer-controlled upload to the concrete approved HTTPS `public_base_url`, check that the live static pack is reachable before collecting aggregate demand signal:

```bash
python3 tools/smoke_test_public_url.py
```

Expected result while approval fields are still missing:

```text
Northsignal Labs live public URL smoke test
state: blocked_until_approved_public_base_url
requests checked: 0
errors: 0
warnings: 1
```

Once `APPROVAL-HANDOFF-FIELDS.json` is approved and the reviewer-controlled upload is live, the helper fetches an expanded allowlist of approved public HTTPS paths covering the repository entry files, browser start guide, AI/search summary, checksum sheet, sample gallery, request roadmap, all five landing pages, the three generated HTML samples, robots/sitemap, GitHub labels, and the template-request/commercial-fit issue templates. It checks for HTTP 200, non-empty bodies, no `northsignal-labs.local` leakage, no forms, no analytics scripts, and no payment/contact-capture risk tokens, then writes `public-url-smoke-test.json` for local review. It does not authenticate, upload, create accounts, post publicly, collect issue bodies/authors/contact details/referrers/IPs, add analytics, create payment/KYC/quote/invoice/sales workflows, or spend money.

## Public file checksum generation

Before the final staging/package gates for an approved upload review, regenerate the manifest-approved public file checksum sheet:

```bash
python3 tools/write_release_checksums.py
```

Expected clean output:

```text
Northsignal Labs release checksum writer
errors: 0
```

The writer hashes every manifest-approved public file except `CHECKSUMS.txt` itself and writes SHA-256 plus byte counts into `CHECKSUMS.txt`. This gives a future reviewer a quick integrity check for the ZIP or repo-root upload tree before public validation starts. It is filesystem-only and does not publish, upload, authenticate, create accounts, contact services, collect data, add analytics, create payment/KYC/quote/invoice workflows, or spend money.

## Post-launch aggregate signal snapshot

After a concrete approved public URL exists and the static pack is actually public, collect aggregate-only validation signal before choosing the next revenue action:

```bash
python3 tools/collect_public_signal_snapshot.py
python3 tools/decide_next_revenue_validation_action.py
```

For an approved non-GitHub/equivalent free static host where GitHub counters cannot be derived, copy the included example and edit only public aggregate integer counters:

```bash
cp manual-aggregate-counters.example.json manual-aggregate-counters.json
python3 tools/collect_public_signal_snapshot.py --manual-aggregate manual-aggregate-counters.json
python3 tools/decide_next_revenue_validation_action.py
```

`manual-aggregate-counters.example.json` is intentionally limited to `stars`, `forks`, `watchers`, `open_issues`, `template_requests`, and `commercial_fit_signals`. Do not add usernames, issue bodies, comments, emails, IPs, referrers, analytics exports, contact details, client names, quotes, invoices, payment data, or confidential information. Manual aggregate mode remains blocked until `APPROVAL-HANDOFF-FIELDS.json` has a completed approved public URL, and the decision helper remains no-spend/no-payment/no-KYC.

## Local release staging

After the checker passes, stage only manifest-approved files into a local `dist/` folder for review:

```bash
python3 tools/stage_release.py
```

Expected result after a clean current staging run:

```text
Northsignal Labs release staging
manifest-approved files copied: 75
forbidden staged files: 0
```

The staging helper copies files listed in `RELEASE-MANIFEST.json`, writes `dist/STAGED-RELEASE-MANIFEST.json` with byte counts and SHA-256 hashes, and blocks internal/cache files such as `status.json`, `__pycache__/`, and `*.pyc`. It is local-only: no upload, no account creation, no public posting, no paid service, no payment, no affiliate workflow, and no analytics.

## Staged release review

After staging, compare the source manifest, staged manifest, and actual `dist/` files:

```bash
python3 tools/review_staged_release.py
```

Expected result after a clean staging run:

```text
Northsignal Labs staged release review
errors: 0
warnings: 0
```

The review helper catches missing required files, unexpected staged files, stale hashes/byte counts, forbidden cache/internal files, and source/staged version mismatches. It is also filesystem-only and does not publish, upload, create accounts, contact services, spend money, enable analytics, or create any payment or commission-link workflow.

## Release-readiness telemetry

For Activity Dashboard status and future cron comparisons, run the local telemetry helper from `autonomous-lab/`:

```bash
python3 tools/write_release_readiness_telemetry.py
```

Expected result after a clean local release review:

```text
wrote release-readiness-telemetry.json
overall_pass: True
```

The helper runs the approval validator, GitHub signal-label validation, GitHub Pages workflow validation, checksum generation, pre-publication check, staging, static HTTP smoke test, and staged-release review, then writes compact machine-readable results to `release-readiness-telemetry.json`. The telemetry file is internal status data for local dashboards, not a public release requirement. For a concrete approved launch, `tools/run_approved_launch_preflight.py` wraps this telemetry helper with cutover, export, ZIP, packet-sync, bundle, and dashboard-honesty gates. Both helpers are filesystem-only and do not publish, upload, create accounts, contact services, spend money, enable analytics, or create any payment or commission-link workflow.

## Post-launch aggregate signal snapshot

After a concrete approved GitHub Pages URL exists in `APPROVAL-HANDOFF-FIELDS.json` and the static pack is actually public, collect aggregate public counters only:

```bash
python3 tools/collect_public_signal_snapshot.py
```

Expected result while public URL fields are still missing:

```text
wrote post-launch-signal-snapshot.json
collection_state: blocked_until_approved_github_pages_public_base_url
aggregate_signal: {'stars': 0, 'forks': 0, 'watchers': 0, 'open_issues': 0, 'template_requests': 0, 'commercial_fit_signals': 0}
```

The snapshot helper reads only GitHub's public aggregate repository counters and label-level counts for `template-request` and `commercial-fit` issues when an approved GitHub Pages URL can be derived, or writes a blocked snapshot while approval is incomplete. If an equivalent approved free static host is used instead of GitHub Pages, a reviewer can provide aggregate-only counters after launch:

```bash
python3 tools/collect_public_signal_snapshot.py --manual-aggregate manual-aggregate-counters.json
```

Manual aggregate mode accepts only non-negative integer counters for `stars`, `forks`, `watchers`, `open_issues`, `template_requests`, and `commercial_fit_signals`; it stays blocked until `APPROVAL-HANDOFF-FIELDS.json` contains an approved public URL. The helper does not persist issue bodies, comments, author names, emails, IPs, analytics IDs, cookies, contact details, private inboxes, payment/KYC data, or lead-capture data; it does not authenticate, publish, post, create accounts, spend money, or start sales workflows.

## Next revenue-validation decision

After writing `post-launch-signal-snapshot.json`, convert the aggregate signal into the next no-spend action:

```bash
python3 tools/decide_next_revenue_validation_action.py
# Optional after approved launch if aggregate asset-category scores are available:
python3 tools/decide_next_revenue_validation_action.py \
  --asset-scores-file asset-signal-scores.json
```

Expected result while public URL fields are still missing:

```text
wrote revenue-validation-decision.json
decision_state: blocked_until_public_url
weighted_signal_score: 0
```

The decision helper is local-only and reads aggregate counters plus either automatic aggregate `asset:*` label totals from `post-launch-signal-snapshot.json` or optional manual 0..3 asset scores from `--asset-scores-json` / `--asset-scores-file` using the copy/edit fixture `asset-signal-scores.example.json`. It prevents drift into low-ROI polish by choosing one of four paths: unblock public URL fields, improve distribution metadata for weak/no signal, improve the conversion/request path for some signal, or prioritize monetization-learning around the strongest requested asset for meaningful signal. It does not contact services, authenticate, publish, post, create accounts, collect personal or client data, spend money, or start payment/KYC/quote/invoice workflows. Asset-score files must contain aggregate category scores only; do not include issue bodies, comments, authors, usernames, emails, IPs, client names, contact details, quotes, invoices, payment data, logs, screenshots, or confidential/security-sensitive information.

## Safe-use framing

The outputs are operational reporting aids. They do not imply Microsoft affiliation, certify an environment, provide insurance/legal/brokerage/underwriting/compliance advice, or replace review by a qualified operator and authorized business owner. Avoid entering secrets, tokens, passwords, private keys, or sensitive customer data in sample JSON.
