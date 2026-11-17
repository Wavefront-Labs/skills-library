---
id: computing-software.web-development.web-accessibility.plain-language-and-readability
name: plain-language-and-readability
category: computing-software
field: web-development
product: web-accessibility
tags: [readable, predictable, plain-language, reading-level, wcag-3-1-5, unusual-words, abbreviations, cognitive-accessibility, microcopy]
level: practitioner
status: docs-checked
description: "Writing accessible content: plain-language rules, reading level (WCAG 3.1.5), defining abbreviations (3.1.4), and testing readability."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/reading-level.html
  - https://www.w3.org/WAI/WCAG22/Understanding/abbreviations.html
  - https://www.plainlanguage.gov/guidelines/
  - https://www.gov.uk/guidance/content-design/writing-for-gov-uk
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plain language and readability

**Goal:** content most people can understand on first read - including people with cognitive disabilities, low literacy, or reading in a second language.

## 1. WCAG hooks (AAA, but best practice)
- **Unusual words**: define jargon/idioms (glossary link, inline definition, `<dfn>`).
- **3.1.4 Abbreviations**: expand on first use ("multi-factor authentication (MFA)").
- **3.1.5 Reading Level**: if text needs more than the lower secondary education level, provide a simpler summary or version.

## 2. Rules that work
- Lead with what the user needs to do; one idea per sentence.
- Active voice, "you" and "we"; verbs over nouns ("apply" not "make an application").
- Common words ("use" not "utilise", "about" not "approximately").
- Headings as questions or tasks; short paragraphs; bulleted steps; numbered lists for sequences.
- Specific error and button text ("Pay £20.00", not "Submit").
- Dates/numbers in unambiguous formats ("3 March 2026").

## 3. Measure
- Readability scores (Flesch-Kincaid grade, Flesch reading ease) - a signal, not a target (they reward short words, not clarity).
- Better: usability test with real users, including people with low literacy; highlighter testing (users mark confusing parts).

## 4. In code
Microcopy belongs in a reviewed content layer (i18n files) so writers can edit it; keep a terminology list; lint UI strings for banned words (e.g. "click here", "invalid").

## Verify
- [ ] Key journeys' copy checked against your target reading level (with human review).
- [ ] Abbreviations expanded on first use; jargon linked to definitions.
- [ ] Usability test participants complete tasks without asking what text means.

## Checked
2026-10-28 Confirmed on the W3C Understanding pages: SC 3.1.5 Reading Level (AAA) uses the lower secondary education level, SC 3.1.4 Abbreviations (AAA). Removed: age range, sentence-length figure, grade target, the 3.1.3/3.1.6 numbers and the abbr-title claim (not on fetched pages), named readability tools, COGA reference. gov.uk page was a stub.
Method: documentation only; no commands were run.
