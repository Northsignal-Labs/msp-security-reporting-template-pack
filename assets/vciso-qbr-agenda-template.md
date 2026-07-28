# vCISO QBR Agenda Template for MSPs

Northsignal Labs — free quarterly business review agenda for MSPs that need a repeatable, executive-friendly security review format.

> Important disclaimer: this is an operational meeting and planning template, not legal, compliance, audit, insurance, regulatory, or professional vCISO advice. Adapt it to the client, jurisdiction, contracts, risk appetite, and qualified advisors. Do not represent it as a certification, complete security assessment, or substitute for a formal risk assessment.

## Intended use

Use this template to run a 45–60 minute quarterly security review with an SMB client. The goal is to convert noisy technical data into a clear business conversation: what changed, what risk matters now, what evidence exists, what decisions are needed, and what the next quarter should improve.

## 45–60 minute agenda

| Time | Segment | Purpose | Output |
|---:|---|---|---|
| 0–5 min | Executive context | Confirm business changes, upcoming projects, incidents, insurance/compliance triggers, and decision makers | Updated context notes |
| 5–12 min | Security scorecard | Summarize the 5–8 metrics executives can understand | Red/amber/green scorecard |
| 12–22 min | Top risks and exceptions | Discuss the highest-risk unresolved items, not every ticket | Risk register updates and owners |
| 22–32 min | Control evidence review | Show evidence for MFA, patching, backups, endpoint/email protection, and incident readiness | Evidence gaps and confidence level |
| 32–42 min | Roadmap decisions | Pick the next quarter’s security priorities based on risk, effort, and budget sensitivity | Approved/parked/needs-review decisions |
| 42–52 min | Incident and change lessons | Review incidents, near misses, major changes, and tabletop/postmortem findings | Action items and due dates |
| 52–60 min | Closeout | Confirm owners, dates, client approvals, and next meeting | Final action register |

## Pre-meeting collection checklist

- `[ ]` Last quarter’s action register and completion status
- `[ ]` Current user count, admin count, and major business/system changes
- `[ ]` MFA/conditional access coverage evidence
- `[ ]` Endpoint protection/EDR deployment and alert summary
- `[ ]` Patch/vulnerability exception report
- `[ ]` Backup success/failure and latest restore-test evidence
- `[ ]` Email security and phishing/awareness indicators
- `[ ]` Incident tickets, near misses, postmortems, or tabletop notes
- `[ ]` Open risk exceptions and business-owner approvals
- `[ ]` Upcoming renewals, projects, audits, cyber-insurance requests, or compliance deadlines

## Executive security scorecard

| Area | Current status | Evidence date | Business impact | Next action | Owner |
|---|---|---|---|---|---|
| Identity and MFA | `[green/amber/red]` | `[date]` | `[short impact]` | `[action]` | `[owner]` |
| Endpoint and device security | `[green/amber/red]` | `[date]` | `[short impact]` | `[action]` | `[owner]` |
| Email and phishing resilience | `[green/amber/red]` | `[date]` | `[short impact]` | `[action]` | `[owner]` |
| Backup and recovery readiness | `[green/amber/red]` | `[date]` | `[short impact]` | `[action]` | `[owner]` |
| Patching and vulnerability exposure | `[green/amber/red]` | `[date]` | `[short impact]` | `[action]` | `[owner]` |
| Incident response readiness | `[green/amber/red]` | `[date]` | `[short impact]` | `[action]` | `[owner]` |
| Governance and exceptions | `[green/amber/red]` | `[date]` | `[short impact]` | `[action]` | `[owner]` |

## Risk discussion prompts

Use these prompts to keep the meeting executive-level:

1. What changed in the business since the last review: people, locations, SaaS, vendors, revenue systems, contracts, or regulatory pressure?
2. Which unresolved security item could create the largest business interruption or financial loss?
3. Which exception has been accepted but not formally documented by a business owner?
4. Which control is working well enough to evidence for insurance, audit, or customer due diligence?
5. Which security improvement is low-effort/high-confidence for the next quarter?
6. Which item needs a business decision because the MSP cannot safely decide alone?

## Quarterly action register

| Priority | Action | Risk reduced | Effort | Decision needed | Owner | Due date | Status |
|---:|---|---|---|---|---|---|---|
| 1 | `[e.g. enforce MFA for remaining remote access users]` | `[account takeover]` | `[S/M/L]` | `[approve/park/escalate]` | `[name/team]` | `[date]` | `[open/in progress/done]` |
| 2 | `[action]` | `[risk]` | `[S/M/L]` | `[approve/park/escalate]` | `[name/team]` | `[date]` | `[open/in progress/done]` |
| 3 | `[action]` | `[risk]` | `[S/M/L]` | `[approve/park/escalate]` | `[name/team]` | `[date]` | `[open/in progress/done]` |

## Safe language for client-facing summaries

Use evidence-backed, bounded language:

- Prefer: `MFA coverage improved from [x]% to [y]% for in-scope Microsoft 365 accounts based on export dated [date]. Remaining gaps are [scope].`
- Avoid: `The client is secure` or `MFA is fully solved` unless scope and evidence are complete.
- Prefer: `Backup restore testing evidence exists for [systems] on [date]; the next quarter should validate [remaining systems].`
- Avoid: `Disaster recovery is guaranteed` or `backup risk is eliminated`.
- Prefer: `The MSP recommends business approval for [control] because it reduces [risk] and has [effort/cost/operational impact].`
- Avoid implying that the MSP can make legal, insurance, regulatory, or risk-acceptance decisions on behalf of the client.

## One-page QBR summary

**Client:** `[name]`  
**Quarter:** `[Q#/YYYY]`  
**Prepared by:** `[MSP / IT team]`  
**Meeting date:** `[YYYY-MM-DD]`  
**Attendees/decision makers:** `[names/roles]`

### Executive summary

This quarter’s strongest security evidence is `[area 1]`, `[area 2]`, and `[area 3]`. The most important unresolved risks are `[risk 1]`, `[risk 2]`, and `[risk 3]`. Recommended next-quarter priorities are `[priority 1]`, `[priority 2]`, and `[priority 3]`, subject to business approval, available budget, operational impact, and any required legal/compliance/insurance review.

### Decisions requested

- `[ ]` Approve: `[specific action]`
- `[ ]` Accept/park risk: `[specific exception]` until `[date/review trigger]`
- `[ ]` Escalate: `[topic]` to `[business/legal/insurance/compliance owner]`

## SEO/distribution notes

Candidate page title: `vCISO QBR Agenda Template for MSPs`  
Search intent: MSPs and small IT providers need a repeatable quarterly security review format for client executives.  
Monetization path if approved later: bundled MSP security governance template pack, local QBR report generator, or reporting workflow starter kit only after public aggregate demand signal and separate explicit monetization approval; do not add sponsorship, commission/referral, quote, invoice, payment, or sales paths during validation.
