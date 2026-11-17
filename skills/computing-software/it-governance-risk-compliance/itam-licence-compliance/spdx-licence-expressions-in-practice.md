---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.spdx-licence-expressions-in-practice
name: spdx-licence-expressions-in-practice
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [spdx-licence-expressions-in-practice, licence-compatibility-analysis, spdx expression, and, or, with, exception, license expression, gpl-2.0-with-classpath-exception, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Read and evaluate compound SPDX expressions with AND, OR and WITH exceptions to determine applicable obligations."
sources:
  - https://github.com/spdx/spdx-spec/blob/support/2.3/chapters/SPDX-license-expressions.md
  - https://github.com/spdx/license-list-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evaluating SPDX licence expressions (AND, OR, WITH)

Goal: derive obligations from an expression.

Syntax: MIT OR Apache-2.0 means you choose either; MIT AND BSD-3-Clause means both apply; GPL-2.0-only WITH Classpath-exception-2.0 means GPL-2.0 modified by the exception. Parentheses group. Default precedence, applied first to last, is +, WITH, AND, OR, so "A OR B AND C" means A OR (B AND C). A "+" directly after an ID with no space (e.g. CDDL-1.0+) means that version or any later one; the list also has -or-later IDs. Operators AND, OR and WITH are case-sensitive; IDs match case-insensitively.

Method:
- For OR, pick the option that fits (record the choice, e.g. "elected Apache-2.0").
- For AND, comply with all.
- For WITH, apply the exception text.
- Use a parser library and check IDs against the SPDX License List.

Gotchas:
- LicenseRef-* identifiers need the text in the document.
- Deprecated IDs (GPL-2.0 without suffix) should be normalised to -only or -or-later by analysing the original text.

Verify: parser validates expressions without error.

## Checked

2026-11-02. Checked against SPDX 2.3 Annex D (grammar, case rules, +, WITH, AND, OR, precedence, parentheses, LicenseRef) and the spdx/license-list-data JSON (Classpath-exception-2.0 exists; GPL-2.0 is flagged isDeprecatedLicenseId). Removed: the named parser libraries (not in the spec).

Method: documentation only; no commands were run.
