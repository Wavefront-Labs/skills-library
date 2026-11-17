---
id: computing-software.software-engineering.ruby.ruby-yjit-upgrades
name: ruby-yjit-upgrades
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-performance, yjit-upgrades]
level: advanced
status: draft
description: "Enable YJIT, and plan Ruby upgrades via deprecation warnings and EOL dates."
sources: ["https://docs.ruby-lang.org/en/", "https://www.ruby-lang.org/en/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# YJIT and Ruby version upgrades
- YJIT (since 3.1, production-ready from 3.2): `ruby --yjit` or `RUBY_YJIT_ENABLE=1`, check `RubyVM::YJIT.enabled?`; extra memory use.
- Upgrade steps: run tests with `-W:deprecated`, update gems, bump minor versions one at a time; check support status at ruby-lang.org/en/downloads/branches.
Verify: p95 latency and memory comparisons in staging.
