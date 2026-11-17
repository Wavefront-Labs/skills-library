---
id: computing-software.web-development.phoenix.containers
name: containers
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, deployment, containers, docker, dockerfile, releases, multi-stage, production]
level: advanced
status: docs-checked
description: "Build a Phoenix container image with mix phx.gen.release --docker: the multi-stage Dockerfile layout and what to configure to deploy it."
sources:
  - https://github.com/phoenixframework/phoenix/blob/main/guides/deployment/containers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: assemble a Phoenix release inside a Docker image and deploy it.

## Generate the Dockerfile
```console
$ mix phx.gen.release --docker
```
This writes a multi-stage Dockerfile (versions in the guide's sample are placeholders for whatever the generator emits). Structure:

- ARGs `ELIXIR_VERSION`, `OTP_VERSION`, `DEBIAN_VERSION`, combined into `BUILDER_IMAGE` (`hexpm/elixir:${ELIXIR_VERSION}-erlang-${OTP_VERSION}-debian-${DEBIAN_VERSION}`) and `RUNNER_IMAGE` (`debian:${DEBIAN_VERSION}`). Find tags on Docker Hub or Hex's build server (Bob). Use the same Debian version for both. Debian/Ubuntu is suggested over Alpine to avoid production compatibility problems (DNS resolution failures, dynamically linked NIFs/precompiled binaries).
- Builder stage: install `build-essential git`, `WORKDIR /app`, `mix local.hex --force && mix local.rebar --force`, `ENV MIX_ENV="prod"`, copy `mix.exs mix.lock`, `mix deps.get --only $MIX_ENV`, copy `config/config.exs` and `config/${MIX_ENV}.exs` before `mix deps.compile` (so config changes recompile deps), `mix assets.setup`, copy `priv` and `lib`, `mix compile`, copy `assets`, `mix assets.deploy`, copy `config/runtime.exs` last (changes there need no recompile), copy `rel`, `mix release`.
- Final stage `FROM ${RUNNER_IMAGE} AS final`: install `libstdc++6 openssl libncurses6 locales ca-certificates`, generate the `en_US.UTF-8` locale and set `LANG`, `LANGUAGE`, `LC_ALL`, `WORKDIR "/app"`, `chown nobody /app`, copy only the release: `COPY --from=builder --chown=nobody:root /app/_build/${MIX_ENV}/rel/my_app ./`, `USER nobody`, `CMD ["/app/bin/server"]`.

`my_app` is your app's name. If your platform does not reap zombie processes, the template suggests adding an init such as tini (commented `ENTRYPOINT ["/tini", "--"]`).

## To deploy the image
- Set environment variables, at least `SECRET_KEY_BASE` (`mix phx.gen.secret`) and `DATABASE_URL`; they are read from `config/runtime.exs`. Do more at runtime for reusable images; keep secrets (DB credentials, API keys) out of the image and supply them from the platform.
- Configure database migrations (platform hook, or edit the server command; see the releases guide).
- Configure clustering; it is needed for long-polling to work, otherwise long-polling must be disabled.

Related: computing-software.web-development.phoenix.releases

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Source switched to the guide in the Phoenix repository because the guide is not published on hexdocs.

Method: documentation only; no commands were run.
