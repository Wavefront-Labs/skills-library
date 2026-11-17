---
id: computing-software.software-engineering.ruby.ruby-rubocop
name: ruby-rubocop
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-testing-style, rubocop]
level: practitioner
status: draft
description: "Configure RuboCop cops, inherit rules, autocorrect safely and manage TODO baselines."
sources: ["https://docs.ruby-lang.org/en/", "https://www.ruby-lang.org/en/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RuboCop configuration and autocorrect
- `.rubocop.yml` with `AllCops: NewCops: enable`, `TargetRubyVersion`, per-cop `Exclude`/`Max`; `rubocop -a` (safe autocorrect) vs `-A` (includes unsafe, review diffs).
- `rubocop --auto-gen-config` creates `.rubocop_todo.yml` baseline; plugins `rubocop-rails`, `rubocop-rspec`, `rubocop-performance`.
- Follow the community Ruby Style Guide: 2-space indent, snake_case methods, CamelCase classes, `?` predicate and `!` dangerous method suffixes.
Verify: run in CI as a required check.
