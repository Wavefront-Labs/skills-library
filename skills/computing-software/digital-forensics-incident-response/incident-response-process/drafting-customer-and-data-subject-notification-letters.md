---
id: computing-software.digital-forensics-incident-response.incident-response-process.drafting-customer-and-data-subject-notification-letters
name: drafting-customer-and-data-subject-notification-letters
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [customer-notification, breach-notification, data-subject-notification, gdpr-article-34, incident-communications, dfir]
level: practitioner
status: docs-checked
description: "Draft data-subject breach notification letters: GDPR Art. 34 content and exemptions, the California notice trigger and AG sample rule, plus fact-control steps for the responder."
sources: ["https://gdpr-info.eu/art-34-gdpr/", "https://gdpr-info.eu/art-33-gdpr/", "https://oag.ca.gov/privacy/databreach/reporting"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Drafting customer and data-subject notification letters

The responder's job is to give Legal accurate facts and to stop the letter over- or under-stating
them. Counsel owns the final text and the decision to send.

## What the sources require
**GDPR Article 34** (communication to the data subject):
- Applies when the breach is **likely to result in a high risk** to individuals' rights and
  freedoms; communicate **without undue delay**.
- The communication must describe the nature of the breach **in clear and plain language** and
  contain at least the information in Article 33(3) points (b), (c) and (d): the contact point
  (data protection officer or other), the likely consequences, and the measures taken or proposed
  including mitigation.
- It is **not required** if: (a) appropriate technical and organisational protection was applied
  to the affected data, such as encryption making it unintelligible to unauthorised persons;
  (b) subsequent measures mean the high risk is no longer likely to materialise; or (c) it would
  involve disproportionate effort, in which case a public communication or similar equally
  effective measure must be used instead.
- The supervisory authority can require communication, or decide an exemption applies.
- Notice to the supervisory authority is separate (Article 33: within 72 hours where feasible).

**California** (Attorney General page): a business must notify any California resident whose
unencrypted personal information was acquired, or reasonably believed to have been acquired, by
an unauthorised person (Civil Code 1798.82(a)). If a single breach requires notice to more than
500 California residents, submit one sample copy of the notification, excluding personally
identifiable information, electronically to the Attorney General (1798.82(f)).
The page does not give required headings or font sizes; check the statute text with counsel.

## What the forensic team supplies
| Section | Facts |
|---|---|
| What happened | Window of unauthorised access (first to last confirmed), date discovered, type |
| Information involved | Exact data elements per recipient group |
| What we are doing | Containment done, law enforcement notified (if allowed), monitoring offered |
| What you can do | Steps tailored to the data lost (password reset, credit freeze, phishing warning) |

## Procedure
1. Build the affected-person list from evidence (exfiltration listing mapped to records), with a
   column per data element; generate letters per data-element combination, not one for all.
2. Write in plain language; avoid boilerplate such as "sophisticated attack" unless supported.
3. Fact-check every sentence against the investigation timeline; keep unconfirmed items out.
4. Coordinate regulator filings (supervisory authority notice, state AG sample) so the letter
   matches what regulators received.
5. Prepare a call-centre FAQ from the same facts and a returned-mail process.

## Gotchas
- "No evidence of misuse" is misleading when logs were missing for the window; say what was and
  was not examined.
- Do not put indicators or technical detail that helps a copycat in a customer letter.
- Consider translations and accessible formats for the recipient population.

## Verify
Each claim in the letter traces to a timeline entry or evidence item, and the recipient list
reconciles to the exfiltrated record count.

## Checked
Checked 2026-11-08 against GDPR Articles 33 and 34 (gdpr-info.eu) and the California Attorney
General breach reporting page. The EDPB guidelines page only links a PDF and was not readable as
text. Removed: California section headings and 10-point font rule, the 8th-grade reading level,
and the claim that one structure satisfies most regimes.
Method: docs-only read of cited pages, 2026-11-08
