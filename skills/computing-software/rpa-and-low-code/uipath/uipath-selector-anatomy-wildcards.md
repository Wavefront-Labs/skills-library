---
id: computing-software.rpa-and-low-code.uipath.uipath-selector-anatomy-wildcards
name: uipath-selector-anatomy-wildcards
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-ui-automation-selectors, uipath-selector-anatomy-wildcards]
level: advanced
status: draft
description: "Build stable selectors from XML-like attributes."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Write robust selectors
**Goal:** Build stable selectors from XML-like attributes.

- A selector is a chain of tags (html, webctrl, wnd) with attributes; remove volatile attributes such as dynamic ids and indexes, and use wildcards (`*`, `?`) for variable text.
- Use UI Explorer to validate and adjust; use variables in selectors with `{{variable}}`.
- Prefer stable attributes (name, automation id, aaname).

## Gotchas
- Idx-based selectors break when layout changes.

## Self-check
Selector highlights the right element in UI Explorer across several runs.
