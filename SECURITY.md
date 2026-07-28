# Security and sensitive-data handling

Status: public-safe guidance for a future approved static release; no private inbox, contact form, account workflow, bounty, paid support, or data-collection process is created by this file.

## Scope

This repository contains static templates, sample data, schemas, and local Python generators for MSP/client-facing reporting workflows. It is not a managed service, monitoring product, legal/compliance/audit service, insurance/brokerage service, Microsoft-affiliated product, or incident-response channel.

## Do not share sensitive information

Do not open issues, pull requests, discussions, comments, or examples that contain:

- client/customer names, tenant names, domains, IP addresses, hostnames, usernames, email addresses, phone numbers, or personal contact details;
- credentials, secrets, tokens, keys, cookies, session data, private URLs, logs, screenshots, packet captures, configuration exports, or vulnerability details from a real environment;
- regulated, confidential, contractual, claim, underwriting, legal, compliance, audit, or incident-response information;
- quote requests, invoices, purchase requests, payment details, payout/tax/KYC details, referral arrangements, or sales commitments.

Use generic placeholders only, such as `Example Client`, `tenant.example`, `192.0.2.10`, `example-control-id`, or synthetic sample values.

## Public feedback path after launch

If the package is later published through an approved non-personal GitHub channel, use only the structured issue templates for public-safe feedback:

- `.github/ISSUE_TEMPLATE/template-request.yml` for template or generator requests.
- `.github/ISSUE_TEMPLATE/commercial-fit-signal.yml` for non-binding commercial-fit signal.

Blank issues are intentionally disabled through `.github/ISSUE_TEMPLATE/config.yml` to reduce accidental sensitive-data intake.

## Vulnerability reports

This project does not currently operate a private vulnerability disclosure inbox or bounty program. Do not submit real vulnerability details, exploit steps, customer evidence, credentials, or private environment data through public GitHub issues or pull requests.

For non-sensitive defects in the static templates or local example generators, describe the issue with synthetic data only and remove all private context before posting.

## Maintainer handling rule

Any accidental sensitive data should be treated as out of scope for public validation: remove it from the public release surface where platform tooling permits, do not copy it into telemetry or examples, and do not use it as sales, marketing, customer, testimonial, or commercial-fit evidence.
