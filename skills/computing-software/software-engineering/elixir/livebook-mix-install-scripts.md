---
id: computing-software.software-engineering.elixir.livebook-mix-install-scripts
name: livebook-mix-install-scripts
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, livebook, mix-install, elixir-script, exs, notebook, smart-cells, kino, livebook-mix-install, elixir-notebooks-data]
level: intro
status: draft
description: "Prototype with Livebook notebooks and run single-file scripts with Mix.install; know caching, version pinning and reproducibility limits."
sources: ["https://hexdocs.pm/mix/Mix.html#install/2", "https://livebook.dev"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Livebook and Mix.install for scripting

**Goal:** quick, reproducible experiments and scripts.

```elixir
Mix.install([{:req, "~> 0.5"}, {:jason, "~> 1.4"}], force: false)
resp = Req.get!("https://example.com")
IO.inspect(resp.status)
```
```bash
elixir script.exs               # no project needed; deps cached under the Mix home
mix run --no-halt script.exs
```

## Rules
- `Mix.install/2` must run once at the top; changing the dependency list requires restarting the runtime.
- Dependencies compile on first run (can be slow) and are cached keyed by the install configuration.
- Livebook notebooks (`.livemd`) are Markdown with code cells; the setup cell holds `Mix.install`. Kino provides inputs and visualisations.
- For project code use `mix.exs`; scripts are for exploration, not services.
- Commit `.livemd` files with pinned versions and a note on needed secrets (Livebook secrets, not hard-coded).

## Self-check
Write a script that fetches JSON with Req and prints a field, run with `elixir script.exs`.
