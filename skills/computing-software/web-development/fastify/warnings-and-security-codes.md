---
id: computing-software.web-development.fastify.warnings-and-security-codes
name: warnings-and-security-codes
category: computing-software
field: web-development
product: fastify
tags: [fastify, warnings, security, fstwrn, fstsec]
level: intro
status: docs-checked
description: "Meaning and fixes for FSTWRN001, FSTWRN003, FSTSEC001-003 and how to disable or trace warnings."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Warnings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fastify uses Node's warning event; codes start with `FSTWRN`, `FSTSEC` or `FSTDEP`.

| Code | Meaning | Fix |
| --- | --- | --- |
| FSTWRN001 | A route schema is missing or not well specified | Check the schema |
| FSTWRN003 | A plugin mixes async and callback styles | Use one style |
| FSTSEC001 | A RegExp content type does not anchor the essence MIME type (CORS bypass risk) | Start with `^` or include `;?` |
| FSTSEC002 | Headers schema uses an external `$ref` not reached by header lowercasing | Inline the headers schema |
| FSTSEC003 | Headers schema uses `$ref` in `propertyNames` | Inline the constraint |

Find the cause with `node --trace-warnings` and `--trace-deprecation`. Issues about warnings without those traces get closed.

Disable (not recommended): `NODE_NO_WARNINGS=1`, `--no-warnings`, `no-warnings` in `NODE_OPTIONS`, or one code with `--disable-warning=FSTWRN003`.

There are currently no active deprecation codes: the APIs deprecated in v5 were removed in v6. The v5 migration guide likewise lists FSTDEP codes that were removed in v5.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Warnings.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
