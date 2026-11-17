---
id: computing-software.web-development.web-accessibility.accessibility-legal-requirements
name: accessibility-legal-requirements
category: computing-software
field: web-development
product: web-accessibility
tags: [european-accessibility-act, ada-title-iii, section-508, en-301-549, accessibility-law]
level: practitioner
status: docs-checked
description: "Accessibility law for websites: ADA Title II and III, Section 508, the European Accessibility Act and EN 301 549, UK and Canada, and reducing legal risk."
sources:
  - https://www.ada.gov/resources/web-guidance/
  - https://www.federalregister.gov/documents/2024/04/24/2024-07758/nondiscrimination-on-the-basis-of-disability-accessibility-of-web-information-and-content-of-state
  - https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en
  - https://www.section508.gov/manage/laws-and-policies/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accessibility legal requirements

Not legal advice: confirm obligations with counsel for your jurisdictions. The technical target is usually a WCAG conformance level; check the law for your market.

## 1. United States
- **ADA Title III** (businesses open to the public): the DOJ web accessibility guidance (March 2022) points to technical standards such as WCAG and Section 508; there is no technical regulation for private websites.
- **ADA Title II** (state and local government): web content requirements were published in the Federal Register on 24 April 2024; check ADA.gov for the technical standard and compliance dates.
- **Section 508** (federal agencies and what they procure): the 508 edition of the VPAT incorporates WCAG 2.0; vendors provide an ACR based on the VPAT.
- State laws may add further obligations; ask counsel.

## 2. European Union
- **European Accessibility Act**: a directive covering products and services the EU identified as most important for persons with disabilities; Member States had to transpose it by June 2022. Check the European Commission page for scope and application date.
- **Web Accessibility Directive**: public-sector sites and apps; an accessibility statement is required (see the W3C accessibility statements page).

## 3. Elsewhere
- Other jurisdictions (UK, Canada, Australia and more) have their own laws; use the W3C list of Web Accessibility Laws & Policies.

## 4. Reducing risk in practice
1. Adopt WCAG 2.2 AA as the internal standard (covers 2.1 and 2.0).
2. Audit key journeys, fix, and retest; keep records.
3. Publish an accessibility statement with known issues, alternatives and a contact route; respond to complaints quickly.
4. Build accessibility into procurement (ask for ACRs) and the design system.
5. Avoid relying on overlay widgets as a compliance strategy.

## Verify
- [ ] Applicable laws identified per market; WCAG target documented; current audit and accessibility statement published; complaint process staffed.

## Checked

2026-10-28. Confirmed in ADA.gov web guidance (March 2022 guidance; April 24, 2024 Federal Register requirements for state and local governments), the ITI VPAT page (508 edition incorporates WCAG 2.0; EU edition) and the European Commission EAA page (transposition by June 2022). Removed: lawsuit counts, 2026/2027 compliance dates and population thresholds, WCAG 2.1 AA mandate wording, EAA application date and directive numbers, state-law example, UK, Canada and Australia details, WCAG-EM reference.

Method: documentation only; no commands were run.
