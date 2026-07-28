# MSP Monthly Security Report Template

Northsignal Labs — free operational template for MSPs and small IT teams.

> Positioning note: this is a practical reporting skeleton. It is not legal, insurance, audit, or compliance advice. Replace examples with verified customer-specific evidence before using externally.

## Intended use

Use this once per month to turn noisy security tooling into a short executive-facing report. The value proposition is speed: one repeatable report that an MSP can complete from Microsoft 365, endpoint protection, backup, ticketing, and firewall/VPN evidence.

## Copy/paste report structure

### 1. Executive summary

**Client:** `[client name]`  
**Reporting period:** `[YYYY-MM-DD to YYYY-MM-DD]`  
**Prepared by:** `[MSP / IT team]`  
**Overall security posture:** `[Green / Amber / Red]`

During this period, we reviewed identity, device, endpoint, backup, email, and network security signals. The highest-priority item is: `[single most important action]`.

| Area | Status | Notes |
|---|---|---|
| Identity and MFA | `[Green/Amber/Red]` | `[e.g. 97% MFA coverage; 2 break-glass exceptions]` |
| Endpoint protection | `[Green/Amber/Red]` | `[e.g. all active devices protected; 1 stale device]` |
| Patch/update hygiene | `[Green/Amber/Red]` | `[e.g. 8 devices pending critical updates]` |
| Backups | `[Green/Amber/Red]` | `[e.g. last successful restore test: date]` |
| Email/security awareness | `[Green/Amber/Red]` | `[e.g. phishing simulation planned / blocked threats]` |
| Network/VPN/firewall | `[Green/Amber/Red]` | `[e.g. old VPN users removed]` |

### 2. Key changes this month

- `[Change 1 — e.g. enabled MFA for 14 users]`
- `[Change 2 — e.g. removed 6 inactive accounts]`
- `[Change 3 — e.g. completed backup restore test]`

### 3. Metrics snapshot

| Metric | Current | Target | Trend | Source |
|---|---:|---:|---|---|
| MFA coverage | `[%]` | `100%` | `[up/down/flat]` | Microsoft Entra / M365 |
| Admin accounts reviewed | `[#]` | `100% monthly` | `[up/down/flat]` | Entra / AD |
| Devices missing EDR | `[#]` | `0` | `[up/down/flat]` | EDR console |
| Critical patches overdue >14 days | `[#]` | `0` | `[up/down/flat]` | RMM / Intune |
| Backup jobs successful | `[%]` | `>=98%` | `[up/down/flat]` | Backup platform |
| Restore tests completed | `[#]` | `>=1 quarterly` | `[up/down/flat]` | Backup evidence |
| High-risk sign-ins | `[#]` | `0 unresolved` | `[up/down/flat]` | Entra ID Protection |
| Phishing/malware blocked | `[#]` | `informational` | `[up/down/flat]` | Email security |

### 4. Incidents and notable alerts

| Date | Alert/incident | Severity | Action taken | Current status |
|---|---|---|---|---|
| `[date]` | `[summary]` | `[Low/Med/High]` | `[containment/remediation]` | `[closed/open]` |

If there were no material incidents, state: `No material security incidents were confirmed during this reporting period. Routine alerts were reviewed and closed according to standard process.`

### 5. Risk register update

| Risk | Business impact | Likelihood | Owner | Due date | Status |
|---|---|---|---|---|---|
| `[e.g. shared admin account remains active]` | `[impact]` | `[L/M/H]` | `[name/team]` | `[date]` | `[open/in progress/closed]` |

### 6. Evidence checklist

Attach or link evidence where possible:

- `[ ]` MFA coverage export or screenshot
- `[ ]` List of privileged users reviewed
- `[ ]` Endpoint/EDR device coverage export
- `[ ]` Patch compliance report
- `[ ]` Backup success report
- `[ ]` Latest restore-test evidence
- `[ ]` High-risk sign-in review
- `[ ]` Firewall/VPN user review
- `[ ]` Security awareness/phishing evidence, if applicable

### 7. Recommended next actions

Prioritize no more than five actions.

| Priority | Action | Reason | Owner | Due date |
|---:|---|---|---|---|
| 1 | `[action]` | `[risk reduced]` | `[owner]` | `[date]` |
| 2 | `[action]` | `[risk reduced]` | `[owner]` | `[date]` |
| 3 | `[action]` | `[risk reduced]` | `[owner]` | `[date]` |

### 8. Client decision log

| Decision needed | Options | Recommendation | Decision/date |
|---|---|---|---|
| `[e.g. require phishing-resistant MFA for admins]` | `[option A/B]` | `[recommendation]` | `[pending/date]` |

## Lightweight automation idea for later

A future Northsignal Labs tool can generate this report from a YAML/JSON input file and output Markdown/HTML/PDF. No paid dependency is needed for a local prototype.

Example input fields:

```yaml
client: Example Ltd
period: 2026-07
posture: Amber
mfa_coverage_percent: 97
critical_patches_overdue: 8
backup_success_percent: 99
restore_test_date: 2026-07-10
top_recommendation: Remove stale admin accounts and close MFA exceptions.
```

## SEO/distribution notes

Candidate page title: `Free MSP Monthly Security Report Template`  
Search intent: MSPs need a client-ready monthly reporting skeleton.  
Monetization path if approved later: downloadable template pack, expanded local generator bundle, reporting starter kit, or no-spend pilot recommendation only after public aggregate demand signal and separate explicit monetization approval.
