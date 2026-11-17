---
id: computing-software.cybersecurity-defensive.application-security.codeql-custom-queries
name: codeql-custom-queries
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [sast, codeql-queries, codeql, ql, data-flow-analysis, code-scanning, query-packs]
level: advanced
status: docs-checked
description: "Write custom CodeQL queries: required query metadata, alert versus path-problem kinds, and testing with .qlref and .expected files via codeql test run."
sources: ["https://codeql.github.com/docs/writing-codeql-queries/metadata-for-codeql-queries/", "https://codeql.github.com/docs/codeql-cli/testing-custom-queries/", "https://codeql.github.com/docs/writing-codeql-queries/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom CodeQL queries

**Goal:** detect organisation-specific vulnerable flows that the default query suites miss.

## Query metadata
Metadata must be correct for results to be viewable in source code; exact requirements depend on how you run
the query (see "About CodeQL queries"). Properties supported by all query files:
- `@name`: the query label, plain text.
- `@description`: purpose and why the result matters.
- `@id`: lowercase letters or digits delimited by `/` or `-`; unique per query. Standard queries use
  `<language>/<brief-description>`.
- `@kind`: `problem` (an alert) or `path-problem` (a path, for data-flow results).
- `@tags`: e.g. `correctness`, `maintainability`, `readability`, `security`.
- `@previous-id`: marks results previously reported under a different query id.

## Testing
A query test consists of example code, a `.qlref` file (location of the query, relative to the root of the
CodeQL pack containing it, usually a pack in the test pack's dependencies) or the `.ql` itself, and a
`.expected` file with the results you expect; the test command can create `.expected` for you. Names must be
consistent: a `.qlref` and its `.expected` share a base name (the query may be named differently). All
example code next to the `.qlref`/`.ql` and in subdirectories is used to build the test database, so do not
nest test directories inside one another.
Run `codeql test run <test|dir>`: a path to a `.qlref`, or a directory searched recursively for `.ql` and
`.qlref` files.

## For everything else
Data-flow and taint-tracking APIs, pack creation, database creation and CI configuration change between
CodeQL versions and languages: read the CodeQL documentation for the language you are targeting.

## Verify
- [ ] Tests include the known-bad sample and sanitised paths, and pass.

## Checked
2026-11-01. Confirmed against the CodeQL "Metadata for CodeQL queries" and "Testing custom queries" pages.
Removed: the Python taint-tracking example (library module names, classes), database-create and pack-init
commands, `--build-mode=none`, code scanning config keys, `@security-severity` and models-as-data advice,
none of which were confirmed on pages read this batch.
Method: documentation only; no commands were run.
