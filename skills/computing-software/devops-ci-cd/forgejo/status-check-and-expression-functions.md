---
id: computing-software.devops-ci-cd.forgejo.status-check-and-expression-functions
name: status-check-and-expression-functions
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [success-function, always-function, hashfiles, format-function]
level: practitioner
status: docs-checked
description: "Pick the right if: status function and use contains, format, join, fromJSON, hashFiles and case in expressions."
sources:
  - https://forgejo.org/docs/latest/user/actions/basic-concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Status functions for `if:` on jobs and steps:

- `success()` is true when no previous job or step failed or was cancelled.
- `failure()` is true when any previous step or job failed.
- `always()` runs even when cancelled. The docs recommend `'!cancelled()'` instead to run regardless of success or failure; quote it so YAML does not read it as a tag.

General functions (`contains`, `startsWith` and `endsWith` are not case sensitive and cast values to strings; `join` also casts values to strings):

- `contains(search, item)` works for substrings or array elements.
- `startsWith(searchString, searchValue)` and `endsWith(...)`.
- `format(string, v0, v1, ...)` uses `{N}` placeholders; escape curly braces by doubling them. At least one replacement value is required.
- `join(array, optionalSeparator)` defaults to the `,` separator.
- `toJSON(value)` pretty-prints; `fromJSON(value)` turns a string into an object or data type.
- `hashFiles(pattern[, ...])` hashes the concatenated content of matching files and returns an empty string if none exist. It is a JavaScript function executed in the container running the action and requires Node.js to be installed.
- `case(predicate1, value1, ..., default)` returns the first matching value; predicates must be booleans, the `default` argument must always be present and there must be an odd number of arguments.

## Checked

Date: 2026-11-07
Confirmed against the "Forgejo Actions | Basic concepts" page, read in full (Conditionals and Functions sections and the string-conversion table): `success()`, `failure()`, `always()` and the recommended quoted `'!cancelled()'`, and the signatures and behaviour of `contains`, `startsWith`, `endsWith`, `format` (including `{N}` placeholders, at least one replace value, doubled braces), `join` (default separator `,`), `toJSON`, `fromJSON`, `hashFiles` and `case`.
Corrected: the skill said all general functions are case-insensitive; the page says that only for `contains`, `startsWith` and `endsWith`. Added the `hashFiles` Node.js requirement and the `case` predicate rule from the page.
Method: documentation only; no commands were run.
