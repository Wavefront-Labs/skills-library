---
id: computing-software.software-engineering.elixir.credo-config-strict-checks
name: credo-config-strict-checks
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, credo, mix-credo, credo-exs, strict, checks, priorities, credo-disable, credo-gen-config, credo-config, elixir-credo]
level: practitioner
status: draft
description: "Add Credo, run mix credo --strict, generate .credo.exs, enable or disable checks and add inline disable comments sparingly."
sources: ["https://hexdocs.pm/credo"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Credo setup, strict mode and .credo.exs

**Goal:** consistent code-quality checks in CI.

```bash
mix credo gen.config                 # writes .credo.exs
mix credo ; mix credo --strict ; mix credo suggest --format oneline
mix credo explain lib/foo.ex:12:5    # why a finding was reported and how to fix
mix credo diff --from-git-merge-base origin/main
```
```elixir
# .credo.exs (inside configs: [%{name: "default", checks: %{enabled: [ ... ], disabled: [ ... ]}}])
{Credo.Check.Readability.MaxLineLength, [max_length: 120]},
{Credo.Check.Design.TagTODO, [exit_status: 0]},
# inline: # credo:disable-for-next-line Credo.Check.Readability.Specs
```

## Rules
- Categories: Consistency, Design, Readability, Refactoring opportunities, Warnings.
- `--strict` includes lower-priority findings; start default and tighten gradually.
- Add `{:credo, "~> 1.7", only: [:dev, :test], runtime: false}`.
- Credo does not format code or find type errors; combine with `mix format` and Dialyzer.
- Prefer fixing findings over disabling; record any disabling reason in a comment.

## Self-check
Run `mix credo explain` on one finding and apply the suggestion.
