# Cyber Insurance Evidence Gap Register — Example MSP Client

Northsignal Labs — local, evidence-only automation output.

> Important: this is an operational evidence organizer, not insurance, legal, brokerage, underwriting, audit, or coverage advice. Final representations should be reviewed by the authorized business owner and qualified advisors.

## Summary

- Entity/client: Example MSP Client
- Review trigger: Cyber-insurance renewal evidence review
- Scope: Microsoft 365, endpoints, backups, remote access, and incident response evidence
- Prepared by: Northsignal Labs local generator sample
- Generated date: 2026-07-28
- Gap count by overstatement risk: high=1, medium=2, low=1

## Gap register

| Control/question | Current answer | Evidence status | Risk of overstatement | Owner | Next action | Due date |
|---|---|---|---|---|---|---|
| MFA for remote access: Is MFA enforced for all remote access and privileged accounts? | yes | needs validation | high | MSP security lead | Ask MSP security lead to attach dated evidence before representing this control as implemented. | 2026-08-05 |
| Endpoint protection coverage: Are endpoints protected by monitored EDR/AV? | partial | partial | medium | Endpoint admin | Ask Endpoint admin to document covered systems, exceptions, and remediation plan. | 2026-08-07 |
| Restore testing: Has a recent restore test been completed and documented? | unknown | missing | medium | Backup owner | Ask Backup owner to validate the answer and mark unsupported claims as unknown until confirmed. | 2026-08-09 |
| Incident response contacts: Are incident escalation and claim notice contacts documented? | yes | attached | low | Operations manager | Keep evidence with the renewal/application packet and confirm it remains current. | 2026-08-01 |

## Conservative wording prompts

- Do not answer `yes` unless the scope and dated evidence support the statement.
- Use `partial` or `unknown` where coverage is not verified across all in-scope systems.
- Keep exceptions, compensating controls, and final approval owner visible before responses are submitted.
