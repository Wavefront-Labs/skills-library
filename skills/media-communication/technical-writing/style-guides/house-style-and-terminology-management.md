---
id: media-communication.technical-writing.style-guides.house-style-and-terminology-management
name: house-style-and-terminology-management
category: media-communication
field: technical-writing
product: style-guides
tags: [style-guides, style-guide, house-style, terminology, terminology-management, termbase, glossary, voice-and-tone, prose-linting, vale, write-good, microsoft-writing-style-guide, google-developer-style-guide, chicago-manual-of-style, ap-style, consistency, word-list, capitalisation, localisation, translation-memory, docs-governance, editorial-standards]
level: practitioner
status: draft
description: "Keep a documentation set consistent: build a lean house style guide on a base guide, manage terminology in a termbase, define voice and tone, and enforce it automatically with Vale prose linting."
sources: ["https://vale.sh/docs/", "https://learn.microsoft.com/en-us/style-guide/welcome/", "https://developers.google.com/style"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# House style and terminology management

**Goal:** many writers, one consistent voice and vocabulary — achieved with a short
house guide, a maintained term list, and automated checks rather than memory and
review-time arguments.

## 1. Don't write a style guide from scratch
Adopt a **base guide** and document only your exceptions and additions:
- Software/tech docs: Microsoft Writing Style Guide or Google developer documentation
  style guide (both free online).
- Publishing/general: Chicago Manual of Style; news: AP Stylebook; UK: a house guide
  such as the Guardian's or GOV.UK's style guide as a model.
Your house guide then says "We follow <base> except: …". Keep it to what writers
actually get wrong — typically 10–20 pages, not 100.

## 2. What the house guide should cover
- **Voice and tone:** 3–4 voice attributes with *do/don't* examples ("Direct: 'Delete the
  file.' not 'You may wish to consider deleting the file.'"). Tone varies by context
  (error message vs marketing page); voice doesn't.
- **Mechanics decisions:** spelling variant (US/UK), serial comma, heading case
  (sentence case is easier), numbers (numerals vs words), dates and times, units.
- **UI and code conventions:** bold for UI labels, code font for commands/filenames/values,
  placeholder format (`<PLACEHOLDER>`), how to write key combinations.
- **Inclusive language:** e.g. allowlist/denylist, primary/replica; avoid ableist idioms.
- **Accessibility:** link text, alt text, heading order, no direction-only instructions
  ("click the button on the right").
- **Word list** (see below).
Include an example for every rule. Rules without examples get misapplied.

## 3. Terminology management
- Keep a **termbase** (a spreadsheet is fine to start): `term | status (preferred /
  allowed / forbidden) | definition | part of speech | context/notes | forbidden synonyms
  | owner | date`.
- One concept = one term: decide "sign in" vs "log in" vs "login" (noun vs verb!), and
  record the forbidden variants.
- Product names: exact capitalisation and trademarks; how to refer on second mention.
- Source new terms from product/engineering early — rename before docs ship, not after.
- If you localise, share the termbase with translators and lock product names as
  do-not-translate; consistent source terms cut translation-memory cost.

## 4. Automate with a prose linter (Vale)
Vale checks Markdown, AsciiDoc, reStructuredText, HTML and more against rule files (YAML).
1. Add `.vale.ini` at the repo root:
   ```ini
   StylesPath = styles
   MinAlertLevel = suggestion
   Packages = Microsoft
   [*.md]
   BasedOnStyles = Vale, Microsoft, House
   ```
2. `vale sync` downloads packages; put house rules in `styles/House/`.
3. A **substitution** rule turns the termbase into checks:
   ```yaml
   # styles/House/Terms.yml
   extends: substitution
   message: "Use '%s' instead of '%s'."
   level: error
   ignorecase: true
   swap:
     log into: sign in to
     e-mail: email
   ```
4. Add product terms to the accepted vocabulary (`styles/config/vocabularies/<Name>/accept.txt`
   in recent Vale versions — *path changed across versions; check your Vale docs*) so
   the spell check doesn't flag them.
5. Run `vale docs/` in CI; start rules at `warning`, promote to `error` once the backlog is clean.
Lint catches mechanics and terms; humans still review clarity and accuracy.

## 5. Governance
- One **owner** of the guide; a lightweight change process (issue › discuss › decide › log).
- Changelog for the guide; announce changes.
- Don't retroactively mass-edit for minor rules; fix pages as they're touched, unless
  it's a term change that confuses users.

## Gotchas
- A guide nobody can find or search goes unused — link it from the docs repo README and templates.
- Too many lint errors at once → writers ignore or disable the linter.
- Conflicting rules between base guide and house guide; the house guide must say which wins.

## Verify
- [ ] House guide names its base guide and lists only exceptions/additions, each with an example.
- [ ] Termbase exists with preferred and forbidden terms and an owner.
- [ ] Vale (or equivalent) runs in CI with house term rules.
- [ ] A random page sample shows no forbidden term variants.
- [ ] The guide has a changelog with a recent entry.
