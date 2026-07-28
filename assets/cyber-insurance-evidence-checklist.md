# Cyber Insurance Evidence Checklist for MSPs

Northsignal Labs — free evidence-only checklist for MSPs and small IT teams preparing cyber-insurance renewal, application, or underwriting conversations.

> Important disclaimer: this is an operational evidence organizer, not insurance, legal, brokerage, underwriting, audit, or coverage advice. Requirements vary by insurer, jurisdiction, policy wording, claims history, sector, contracts, and current threat conditions. Do not use this checklist to represent that coverage will be granted, maintained, priced, or paid. Use it to collect evidence and questions for a qualified broker, insurer, counsel, or risk advisor.

## Intended use

Use this checklist before a renewal/application call or client risk review. The goal is to reduce scramble, identify missing evidence, and make it easier to answer common control questions truthfully. Keep the tone factual: **implemented / partially implemented / not implemented / unknown**, with evidence attached.

## 20-minute scoping questions

| Question | Evidence to collect | Owner | Status |
|---|---|---|---|
| Which policy, application, or renewal date is driving the review? | Current policy, renewal notice, broker request, due date | `[name/team]` | `[unknown/in review/confirmed]` |
| Which entities, locations, and systems are in scope? | Entity list, user count, revenue band if already required, asset inventory | `[name/team]` | `[missing/partial/ready]` |
| What security control questions has the insurer or broker already asked? | Application form, supplemental questionnaire, email thread | `[name/team]` | `[missing/partial/ready]` |
| Are any answers uncertain or unsupported by evidence? | Marked-up questionnaire, evidence gap register | `[name/team]` | `[none/some/many]` |
| Who is allowed to make final representations to the insurer? | Internal approval path, broker contact, legal/risk owner | `[name/team]` | `[unknown/in review/confirmed]` |

## Evidence checklist

### 1. Insurance and scope packet

- `[ ]` Current policy/declarations page or renewal request, if available
- `[ ]` Broker/insurer questionnaire and supplemental forms
- `[ ]` In-scope entities, locations, users, and core systems
- `[ ]` Contact list for finance/risk/legal/IT/MSP stakeholders
- `[ ]` Prior claim, incident, or material-change notes if already known and approved for disclosure review

### 2. Identity and access controls

- `[ ]` MFA coverage report for email, VPN/remote access, admin portals, and privileged users
- `[ ]` Privileged account inventory and latest access review
- `[ ]` Joiner/mover/leaver process evidence
- `[ ]` Conditional access or equivalent access policy screenshots/exports
- `[ ]` Break-glass account controls and review date

### 3. Endpoint, email, and monitoring controls

- `[ ]` Endpoint protection/EDR deployment report
- `[ ]` Email security controls summary: filtering, anti-phishing, DMARC/SPF/DKIM where applicable
- `[ ]` Security alert monitoring process and escalation contacts
- `[ ]` Device encryption coverage report where applicable
- `[ ]` Unsupported or unmanaged device exception list

### 4. Backup and recovery evidence

- `[ ]` Backup policy with scope, retention, and responsibility owner
- `[ ]` Latest backup success/failure report
- `[ ]` Latest restore test evidence, date, and result
- `[ ]` RTO/RPO expectations or recovery priority notes
- `[ ]` Backup immutability/offline/separation evidence if present; mark unknown if not verified

### 5. Vulnerability, patching, and configuration

- `[ ]` Patch compliance report for endpoints and servers
- `[ ]` Vulnerability scan, exposure review, or external attack surface notes if available
- `[ ]` Secure configuration baseline for key platforms
- `[ ]` Exception register for delayed patches, legacy systems, or unsupported software
- `[ ]` Remediation owner and target date for high-risk items

### 6. Incident response and reporting readiness

- `[ ]` Incident response plan or playbook
- `[ ]` Severity levels and internal escalation path
- `[ ]` External contacts: broker, insurer claim notice route, counsel, forensics/MSP escalation
- `[ ]` Evidence preservation/log retention notes
- `[ ]` Recent tabletop, postmortem, or lessons-learned evidence if available

### 7. Security awareness and governance

- `[ ]` Security awareness/phishing training evidence
- `[ ]` Management review cadence for cyber risk
- `[ ]` Security policy or acceptable-use policy evidence
- `[ ]` Vendor/supplier risk process for critical SaaS/providers
- `[ ]` Approval process for final questionnaire responses

## Evidence gap register

| Control/question | Current answer | Evidence status | Risk of overstatement | Owner | Next action | Due date |
|---|---|---|---|---|---|---|
| `[e.g. MFA for all remote access]` | `[yes/partial/no/unknown]` | `[attached/missing/needs validation]` | `[low/medium/high]` | `[name/team]` | `[specific next step]` | `[date]` |

## Safe response wording helper

Use conservative wording when evidence is incomplete:

- Prefer: `MFA is enforced for Microsoft 365 users and administrators according to the attached Conditional Access export dated [date]. VPN and third-party SaaS coverage still need validation.`
- Avoid: `MFA is enabled everywhere` unless that has been verified for every in-scope system.
- Prefer: `A restore test was completed for [system] on [date]; broader recovery testing is planned.`
- Avoid: `Backups are fully tested` without scope and date.

## Executive summary template

**Client/entity:** `[name]`  
**Review trigger:** `[renewal/application/client review]`  
**Review date:** `[YYYY-MM-DD]`  
**Prepared by:** `[MSP / IT team]`  
**Scope:** `[systems/entities reviewed]`

Evidence is strongest for `[area 1]`, `[area 2]`, and `[area 3]`. The highest-priority evidence gaps before final insurance representations are `[gap 1]`, `[gap 2]`, and `[gap 3]`. Final answers, coverage implications, and disclosures should be reviewed by the authorized business owner and qualified insurance/legal advisors.

## SEO/distribution notes

Candidate page title: `Cyber Insurance Evidence Checklist for MSPs`  
Search intent: MSPs and SMB IT teams need a practical evidence packet before cyber-insurance applications and renewals.  
Monetization path if approved later: bundled insurance-renewal evidence pack, local questionnaire evidence tracker, or evidence workflow starter kit only after public aggregate demand signal and separate explicit monetization approval; do not add broker/referral, quote, invoice, payment, or sales paths during validation.
