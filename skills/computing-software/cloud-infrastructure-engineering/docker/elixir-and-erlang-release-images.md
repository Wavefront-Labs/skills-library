---
id: computing-software.cloud-infrastructure-engineering.docker.elixir-and-erlang-release-images
name: elixir-and-erlang-release-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, language-images, elixir-release, mix-release, erlang, phoenix, multi-stage]
level: practitioner
status: docs-checked
description: "Package Elixir/Phoenix apps with mix release in a multi-stage build: matching OTP/glibc between builder and runner, assets, runtime config, and clustering/epmd notes."
sources: ["https://hexdocs.pm/phoenix/releases.html#containers", "https://hexdocs.pm/mix/Mix.Tasks.Release.html", "https://hub.docker.com/r/hexpm/elixir"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elixir/Erlang release images

A Mix release bundles the BEAM, your compiled code and dependencies. The runtime image needs
only the system libraries the ERTS was built against.

## Dockerfile (Phoenix style)
```dockerfile
# syntax=docker/dockerfile:1
# pick tags that exist on https://hub.docker.com/r/hexpm/elixir
ARG ELIXIR=<ELIXIR_VERSION>
ARG OTP=<OTP_VERSION>
ARG DEBIAN=<DEBIAN_TAG>
FROM hexpm/elixir:${ELIXIR}-erlang-${OTP}-debian-${DEBIAN} AS build
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
ENV MIX_ENV=prod
RUN mix local.hex --force && mix local.rebar --force
COPY mix.exs mix.lock ./
RUN mix deps.get --only prod && mkdir config
COPY config/config.exs config/prod.exs config/
RUN mix deps.compile
COPY priv priv
COPY assets assets
COPY lib lib
RUN mix assets.deploy && mix compile
COPY config/runtime.exs config/
RUN mix release

FROM debian:${DEBIAN} AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends libstdc++6 openssl libncurses6 locales ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && sed -i '/en_US.UTF-8/s/^# //' /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 MIX_ENV=prod
WORKDIR /app
RUN useradd -r -u 10001 app && chown app /app
COPY --from=build --chown=app:root /app/_build/prod/rel/myapp ./
USER app
CMD ["/app/bin/server"]
```
`mix phx.gen.release --docker` generates essentially this file.

## Rules
- Builder and runtime must share the **same Debian release** (glibc, OpenSSL ABI): pin both
  from the same `DEBIAN` arg. A mismatch shows up as missing shared-library errors at boot.
- Order copies so `deps.compile` stays cached: `mix.exs`/`mix.lock` and compile-time config
  first, `lib` last. `runtime.exs` is copied after compile so changing it does not recompile.
- Runtime config comes from env in `config/runtime.exs` (`DATABASE_URL`, `SECRET_KEY_BASE`), never baked at build time.
- Migrations: run `bin/myapp eval "MyApp.Release.migrate"` (a function you define, per the Phoenix releases guide) as a one-off container or a Compose service with `depends_on` ordering.

## Clustering
- Distributed Erlang needs a resolvable node name: set `RELEASE_DISTRIBUTION=name` and `RELEASE_NODE` (see the `Mix.Tasks.Release` page for the release environment variables).

## Verify
```bash
docker run --rm myapp /app/bin/myapp version
docker run --rm -e SECRET_KEY_BASE=$(openssl rand -base64 48) -p 4000:4000 myapp
```

## Checked
2026-10-28. Confirmed against the Phoenix releases guide (containers section) and `Mix.Tasks.Release`: `mix phx.gen.release --docker`, runtime config in `config/runtime.exs` copied after compile, `eval "MyApp.Release.migrate"`, `bin/server` overlay, `RELEASE_DISTRIBUTION=name` and `RELEASE_NODE`. Removed: pinned Elixir/OTP/Debian versions (use tags from Docker Hub hexpm/elixir), epmd and `inet_dist_listen` port details, the specific libcrypto error text, libcluster note, `PHX_HOST`.
Method: documentation only; no commands were run.
