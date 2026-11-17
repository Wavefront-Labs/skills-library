---
id: computing-software.software-engineering.elixir.docker-multistage-release
name: docker-multistage-release
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, docker, multi-stage, dockerfile, hexpm-images, mix-phx-gen-release, container, healthcheck, docker-deploy]
level: practitioner
status: docs-checked
description: "Build a multi-stage Docker image: compile the release in an Elixir builder image and copy it into a slim runtime image; use mix phx.gen.release --docker for Phoenix."
sources: ["https://hexdocs.pm/phoenix/releases.html", "https://hub.docker.com/r/hexpm/elixir", "https://hexdocs.pm/mix/Mix.Tasks.Release.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker images for Elixir releases

**Goal:** small, reproducible container for an Elixir release.

```dockerfile
ARG ELIXIR=1.19.6 OTP=28.1.1 DEBIAN=bookworm-20261027-slim   # example tag seen on Docker Hub; pin versions you actually use
FROM hexpm/elixir:${ELIXIR}-erlang-${OTP}-debian-${DEBIAN} AS build
WORKDIR /app
ENV MIX_ENV=prod
RUN mix local.hex --force && mix local.rebar --force
COPY mix.exs mix.lock ./
RUN mix deps.get --only prod
COPY config/config.exs config/prod.exs config/
RUN mix deps.compile
COPY priv priv
COPY lib lib
RUN mix compile
COPY config/runtime.exs config/
RUN mix release

FROM debian:${DEBIAN}
RUN apt-get update && apt-get install -y --no-install-recommends libstdc++6 openssl libncurses6 locales ca-certificates && rm -rf /var/lib/apt/lists/*
ENV LANG=en_US.UTF-8
WORKDIR /app
COPY --from=build /app/_build/prod/rel/my_app ./
USER nobody
CMD ["bin/my_app", "start"]
```

## Rules
- The Phoenix-generated runner stage installs `libstdc++6`, `openssl`, `libncurses6`, `locales` and `ca-certificates`, and sets a UTF-8 locale (it generates `en_US.UTF-8` with `locale-gen`; add that step if you use `en_US.UTF-8` as above). The release guide says the target needs system packages such as OpenSSL for `:crypto`/`:ssl`.
- Copy `mix.exs`/`mix.lock` first, then the compile-time config files (`config.exs`, `prod.exs`) before compiling dependencies, so config changes recompile them; copy `config/runtime.exs` late because changing it does not require recompiling code.
- The generated Dockerfile suggests the same Debian version for builder and runner, and Debian/Ubuntu rather than Alpine to avoid DNS resolution failures and dynamically linked NIF problems.
- Phoenix: `mix phx.gen.release --docker` generates a Dockerfile; `mix phx.gen.release` also generates `server` and `migrate` overlay scripts and a `release.ex` for Ecto migrations without Mix.
- Run as non-root (`USER nobody`). SIGINT/SIGTERM shut the release down, stopping each application and its supervision tree in the reverse order of startup; `bin/my_app stop` does the same.
- If the platform does not reap zombie processes, the generated file advises an init such as tini as the entrypoint.
- When building images under emulation, set `ENV ERL_AFLAGS "+JMsingle true"` in the build stage (JIT issue noted in the release guide).
- Versions above are examples only; Docker Hub tags follow `${ELIXIR_VER}-erlang-${OTP_VER}-${OS_NAME}-${OS_VER}`.

## Self-check
Run the container and `docker exec` into `bin/my_app remote`.

## Checked

Checked 2026-11-08 against the Phoenix releases guide (generated Dockerfile, runner packages, `phx.gen.release`, Alpine advice, tini), the `mix release` page (SIGTERM shutdown, `+JMsingle true`, target requirements) and the hexpm/elixir Docker Hub page (tag scheme, example tag). Removed: the old pinned tags, the `System.stop` detail and the invalid `COPY config lib priv ./` line.

Method: docs-only read of cited pages, 2026-11-08
