---
id: computing-software.software-engineering.elixir.mix-release-build-run
name: mix-release-build-run
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, mix-release, release, rel-overlays, release-cookie, release-node, bin-start, remote-console, env-sh-eex, elixir-releases]
level: practitioner
status: docs-checked
description: "Build self-contained releases with mix release, configure runtime via runtime.exs and RELEASE_* env vars, and operate them with the generated bin script."
sources: ["https://hexdocs.pm/mix/Mix.Tasks.Release.html", "https://hexdocs.pm/phoenix/releases.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building releases with mix release

**Goal:** package an app that runs without Elixir installed.

```bash
MIX_ENV=prod mix release                 # output: _build/prod/rel/my_app
_build/prod/rel/my_app/bin/my_app start          # foreground
_build/prod/rel/my_app/bin/my_app daemon ; stop ; restart ; pid
_build/prod/rel/my_app/bin/my_app remote         # IEx attached to the running node
_build/prod/rel/my_app/bin/my_app eval "MyApp.Release.migrate()"
mix release.init                         # generates rel/ templates (env.sh.eex, vm.args.eex)
```
```elixir
# mix.exs
releases: [my_app: [include_executables_for: [:unix], applications: [runtime_tools: :permanent],
                    steps: [:assemble, :tar]]]
```

## Rules
- Host and target must match in architecture, vendor and operating system, and ABI (for example `x86_64-unknown-linux-gnu` vs `x86_64-unknown-linux-musl`); NIF dependencies must be compiled for the same triple. The release includes ERTS by default (`include_erts: true`, the recommended value); `false` uses the target's ERTS, which must be the exact same version.
- Env vars include `RELEASE_COOKIE`, `RELEASE_NODE`, `RELEASE_DISTRIBUTION` (`name`, `sname` or `none`; default `sname`), `RELEASE_TMP` (default `$RELEASE_ROOT/tmp`) and `RELEASE_VM_ARGS`; `config/runtime.exs` runs every time the release boots.
- `config/runtime.exs` must `import Config`, must not `import_config` other files and must not access Mix, because Mix is not available inside releases.
- Run migrations through a release module that calls `Ecto.Migrator`, invoked with `bin/my_app eval "MyApp.Release.migrate"` (pattern from the Phoenix release guide).
- `eval` starts a fresh VM without starting the release's applications, so start what you need with `Application.ensure_all_started/1`; `rpc` runs against the already running system.
- `config/config.exs` is build-time configuration, evaluated when the release is assembled; values read with `Application.compile_env/3` are checked against runtime config at boot (`:validate_compile_env`), and a mismatch stops the system booting.
- Cookie: if `:cookie` is not set, a random one is written to `releases/COOKIE` when the first release is assembled; at runtime `RELEASE_COOKIE` is tried first, then `releases/COOKIE`. Use a long random alphanumeric string if you set it yourself.

## Failure modes
- NIFs or dynamically linked system libraries (for example OpenSSL for `:crypto`/`:ssl`) missing or mismatched when the build host differs from the target.

## Self-check
Build a release, `eval "IO.puts(1)"`, and attach with `remote`.

## Checked

Checked 2026-11-08 against the `mix release` task page (bin commands, options, `rel` templates, environment variables, cookie, runtime config, deployment requirements) and the Phoenix releases guide (Ecto.Migrator eval pattern). Removed: the unsourced claim that the cookie must be stable across cluster nodes, and the vague libc wording (the page speaks of target triple and ABI).

Method: docs-only read of cited pages, 2026-11-08
