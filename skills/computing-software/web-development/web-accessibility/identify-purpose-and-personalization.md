---
id: computing-software.web-development.web-accessibility.identify-purpose-and-personalization
name: identify-purpose-and-personalization
category: computing-software
field: web-development
product: web-accessibility
tags: [identify-purpose, wcag-1-3-6, wcag-1-3-5, personalization-semantics, autocomplete]
level: advanced
status: docs-checked
description: "WCAG 1.3.6 Identify Purpose (AAA) and 1.3.5: exposing the purpose of regions, controls and icons with landmarks, autocomplete and ARIA so users' tools can personalise the UI."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/identify-purpose.html
  - https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html
  - https://www.w3.org/TR/adapt-symbols/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identify purpose (1.3.6) and personalization semantics

Users with cognitive and learning disabilities may use tools that simplify pages, replace icons with familiar symbols, or hide non-essential content. These tools need machine-readable purpose.

## 1. 1.3.5 Identify Input Purpose (AA) recap
Inputs collecting user data use the HTML `autocomplete` tokens (`name`, `email`, `tel`, `street-address`, `bday`, `cc-number`...). This lets browsers autofill and lets tools add icons or labels.

## 2. 1.3.6 Identify Purpose (AAA)
"In content implemented using markup languages, the purpose of user interface components, icons, and regions can be programmatically determined."
Techniques available today:
- **Regions**: ARIA landmarks / HTML sectioning (`<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`, `role="search"` / `<search>`), with labels when repeated (`<nav aria-label="Breadcrumb">`).
- **Controls**: native elements and correct roles; accessible names that use common words ("Search", "Close", "Help") rather than clever copy.
- **Icons**: consistent icons for the same function site-wide, with text labels or accessible names; inline SVG with `<title>` or `aria-label`.

## 3. WAI-Adapt
W3C's WAI-Adapt modules define vocabularies for tagging content so personalisation tools can transform it; the Symbols module defines an `adapt-symbol` attribute whose values come from the WAI-Adapt registry. The modules are drafts (the Symbols source in the w3c/adapt repository is an Editor's Draft): treat them as an optional enhancement, not a conformance technique you can rely on.

## 4. Practical checklist
- Every page has `main`, primary `nav`, `header`/`footer` landmarks; repeated landmarks labelled.
- All personal-data inputs carry correct `autocomplete`.
- Icon-only buttons have names; the same icon always means the same action.
- Non-essential content (promos, related links) is in `aside` or labelled regions so tools can hide it.

## Verify
- [ ] Landmarks listed correctly in a screen reader rotor; autocomplete tokens validated (axe `autocomplete-valid`); icon meanings consistent across the site.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text: 1.3.5 Identify Input Purpose is Level AA and 1.3.6 Identify Purpose is Level AAA (quoted SC text matches); MDN lists the autocomplete tokens name, email, tel, street-address, bday and cc-number and the search element; axe has the autocomplete-valid rule; the w3c/adapt repository defines adapt-symbol and its Symbols module is an Editor's Draft. Removed the unconfirmed microdata claim and the other adapt-* attribute names.

Method: documentation only; no commands were run.
