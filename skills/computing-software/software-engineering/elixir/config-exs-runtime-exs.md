---
id: computing-software.software-engineering.elixir.config-exs-runtime-exs
name: config-exs-runtime-exs
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, config-exs, runtime-exs, application-get-env, compile-env, system-get-env, fetch-env-bang, runtime-config, elixir-config]
level: practitioner
status: docs-checked
description: "Know when each config file runs: config.exs at compile time, runtime.exs at boot; read env vars in runtime.exs and use Application.fetch_env! at runtime."
sources: ["https://hexdocs.pm/elixir/Config.html", "https://hexdocs.pm/mix/Mix.Tasks.Release.html", "https://hexdocs.pm/elixir/Application.html", "https://hexdocs.pm/mix/Mix.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# config.exs, runtime.exs and Application.get_env

**Goal:** configure one build for many environments.

```elixir
# config/config.exs (compile time)
import Config
config :my_app, MyApp.Mailer, adapter: Swoosh.Adapters.Local
import_config "#{config_env()}.exs"

# config/runtime.exs (every boot, including releases)
import Config
if config_env() == :prod do
  config :my_app, MyApp.Repo,
    url: System.fetch_env!("DATABASE_URL")
end
# reading
Application.fetch_env!(:my_app, :key) ; Application.get_env(:my_app, :opt, default)
@timeout Application.compile_env(:my_app, :timeout, 5_000)   # compile-time, checked
```

## Rules
- `config/config.exs` and the files it imports (`dev.exs`, `prod.exs`) are build-time configuration, evaluated whenever you compile or assemble a release; a `System.fetch_env!` there is computed on the build host and fails if the variable is missing there. Put secrets and host-specific values in `config/runtime.exs`.
- `config/runtime.exs` is executed right before applications start, in Mix and in releases; it must `import Config`, must not `import_config` other files and must not access Mix.
- Reading the application environment at runtime is the preferred approach. `Application.fetch_env!/2` in a module body (outside a function) draws a warning telling you to use `Application.compile_env/3`; `compile_env` stores the compile-time value and compares it with the runtime value when the system starts.
- Libraries should avoid the application environment (it is global storage), and a library's own `config/config.exs` is not evaluated when it is used as a dependency; pass options explicitly.
- Use `config_env()` (and `config_target()`) instead of `Mix.env()` in config files; outside config and Mix tasks, avoid `Mix.env()` and read a config key such as `config :my_app, env: config_env()` instead.
- `config/2` and `config/3` deep-merge keyword lists.

## Failure modes
- Boot fails with an error when a value read via `Application.compile_env/3` differs at startup from the value used at compile time (releases check this unless `validate_compile_env` is false).

## Self-check
Set `DATABASE_URL` and boot a release; confirm the runtime value is used without rebuilding.

## Checked

Checked 2026-11-08 against the Config module page (config.exs, runtime.exs, `config_env/0`, merge behaviour, library advice), the Application module page (`fetch_env!`, `compile_env/3`, module-body warning) and the Mix and `mix release` pages (build-time versus runtime configuration, `validate_compile_env`). Removed: `System.get_env` pool-size example and the quoted error message text, which the pages do not give.

Method: docs-only read of cited pages, 2026-11-08
