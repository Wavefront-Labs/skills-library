---
id: computing-software.software-engineering.crystal.lucky-amber-athena
name: lucky-amber-athena
category: computing-software
field: software-engineering
product: crystal
tags: [lucky-amber-athena, frameworks, lucky, amber, athena, web-framework, orm, granite, avram, crystal-frameworks, spider-gazelle, shardbox, crystal]
level: practitioner
status: draft
description: "Choose between the full-stack Lucky, the Rails-like Amber and the component-based Athena framework, and where to find others."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lucky, Amber and Athena compared

Goal: pick a framework (confirm each project's current maintenance status before adopting).

- Lucky (luckyframework.org): type-safe full-stack framework; actions as classes, Avram ORM and migrations, type-checked HTML pages (Lucky::HTMLPage), generators via the `lucky` CLI; PostgreSQL focus.
- Amber (amberframework.org): Rails-like MVC with generators, Granite ORM, Jinja/Slang templates, WebSocket channels.
- Athena (athenaframework.org): modular components (routing, dependency injection, validator, console, serializer, event dispatcher) with annotations; more like Symfony.
- Others: Spider-Gazelle (controllers with annotations), Grip, Marten (Django-like), Kemal (micro).
- Data layers: `crystal-db` with `crystal-pg`/`crystal-mysql`/`crystal-sqlite3` drivers, ORMs Avram, Granite, Jennifer, Clear.
- Search: shardbox.org and GitHub topic crystal-lang.

Gotchas:
- Framework ecosystems are smaller than Rails or Django; check last commit dates.
- Annotation- and macro-heavy frameworks give hard compile errors; use `--error-trace`.
- Compile times grow with app size; use `--no-codegen` while iterating.

Verify: generate the framework's hello app and run its spec.
