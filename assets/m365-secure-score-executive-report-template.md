# M365 Secure Score Executive Report Template

Northsignal Labs — free operational template for MSPs and small IT teams.

> Use disclaimer: this is an operational reporting template, not legal, audit, insurance, Microsoft licensing, or compliance advice. Microsoft Secure Score is one signal, not a complete security measurement. Validate all findings in the tenant before sending externally.

## Intended use

Use this template to translate Microsoft Secure Score and related Microsoft 365/Entra signals into a short executive-facing client report. The goal is to show trend, risk themes, evidence, and recommended next actions without drowning the client in portal details.

## 10-minute evidence collection

Collect the following from the tenant before completing the report:

- `[ ]` Current Microsoft Secure Score percentage and points achieved/available
- `[ ]` Previous-period score, if available
- `[ ]` Top improvement actions from Secure Score
- `[ ]` MFA/conditional-access coverage evidence
- `[ ]` Privileged role/admin account review
- `[ ]` Legacy authentication or risky sign-in evidence
- `[ ]` Device compliance/management snapshot, if Intune is used
- `[ ]` Email protection baseline signals, if available
- `[ ]` Exceptions accepted by client or MSP

## Copy/paste executive report

### 1. Executive summary

**Client:** `[client name]`  
**Tenant:** `[tenant name / tenant id optional]`  
**Reporting period:** `[YYYY-MM-DD to YYYY-MM-DD]`  
**Prepared by:** `[MSP / IT team]`  
**Current Secure Score:** `[score_percent]%` (`[points_achieved]` / `[points_available]` points)  
**Trend:** `[up / flat / down]` compared with `[previous_score_percent]%` last period  
**Overall posture:** `[Green / Amber / Red]`

Microsoft Secure Score improved/declined/remained stable during this period. The most important action for leadership is: `[single decision or action needed]`.

### 2. Score trend

| Metric | Current | Previous | Change | Notes |
|---|---:|---:|---:|---|
| Secure Score percentage | `[%]` | `[%]` | `[+/- points]` | `[summary]` |
| Points achieved | `[#]` | `[#]` | `[+/-]` | `[summary]` |
| Improvement actions completed | `[#]` | `[#]` | `[+/-]` | `[summary]` |
| High-impact actions remaining | `[#]` | `[#]` | `[+/-]` | `[summary]` |

### 3. Control-area summary

| Area | Status | Evidence source | Executive note |
|---|---|---|---|
| Identity and MFA | `[Green/Amber/Red]` | `[Secure Score / Entra]` | `[e.g. MFA gap remains for 3 users]` |
| Admin and privileged access | `[Green/Amber/Red]` | `[Entra roles / PIM]` | `[e.g. stale admin account removed]` |
| Device management | `[Green/Amber/Red]` | `[Intune / Defender]` | `[e.g. unmanaged endpoints still exist]` |
| Email and collaboration protection | `[Green/Amber/Red]` | `[Defender / Exchange]` | `[e.g. anti-phishing policy reviewed]` |
| Data protection | `[Green/Amber/Red]` | `[Purview / M365]` | `[e.g. sensitivity labels not deployed]` |
| Monitoring and response | `[Green/Amber/Red]` | `[Defender / alerts]` | `[e.g. alert triage ownership confirmed]` |

### 4. Completed improvements this period

| Action completed | Score impact | Risk reduced | Evidence link/location |
|---|---:|---|---|
| `[e.g. disabled legacy authentication]` | `[+points]` | `[account compromise risk]` | `[ticket/screenshot/export]` |
| `[action]` | `[+points]` | `[risk]` | `[evidence]` |

### 5. Recommended next actions

Prioritize no more than five actions. Tie each recommendation to a business risk or operational decision.

| Priority | Recommended action | Expected impact | Owner | Target date | Decision needed |
|---:|---|---|---|---|---|
| 1 | `[action]` | `[score/risk impact]` | `[name/team]` | `[date]` | `[yes/no/which option]` |
| 2 | `[action]` | `[score/risk impact]` | `[name/team]` | `[date]` | `[yes/no/which option]` |
| 3 | `[action]` | `[score/risk impact]` | `[name/team]` | `[date]` | `[yes/no/which option]` |

### 6. Exceptions and accepted risks

| Exception | Reason | Compensating control | Owner | Review date |
|---|---|---|---|---|
| `[e.g. break-glass account excluded from MFA]` | `[reason]` | `[monitoring/restriction]` | `[owner]` | `[date]` |

### 7. Evidence checklist

- `[ ]` Secure Score screenshot/export for current period
- `[ ]` Previous score or monthly comparison
- `[ ]` List of completed improvement actions
- `[ ]` List of remaining high-impact actions
- `[ ]` MFA/conditional-access policy evidence
- `[ ]` Privileged role review evidence
- `[ ]` Device compliance or endpoint-management evidence
- `[ ]` Client-approved exception/risk notes

## Structured input schema

A local generator can use the companion JSON schema at `../schemas/m365-secure-score-report.schema.json` to produce this report from a validated JSON file.

Minimal example:

```json
{
  "client_name": "Example Ltd",
  "tenant_name": "example.onmicrosoft.com",
  "reporting_period": "2026-07",
  "prepared_by": "MSP / IT team",
  "secure_score_percent": 57,
  "previous_score_percent": 52,
  "points_achieved": 342,
  "points_available": 600,
  "overall_posture": "Amber",
  "top_recommendation": "Enable phishing-resistant MFA for privileged roles.",
  "control_areas": [
    {"area": "Identity and MFA", "status": "Amber", "evidence_source": "Microsoft Secure Score / Entra", "executive_note": "MFA coverage improved but two exceptions remain."}
  ],
  "recommended_actions": [
    {"priority": 1, "action": "Require phishing-resistant MFA for admins", "expected_impact": "Reduces account takeover risk", "owner": "IT", "target_date": "2026-08-15", "decision_needed": "Approve rollout window"}
  ]
}
```

## SEO/distribution notes

Candidate page title: `M365 Secure Score Executive Report Template`  
Search intent: MSPs and IT teams need a client-safe way to explain Secure Score trend and next actions.  
Monetization path if approved later: downloadable template pack, local report generator bundle, or reporting starter kit only after public aggregate demand signal and separate explicit monetization approval; do not add affiliate/referral, quote, invoice, payment, or sales paths during validation.
