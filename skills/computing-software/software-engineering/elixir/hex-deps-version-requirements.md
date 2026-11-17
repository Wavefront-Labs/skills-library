---
id: computing-software.software-engineering.elixir.hex-deps-version-requirements
name: hex-deps-version-requirements
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, hex, deps, mix-lock, version-requirements, git-dependency, path-dependency, override, deps-update, hex-deps, elixir-deps-hex]
level: practitioner
status: docs-checked
description: "Declare Hex, git and path dependencies, use ~> requirements, update with mix deps.update and audit with hex.audit/hex.outdated."
sources: ["https://hexdocs.pm/mix/Mix.Tasks.Deps.html", "https://hex.pm/docs/usage", "https://hexdocs.pm/elixir/Version.html", "https://hexdocs.pm/hex/Mix.Tasks.Hex.Audit.html", "https://hexdocs.pm/hex/Mix.Tasks.Hex.Outdated.html", "https://hexdocs.pm/mix/Mix.Tasks.Deps.Update.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declaring dependencies and version requirements

**Goal:** control dependency versions deliberately.

```elixir
defp deps do
  [
    {:phoenix, "~> 1.7"},                       # >= 1.7.0 and < 2.0.0
    {:jason, "~> 1.4.1"},                       # >= 1.4.1 and < 1.5.0
    {:credo, "~> 1.7", only: [:dev, :test], runtime: false},
    {:mylib, git: "https://example.com/mylib.git", tag: "v1.0"},
    {:local, path: "../local"},
    {:shared, in_umbrella: true},
    {:forced, "~> 2.0", override: true}
  ]
end
```
```bash
mix deps.get ; mix deps.update jason ; mix deps.update --all ; mix deps.tree
mix hex.outdated ; mix hex.audit ; mix deps.unlock --unused ; mix hex.info jason   # unlock --unused: no longer in mix.exs
```

## Rules
- Always commit `mix.lock`: Mix locks versions so all developers get the same ones. `mix deps.get` fetches what is not yet fetched; `mix deps.update` updates the named dependency (and the projects it depends on) and writes the lockfile; `--all` is required to update everything.
- To update one dependency without touching its children, run `mix deps.unlock some_dep` then `mix deps.get`.
- `~>` with three parts (`~> 1.4.1`) bounds the minor version; with two parts (`~> 1.7`) it bounds the major version. Hex dependencies need a requirement. Versions follow Semantic Versioning format and requirements are defined by the `Version` module.
- `only:` limits a dependency to the given environments; dependencies run in `prod` unless `:env` is set, so dev- or test-only tools need `only:`.
- `runtime: false` keeps a dependency out of the runtime applications when `applications` is not set in `application/0`.
- `override: true` makes the dependency override other definitions of itself by other dependencies.
- The lockfile is ignored when a project is used as a dependency.
- `mix hex.audit` lists Hex dependencies that are retired or have security advisories and exits non-zero if any are found; `mix hex.outdated` exits 1 by default when anything is outdated, and `--within-requirements` limits that to updates your requirements allow.

## Self-check
Run `mix deps.tree` and find who pulls in a transitive dependency.

## Checked

Checked 2026-11-08 against the pages for `mix deps`, `mix deps.update`, `mix deps.tree`, `mix deps.unlock`, the Hex usage guide, the `Version` module (`~>` translations), `mix hex.audit`, `mix hex.outdated` and `mix hex.info`. Removed: the claim that git and path dependencies cannot be used in a Hex package and the third-party `mix deps.audit` suggestion, neither of which the pages state.

Method: docs-only read of cited pages, 2026-11-08
