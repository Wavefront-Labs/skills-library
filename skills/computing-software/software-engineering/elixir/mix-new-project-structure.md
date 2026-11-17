---
id: computing-software.software-engineering.elixir.mix-new-project-structure
name: mix-new-project-structure
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, mix-new, mix-exs, mix-compile, mix-run, project-structure, elixirc-paths, mix-env, mix-project, elixir-mix-build]
level: intro
status: docs-checked
description: "Create projects with mix new, read mix.exs (project/0, application/0, deps/0), and use common mix commands and environments."
sources: ["https://hexdocs.pm/mix/Mix.html", "https://hexdocs.pm/elixir/introduction-to-mix.html", "https://hexdocs.pm/mix/Mix.Tasks.New.html", "https://hexdocs.pm/mix/Mix.Tasks.Compile.html", "https://hexdocs.pm/mix/Mix.Tasks.Run.html", "https://hexdocs.pm/mix/Mix.Tasks.Clean.html", "https://hexdocs.pm/mix/Mix.Tasks.Deps.Clean.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mix new, mix.exs and compilation

**Goal:** navigate and drive a Mix project.

```bash
mix new my_app --sup            # app with a supervision tree and application callback; --umbrella for an umbrella project
mix deps.get ; mix compile ; mix test ; mix run -e "IO.puts(1)" ; iex -S mix
MIX_ENV=prod mix compile ; mix help ; mix help test
mix compile --warnings-as-errors ; mix clean ; mix deps.clean --all
```
```elixir
# mix.exs
def project, do: [app: :my_app, version: "0.1.0", elixir: "~> 1.17",
                  start_permanent: Mix.env() == :prod,
                  deps: deps(), aliases: aliases()]
```

## Rules
- Environments are `dev` (default), `test` (what `mix test` runs in) and `prod`, chosen with `MIX_ENV`; compilation artefacts go under `_build`. A dependency runs in `prod` unless its `:env` option says otherwise.
- `start_permanent: Mix.env() == :prod` starts the app in permanent mode in prod, so the VM crashes if the supervision tree shuts down; dev and test stay up for troubleshooting.
- Always commit `mix.lock` (see the Hex usage guide).
- `mix compile --warnings-as-errors` exits non-zero if the project (not its dependencies) has compile warnings; `mix format --check-formatted` is the introduction's recommended CI check; `mix clean` deletes the project's build artefacts in all environments unless `--only` is given.
- `mix deps.clean --all` deletes all dependencies' files; `mix run -e "EXPR"` evaluates code in the application context, and `mix run --no-halt` is for long-running systems.

## Self-check
Run `mix help` and `mix help compile` and find the flags for warnings.

## Checked

Checked 2026-11-08 against the pages for Mix, the introduction to Mix, `mix new`, `mix compile`, `mix run`, `mix clean` and `mix deps.clean`. Removed: the `elixirc_paths` example, the ignore-`_build/`-and-`deps/` advice, the `_build/<env>` layout and the minimum-version advice for `elixir:`, none of which the pages state.

Method: docs-only read of cited pages, 2026-11-08
