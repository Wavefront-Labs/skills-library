---
id: computing-software.software-engineering.elixir.umbrella-apps-in-umbrella
name: umbrella-apps-in-umbrella
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, umbrella, in-umbrella, apps-dir, umbrella-vs-single, poncho-projects, mix-new-umbrella, umbrella-apps, elixir-umbrella]
level: advanced
status: draft
description: "Create an umbrella with apps/ children, share dependencies via in_umbrella and weigh it against a single app with contexts or poncho projects."
sources: ["https://hexdocs.pm/elixir/dependencies-and-umbrella-projects.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Umbrella projects

**Goal:** know when and how to split into multiple apps.

```bash
mix new my_system --umbrella
cd my_system/apps && mix new core && mix phx.new.web web   # web is the Phoenix app (phx.new.web is Phoenix's generator)
```
```elixir
# apps/web/mix.exs
{:core, in_umbrella: true}
# umbrella root config applies to all apps; build_path/config_path/deps_path/lockfile are shared
```

## Rules
- All apps share one `deps/`, `_build`, `mix.lock` and config; running `mix test` at the root runs every app (`mix cmd --app x mix test` for one).
- Use umbrellas for separate deployable units or to enforce compile-time boundaries; a single app with well-separated contexts is simpler for most teams.
- Dependency cycles between umbrella apps are rejected.
- Apps cannot have different versions of the same dependency.
- Alternatives: poncho projects (path dependencies between independent apps), or umbrella-like tooling with boundary checks via the Boundary library (unconfirmed current status).

## Self-check
Add `{:core, in_umbrella: true}` to `web` and call a `Core` function from IEx at the umbrella root.
