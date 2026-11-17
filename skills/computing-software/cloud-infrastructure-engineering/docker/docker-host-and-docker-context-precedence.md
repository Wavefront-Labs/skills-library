---
id: computing-software.cloud-infrastructure-engineering.docker.docker-host-and-docker-context-precedence
name: docker-host-and-docker-context-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-context, docker-host-env, docker-context-env, docker-config, remote-daemon, cli-configuration]
level: practitioner
status: docs-checked
description: "Know which daemon a docker command talks to: --host, --context, DOCKER_HOST, DOCKER_CONTEXT and config.json currentContext precedence, plus related TLS and config env vars."
sources: ["https://docs.docker.com/engine/manage-resources/contexts/", "https://docs.docker.com/reference/cli/docker/#environment-variables", "https://github.com/docker/cli/blob/master/cli/command/cli.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DOCKER_HOST and DOCKER_CONTEXT precedence

"Why is this command hitting production?" usually comes down to a forgotten env var.

## Order (first match wins)
How the CLI picks the context, from its source (`resolveContextName` in docker/cli):
1. `--context` flag
2. `--host` / `-H` flag, or a non-empty `DOCKER_HOST`: the `default` context is used with that host
3. `DOCKER_CONTEXT` environment variable
4. `currentContext` in `~/.docker/config.json` (set by `docker context use`)
5. The `default` context (local socket)

Passing both `--context` and `--host` is an error (`conflicting options: cannot specify both --host and --context`). `DOCKER_HOST` therefore overrides a context chosen with `docker context use` or `DOCKER_CONTEXT`, and `docker context ls` prints a warning that the `DOCKER_HOST` variable overrides the active context. The reference page's wording says `DOCKER_CONTEXT` overrides `DOCKER_HOST`; the source above is what the CLI does, so unset `DOCKER_HOST` when a context seems ignored.

## See where you are
```bash
docker context ls                       # * marks the active one; warning if DOCKER_HOST is set
docker context show
env | grep -E '^DOCKER_(HOST|CONTEXT|TLS_VERIFY|CERT_PATH|CONFIG)='
docker info -f '{{.Name}} {{.ServerVersion}}'    # name and version of the daemon actually reached
```

## Related variables
| Variable | Effect |
|---|---|
| `DOCKER_TLS_VERIFY=1`, `DOCKER_CERT_PATH` | TLS settings for `tcp://` hosts; used by both the CLI and `dockerd` (a context holds TLS material itself) |
| `DOCKER_CONFIG` | Location of the client configuration files |
| `DOCKER_API_VERSION` | Override the negotiated API version (debugging) |
| `BUILDX_BUILDER` | Builder instance to use |
| `COMPOSE_PROJECT_NAME`, `COMPOSE_FILE` | Compose project name and file selection |

## Safe habits
- Prefer named contexts over exported `DOCKER_HOST`; put the context in the prompt
  (`docker context show` in PS1) for production access.
- Scripts: pass `--context prod` explicitly rather than relying on global state.
- CI: use an isolated `DOCKER_CONFIG` directory per job so contexts and credentials do not leak between jobs.
- `unset DOCKER_HOST` is the first troubleshooting step when contexts "do not work".

## Gotchas
- A stale `DOCKER_HOST` exported in a shell profile silently redirects every command; check `env` first.
- Contexts live under `~/.docker/contexts/` (a `meta.json` per context) in the config directory, so a different user or `DOCKER_CONFIG` sees different contexts.

## Checked

Checked against docker/cli `cli/command/cli.go` (`resolveContextName`) and `cli/command/context/list.go`, and docker/docs `engine/manage-resources/contexts.md` and the `docker` command reference (docker/docs latest commit 2026-10-23, Engine 29).

- Resolution order and the `--host`/`--context` conflict error come from the CLI source; `docker context ls` warns when `DOCKER_HOST` overrides the active context.
- Environment variable descriptions (`DOCKER_CONFIG`, `DOCKER_API_VERSION`, `DOCKER_CERT_PATH`, `DOCKER_TLS_VERIFY`, `BUILDX_BUILDER`, Compose variables) match the docs. `docker context show` exists.
- Noted discrepancy: the documentation says `DOCKER_CONTEXT` overrides `DOCKER_HOST`, while the source resolves `DOCKER_HOST` first.
- Removed as unconfirmed: the Docker Desktop context name, the WSL `DOCKER_HOST` remark and the `sudo` config remark.

Method: documentation only; no commands were run.
