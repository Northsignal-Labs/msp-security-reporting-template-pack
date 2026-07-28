# M365 Secure Score Executive Report — Example MSP Client

Prepared by Northsignal Labs / independent automation lab
Generated: 2026-07-28 05:45 UTC

> This report is an operational reporting aid. It is not legal advice, does not imply Microsoft affiliation, and does not certify that an environment is secure or compliant.

## Executive summary

- **Client:** Example MSP Client
- **Tenant:** example-client.onmicrosoft.com
- **Reporting period:** July 2026
- **Prepared by:** Northsignal Labs automation prototype
- **Secure Score:** 62% (620 / 1000 points)
- **Previous score:** 55%
- **Overall posture:** Amber
- **Top recommendation:** Prioritise phishing-resistant MFA for administrators and high-risk users before lower-impact hygiene items.

Current posture is **Amber** at **62%**. Score improved by 7.0 percentage points since the previous period.

## Control areas

| Area | Status | Evidence source | Executive note |
| --- | --- | --- | --- |
| Identity and MFA | Red | Entra admin center / Secure Score recommended actions export | Admin MFA is partially complete; privileged accounts should be brought to phishing-resistant MFA first. |
| Email protection | Amber | Microsoft Defender portal policy review | Anti-phishing and safe attachment policies exist but enforcement scope should be confirmed. |
| Device compliance | Amber | Intune compliance dashboard screenshot | Most managed devices report compliance; unmanaged endpoints remain a reporting gap. |
| Audit and logging | Green | Purview audit configuration export | Audit logging is enabled and evidence can be attached to the monthly client pack. |

## Completed improvements this period

| Action completed | Score impact | Risk reduced | Evidence location |
| --- | --- | --- | --- |
| Enabled security defaults for pilot group | +4% | Reduced likelihood of password-only sign-in compromise for pilot users | Evidence pack / July / MFA pilot screenshot |
| Reviewed legacy authentication sign-ins | +3% | Identified legacy protocol usage before full block policy rollout | Evidence pack / July / legacy-auth-export.csv |

## Recommended next actions

| Priority | Action | Expected impact | Owner | Target date | Decision needed |
| --- | --- | --- | --- | --- | --- |
| 1 | Roll out phishing-resistant MFA for all administrator accounts | High risk reduction for tenant takeover scenarios | MSP security lead | 2026-08-15 | Approve administrator rollout window and fallback process |
| 2 | Confirm Defender for Office 365 anti-phishing policy scope | Improves executive confidence in email protection coverage | Messaging administrator | 2026-08-22 | Confirm whether VIP/high-risk users need stricter policy |
| 3 | Document unmanaged endpoint exception list | Makes residual endpoint risk visible for QBR discussion | Client IT owner | 2026-08-31 | Decide whether remaining unmanaged devices should be enrolled or retired |

## Exceptions / accepted risks

| Exception | Reason | Compensating control | Owner | Review date |
| --- | --- | --- | --- | --- |
| One legacy line-of-business app cannot yet use modern authentication | Vendor upgrade is pending | Restricted network location and monitored sign-in alerts | Client application owner | 2026-09-30 |

## Suggested MSP follow-up

1. Confirm whether any Red/Amber items need leadership approval, budget, or change-window planning.
2. Attach screenshots or exported evidence from Microsoft 365 Defender / Entra / admin portals.
3. Re-run this report next month to show trend, decisions, and completed improvements.
