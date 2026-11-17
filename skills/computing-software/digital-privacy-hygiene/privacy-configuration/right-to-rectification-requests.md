---
id: computing-software.digital-privacy-hygiene.privacy-configuration.right-to-rectification-requests
name: right-to-rectification-requests
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, right-to-rectification, gdpr, right-to-correct, data-subject-rights]
level: practitioner
status: docs-checked
description: "Get inaccurate personal data corrected under GDPR Article 16, with evidence, the Article 12 deadlines, restriction while disputed, and escalation."
sources:
  - "https://gdpr-info.eu/art-16-gdpr/"
  - "https://gdpr-info.eu/art-12-gdpr/"
  - "https://gdpr-info.eu/art-18-gdpr/"
  - "https://gdpr-info.eu/art-19-gdpr/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Correction requests

**Goal:** wrong data (address, date of birth, account history, a profile on a broker site) is fixed, not just
ignored.

## Rights
- **GDPR Article 16**: rectification of inaccurate personal data "without undue delay", and completion of incomplete
  data, including by means of a supplementary statement, taking the purposes of processing into account.
- **Article 18**: while you contest accuracy, you can obtain restriction of processing for a period enabling the
  controller to verify it. Restricted data may, apart from storage, be processed only with your consent, for legal
  claims, for protecting another person's rights or for important public interest.
- Credit reports and other regimes (for example California) have their own dispute processes; this skill covers the
  GDPR text only.

## How
1. Try self-service account settings first.
2. Otherwise write to the privacy contact:
   > Under Article 16 GDPR, please correct the following inaccurate personal data: [field] currently shows [X]; the
   > correct value is [Y]. Evidence attached. Please confirm the correction and inform any recipients you have
   > disclosed it to (Article 19).
3. Attach minimal evidence (a redacted bill for an address).

## Deadlines
Article 12(3): information on action taken without undue delay and within one month of receipt, extendable by two
further months where necessary given complexity and number of requests; the controller must tell you of an
extension, with reasons, within the first month. Requests are free of charge unless manifestly unfounded or
excessive, and the controller may ask for extra information if it has reasonable doubts about your identity
(Article 12(5)-(6)). Article 19: the controller must tell each recipient it disclosed the data to about the
rectification unless impossible or disproportionate effort, and must tell you who they are if you ask.

## If refused
Article 12(4): the controller must tell you, without delay and within one month, the reasons for not acting and
that you can lodge a complaint with a supervisory authority and seek a judicial remedy. Ask for a supplementary
statement to be added (Article 16), then escalate to the regulator.

## Gotchas
- Correcting data at a data broker can make the profile more accurate and valuable; deletion or opt-out may be what
  you actually want (a practical caution, not from the cited pages).

## Checked
Checked 2026-11-08 against the full text of gdpr-info.eu Articles 12, 16, 18 and 19. The ICO and CPPA pages returned
only stubs and were dropped from sources. Removed the CPRA right, the 45-day CCPA deadline, the credit-reporting
statutes and the claim that opinions may be annotated, none of which those articles state.
Method: documentation only; no commands were run.
