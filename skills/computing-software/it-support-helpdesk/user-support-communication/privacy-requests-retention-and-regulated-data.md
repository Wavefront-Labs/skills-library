---
id: computing-software.it-support-helpdesk.user-support-communication.privacy-requests-retention-and-regulated-data
name: privacy-requests-retention-and-regulated-data
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, data-subject-request, ticket-data-retention, regulated-data-handling, data-breach-reporting, gdpr, hipaa, pci-dss]
level: practitioner
status: draft
description: "Handle privacy work that lands on the desk: data subject requests, ticket data retention, PCI and HIPAA data in tickets, and reporting suspected data breaches on time."
sources:
  - "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-of-access/"
  - "https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html"
  - "https://www.pcisecuritystandards.org/document_library/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# privacy-requests-retention-and-regulated-data

## Data subject requests (GDPR/UK GDPR and similar)
- Recognise them: any request from a person to access, correct, delete or port their
  personal data, in any wording, to any channel ("send me everything you hold about me").
- Don't action it yourself; log and route to the privacy/DPO team the same day. The
  legal clock (one month under GDPR, extendable) starts on receipt by the organisation,
  including the service desk.
- Help the privacy team find data: ticket history for that user, mailbox and file
  searches (eDiscovery by authorised staff), logs.
- Verify identity before releasing anything.

## Ticket data retention
- Tickets contain personal data; keep them only as long as the retention schedule
  allows (commonly 2-7 years depending on purpose, sector and legal need).
- Configure archiving/deletion rules in the ITSM tool (archive rules, data retention
  policies); attachments often hold the most sensitive data (screenshots, HR documents).
- Legal holds override deletion for specific records.

## Regulated data in support
| Data | Rule of thumb |
|---|---|
| Payment card numbers (PCI DSS) | Never store full PAN or CVV in tickets, chats or recordings; redact, delete attachments; pause call recording when card details are spoken |
| Health information (HIPAA in the US) | Minimum necessary; don't paste PHI into tickets; access logged; BAAs with vendors (including remote support tools) |
| Special category data (GDPR) | Health, biometrics, etc. restricted; tickets about HR/medical issues in restricted queues |
- Remote sessions on screens showing regulated data: ask the user to close records first.
- Don't move regulated data to personal devices or unapproved AI tools.

## Reporting a data breach
- A breach includes misdirected email with personal data, lost unencrypted device,
  unauthorised access, ransomware with exfiltration.
- Report internally to security/privacy immediately with facts: what data, how many
  people, when discovered, containment so far. Don't investigate deeply or notify
  affected people yourself.
- Regulatory deadlines are short: GDPR requires notifying the supervisory authority
  within 72 hours of becoming aware (where required); HIPAA breach notification within
  60 days to individuals; PCI incidents to the acquirer per contract. The clock starts
  when the organisation knows, so desk delays count.

## Verify
DSARs are logged and routed same day, retention rules run in the ITSM tool, ticket audits
find no card numbers or PHI, and breach reports reach privacy within an hour of discovery.
