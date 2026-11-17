---
id: computing-software.rpa-and-low-code.uipath.uipath-regex-matches
name: uipath-regex-matches
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-string-regex-json, uipath-regex-matches]
level: practitioner
status: draft
description: "Use .NET regex via Matches and Is Match."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Extract with Regex
**Goal:** Use .NET regex via Matches and Is Match.

- `System.Text.RegularExpressions.Regex.Matches(text, pattern)`; use named groups.
- Test patterns before use and escape backslashes.
- Use Regex builder in Studio.

## Gotchas
- Greedy patterns over-capture; use lazy quantifiers or anchors.

## Self-check
Pattern matches the sample set.
