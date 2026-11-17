---
id: computing-software.cybersecurity-defensive.application-security.developer-security-training
name: developer-security-training
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [developer-security-training, secure-coding-training, appsec-education, security-awareness, role-based-training, nist-ssdf, owasp-samm]
level: practitioner
status: docs-checked
description: "Plan developer security training using NIST SSDF PO.2.2 and OWASP SAMM Education and Guidance: role-based plans, desired outcomes and measuring results."
sources: ["https://owaspsamm.org/model/governance/education-and-guidance/", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Developer security training

Two public frameworks give the structure; anything beyond them is your own design.

## What the frameworks ask for
- **NIST SP 800-218 (SSDF) PO.2.2:** provide role-based training for all personnel with
  responsibilities that contribute to secure development, periodically review personnel
  proficiency and the training, and update it as needed.
- **SSDF implementation examples for PO.2.2:** document the desired training outcomes for
  each role; define the type of training or curriculum needed to reach them; create a
  training plan for each role; acquire or create training, noting that acquired training may
  need customising for the organisation; and measure outcome performance to find where
  training should change.
- **SSDF roles to cover** (PO.2.1 example): cybersecurity staff, security champions,
  project managers and leads, senior management, developers, testers, software assurance
  staff, product owners, and operations and platform engineers.
- **Just-in-time:** an SSDF example suggests development environments with automated
  features that encourage or require secure coding practices with just-in-time training in
  place.
- **OWASP SAMM Education and Guidance (EG):**
  - Stream A, Training and Awareness: maturity 1 gives security awareness training for all
    personnel involved in development; maturity 2 adds technology- and role-specific
    guidance, including the security nuances of each language and platform; maturity 3
    standardises in-house guidance around the organisation's secure development standards.
  - Stream B, Organisation and Culture: maturity 1 identifies a Security Champion in each
    development team; maturity 2 builds a secure software centre of excellence; maturity 3
    builds a secure software community. Maturity 3 objective: in-house training programmes
    facilitated by developers across teams.
  - SAMM notes that training may be instructor-led or computer-based and should grow from
    developers to other roles, ending with role-based training for applicability.

## Practical shape
1. For each role, write the desired outcome, then the curriculum, then the plan (the SSDF
   sequence).
2. Make technology-specific material for the languages and platforms your teams use
   (SAMM maturity 2).
3. Name a security champion per team (SAMM B1).
4. Review proficiency and update content periodically (SSDF PO.2.2).
5. Measure outcomes, not just attendance, and adjust the training.

## Verify
- [ ] Every role involved in the SDLC has a documented outcome and training plan.
- [ ] Each team has a named security champion.
- [ ] Training content has a review date and an owner.
- [ ] Outcome measures exist and feed changes to the training.

## Checked
Method: docs-checked 2026-11-09 against the OWASP SAMM Education and Guidance page (read in full) and NIST SP 800-218 SSDF v1.1 text (PO.2 and the just-in-time example read; converted with pdftotext). Removed as unconfirmed: the claim to group findings by CWE for the top five classes, named labs (Juice Shop, WebGoat, commercial platforms; the Juice Shop page is on an unreadable host), per-role topic lists, recurrence and remediation-time metrics, and the claim that annual video courses change nothing.
