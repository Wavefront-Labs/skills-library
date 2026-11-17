---
id: computing-software.ux-hci-design.wcag-accessibility.language-of-page-and-parts
name: language-of-page-and-parts
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [language-of-page, lang-attribute, wcag-readable-predictable]
level: intro
status: docs-checked
description: "Set the lang attribute on the html element so the default page language is programmatically determinable (SC 3.1.1)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Language
```html
<html lang="de">
```
- SC 3.1.1 (Level A): the default human language of each web page can be programmatically determined. The sufficient technique for HTML is the `lang` attribute on the `html` element (H57).
- When a page uses several languages, the default is the language used most; if several are used equally, the first language used.
- Screen readers can load the correct pronunciation rules from it; visual browsers can display characters and scripts correctly and media players can show captions correctly.
- For multilingual sites, the Working Group strongly encourages SC 3.1.2 Language of Parts (Level AA) as well, even when targeting Level A.

## Verify
- [ ] The HTML page has a `lang` attribute with a valid language tag, and it matches the page's default language (the matching test rules listed on the page are: has lang attribute, valid tag, matching `lang` and `xml:lang`, subtag matches default language).

## Checked

2026-11-09. Confirmed on the Understanding SC 3.1.1 page: the success criterion text and level, the intent and benefits, the default-language rule for multilingual pages, technique H57, the 3.1.2 note and the four test rules. Removed: the French span example and the BCP 47 tag list, the dir="rtl" bullet and the garbled-speech claim, none of which this page states.

Method: documentation only; no commands were run.
