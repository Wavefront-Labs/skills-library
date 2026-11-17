---
id: computing-software.rpa-and-low-code.uipath.uipath-variable-scope-types
name: uipath-variable-scope-types
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-variables-arguments, uipath-variable-scope-types]
level: practitioner
status: draft
description: "Declare variables at the narrowest scope with correct types."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use variable scope and types correctly
**Goal:** Declare variables at the narrowest scope with correct types.

- Variables are scoped to the container where declared; types include String, Int32, Boolean, DataTable, GenericValue and Dictionary.
- Use meaningful names (prefix by type if the team agrees on a convention).
- Initialise before use and avoid reusing across unrelated sections.

## Gotchas
- Out-of-scope variables show a red icon on the activity.

## Self-check
No unused variable warnings in the Workflow Analyzer.
