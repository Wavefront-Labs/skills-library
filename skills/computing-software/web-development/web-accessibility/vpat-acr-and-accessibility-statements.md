---
id: computing-software.web-development.web-accessibility.vpat-acr-and-accessibility-statements
name: vpat-acr-and-accessibility-statements
category: computing-software
field: web-development
product: web-accessibility
tags: [accessibility-testing, vpat, accessibility-statement, acr, section-508, en-301-549]
level: practitioner
status: docs-checked
description: "Producing a VPAT/ACR and a public accessibility statement: choosing the edition, honest conformance levels, remarks, and 508, EN 301 549 and EAA context."
sources:
  - https://www.itic.org/policy/accessibility/vpat
  - https://www.w3.org/WAI/planning/statements/
  - https://www.section508.gov/sell/acr/
  - https://ec.europa.eu/social/main.jsp?catId=1202
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPAT / ACR and accessibility statements

## 1. VPAT vs ACR
The **VPAT** (Voluntary Product Accessibility Template, by ITI) is the blank template; a completed one is an **ACR** (Accessibility Conformance Report). Buyers (US federal under Section 508, universities, enterprises, EU public sector) ask for it during procurement.

## 2. Pick the edition (VPAT 2.5+)
- **508**: US federal (Revised 508 = WCAG 2.0 AA plus hardware/software/docs chapters).
- **EU**: EN 301 549 (WCAG 2.1 AA for web + more) for EU procurement and the European Accessibility Act.
- **WCAG**: WCAG 2.x only.
- **INT**: all of the above in one document - most common for SaaS.
Recent editions include WCAG 2.2 criteria.

## 3. Fill it honestly
Conformance terms per criterion: **Supports**, **Partially Supports**, **Does Not Support**, **Not Applicable**. Remarks must explain what doesn't work and where ("Partially Supports: data tables in Reports lack header associations; fix planned Q1"). Base it on a real audit (WCAG-EM style) dated and with product version; list evaluation methods (tools, AT used).
Overclaiming "Supports" everywhere is common, easy for buyers' auditors to disprove, and a legal liability in disputes.

## 4. Accessibility statement (public)
Required for EU public sector bodies (Web Accessibility Directive) and expected under the EAA for covered services. Contents (W3C generator):
- Commitment and standard targeted (WCAG 2.2 AA).
- Conformance status (fully/partially/non-conformant).
- Known limitations and alternatives, with dates for fixes.
- Contact method for feedback/alternative formats and expected response time; enforcement procedure (EU).
- Date of last review and method (self-assessment or third-party).
Link it from the footer of every page.

## 5. Maintain
Update ACRs per major release; keep a changelog; the statement must reflect reality, not aspiration.

## Verify
A buyer's auditor spot-checking three "Supports" criteria finds them true; statement includes working contact details and a review date within the last year.

## Checked

2026-10-28. Confirmed in the ITI VPAT page: VPAT is a template and the completed document is an ACR, no certification or submission process, editions 508 (WCAG 2.0), EU (EN 301 549, WCAG 2.1), WCAG and INT, four conformance levels; and in the W3C accessibility statements page: statements, EU Web Accessibility Directive, contents. Removed: the Not Evaluated term, the EAA date and the annual update cadence.

Method: documentation only; no commands were run.
