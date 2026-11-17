---
id: computing-software.digital-privacy-hygiene.password-hygiene.triaging-a-breach-notification-letter
name: triaging-a-breach-notification-letter
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, breach-notification-triage, data-breach, breach-response, credit-monitoring, ssn-exposure, health-data-breach, phishing-follow-up]
level: practitioner
status: draft
description: "Read a data breach notice, work out which data types leaked, and take the matching actions (password, freeze, card replacement, phishing watch) without overreacting or ignoring it."
sources:
  - "https://www.identitytheft.gov/databreach"
  - "https://consumer.ftc.gov/articles/what-do-if-you-were-affected-data-breach"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Triaging a breach notification

**Goal:** most people get several breach letters a year. Map the leaked data types to
specific actions.

## First: is the letter real?
Breach notices are themselves used for phishing. Don't click links or call numbers in
the email; find the company's breach page via its main website or search news, and enrol
in any offered monitoring through that page.

## Action by data type
| Leaked | Do |
|---|---|
| Email + password (even hashed) | Change that password; change anywhere it was reused; enable MFA |
| Email only | Expect targeted phishing referencing the company; consider alias |
| Phone number | Expect smishing; carrier port-out PIN |
| Payment card number | Ask issuer for a new card; watch statements |
| Bank account + routing | Alert bank; watch for ACH debits |
| SSN / national ID + DOB | **Credit freeze** at all bureaus; IRS IP PIN; consider fraud alert |
| Driver's licence / passport number | Report to issuer per their guidance; monitor |
| Health/insurance data | Review explanation-of-benefits statements for services you didn't receive |
| Security question answers | Change those answers (random) everywhere |
| Physical address, DOB | Expect pretexting; verbal passwords on accounts |

## Free monitoring offers
Accept if from the company (often 1-2 years of credit monitoring); a freeze is stronger
than monitoring, so do both.

## Record keeping
Keep the letter (date, breach ID) in a folder; useful for disputes and class settlements.

## Verify
- [ ] Each leaked data type has its action completed.
- [ ] Company's breach page found independently, not via the email link.
