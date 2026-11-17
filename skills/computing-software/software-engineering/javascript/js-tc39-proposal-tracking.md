---
id: computing-software.software-engineering.javascript.js-tc39-proposal-tracking
name: js-tc39-proposal-tracking
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, tc39-proposals, js-versions]
level: advanced
status: draft
description: "Follow TC39 proposals and decide how to use them via Babel/TypeScript."
sources: ["https://tc39.es/process-document/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tracking TC39 proposals and decorators

- Track at github.com/tc39/proposals (active, finished, stage 3) and meeting notes.
- Babel plugins for proposals: `@babel/plugin-proposal-*` renamed `@babel/plugin-transform-*` once stage 4; check plugin names per release.
- Decorators: the standard (2023-11 stage 3) differs from legacy TypeScript `experimentalDecorators`; do not mix them in one project.
- Pipeline operator, records and tuples, and others have changed or stalled; avoid building on stage 1-2.
- Pin tool versions and read release notes when upgrading.

Self-check: list every proposal-stage syntax in your codebase and its stage.
