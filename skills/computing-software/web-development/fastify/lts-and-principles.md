---
id: computing-software.web-development.fastify.lts-and-principles
name: lts-and-principles
category: computing-software
field: web-development
product: fastify
tags: [fastify, lts, versioning, support, principles]
level: intro
status: docs-checked
description: "Fastify support policy and the ten technical principles that guide design decisions."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/LTS.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Principles.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Support policy: a major version is supported for at least 6 months, then gets 6 more months of security updates after the next major ships. v5 was released 2024-09-17; v6 date is TBD. Because of long-term support, breaking changes sometimes ship in minor releases (always documented in the release notes); a tilde range (`~`) avoids them but leaves the application vulnerable, so use it with caution. HeroDevs provides commercial end-of-life support. The LTS schedule table lists the Node.js versions per release; v5 needs Node.js 20+.

The ten principles:
1. "Zero" overhead in production
2. "Good" developer experience
3. Works great for small and big projects alike
4. Easy to migrate to microservices (or serverless) and back
5. Security and data validation
6. If something could be a plugin, it likely should be
7. Easily testable
8. Do not monkeypatch core
9. Semantic versioning and Long Term Support
10. Specification adherence

Implications:
- Binary addons are forbidden because most JavaScript developers have no compiler.
- A web framework is the first point of contact with untrusted data and must act as the first line of defense.
- Catering to every use case in one module would make the codebase unmaintainable, so hooks and options are provided to customize the framework.
- No monkeypatching of Node.js APIs or installing globals that alter the runtime, because that makes modular applications harder to build.
- When in doubt, the strict behavior defined by the spec wins.

Gotcha: do not read "zero overhead" literally; the docs say it can conflict with developer experience and features.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (LTS.md, Principles.md) and confirmed. Removed or corrected: claims the pages do not make (middleware, CORS and static serving as plugins; diagnostics_channel as an extension point; first-class validation), now reworded from the Principles page; the invented Verify step.

Method: documentation only; no commands were run.
