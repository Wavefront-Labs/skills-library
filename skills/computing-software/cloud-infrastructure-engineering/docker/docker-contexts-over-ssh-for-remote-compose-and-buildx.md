---
id: computing-software.cloud-infrastructure-engineering.docker.docker-contexts-over-ssh-for-remote-compose-and-buildx
name: docker-contexts-over-ssh-for-remote-compose-and-buildx
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-context, contexts, remote-daemon, docker-context-create, context-switching, ssh-context, ssh-controlmaster, compose-context, remote-context-builds]
level: practitioner
status: docs-checked
description: "Manage remote engines with docker context create/use/export over SSH, reuse the SSH connection with ControlMaster, and run Compose and buildx against remote contexts."
sources: ["https://docs.docker.com/engine/manage-resources/contexts/", "https://docs.docker.com/reference/cli/docker/context/create/", "https://docs.docker.com/reference/cli/docker/context/use/", "https://docs.docker.com/reference/cli/docker/context/export/", "https://docs.docker.com/engine/security/protect-access/", "https://docs.docker.com/reference/cli/docker/buildx/create/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker contexts over SSH for remote Compose and buildx

## Create and switch
```sh
docker context create prod-web --description "prod web-1" --docker "host=ssh://deploy@web-1.example.com"
docker context ls
docker context use prod-web          # persistent: updates ~/.docker/config.json
docker --context prod-web ps         # one command
DOCKER_CONTEXT=prod-web docker ps    # per shell
docker context use default
```
- `docker context use` sets the default context by updating the CLI config
  (`~/.docker/config.json`); it affects every shell and session that shares that config.
  For one-off commands or per-shell use, use `--context` or `DOCKER_CONTEXT`.
- Per the `docker` CLI reference: `-c`/`--context` overrides the `DOCKER_HOST` environment
  variable and the default context set with `docker context use`; `DOCKER_CONTEXT` likewise
  overrides `DOCKER_HOST` and the default context. So an exported `DOCKER_HOST` overrides
  `docker context use`. Check `docker context show` and `env | grep DOCKER_`.
- The context user must be allowed to use the Docker socket on the remote machine. An
  `ssh://<user>@<host>` URL requires Docker 18.09 or later on the remote host (Docker CLI
  source).

Export and import a context (the default export file name is `<CONTEXT>.dockercontext`;
`-` writes to stdout):
```sh
docker context export prod-web
docker context import prod-web prod-web.dockercontext
```

## SSH tips
Docker's own guidance for the best SSH experience is to reuse one SSH connection for several
`docker` invocations in `~/.ssh/config`:
```
Host web-1.example.com
  User deploy
  ControlMaster auto
  ControlPath ~/.ssh/control-%C
  ControlPersist yes
```
Use key-based authentication so commands do not prompt.

## Compose against a remote context
```sh
docker --context prod-web compose -f compose.yaml -f compose.prod.yaml up -d
```
- Bind mounts are created on the Docker daemon host, not the client; with a remote daemon
  you cannot bind mount a local path, so use named volumes, configs or images that contain
  the files.
- Docker's production guide says that once the connection to the remote host is set up, the
  normal `docker compose` commands work with no further configuration.

## buildx with remote contexts
```sh
docker buildx create --name remote-builder prod-web     # builder pointing at the context
docker buildx build --builder remote-builder -t reg/app:1 --push .
```
`docker buildx create [CONTEXT|ENDPOINT]` makes a builder that points to a Docker context
(or endpoint), where the context is a name from `docker context ls`. Pass `--driver` (`docker-container`,
`kubernetes`, `remote`, `cloud`) to pick the driver explicitly.

## Gotchas
- A context exists only where it was created or imported, so CI needs it created in the job
  (or `DOCKER_HOST=ssh://...`).
- `docker context use` changes the default for every terminal that shares the config; use
  `--context` in scripts.

## Verify
`docker --context prod-web info` prints the remote engine's details; `docker context ls`
shows the active context with an asterisk.

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main) and docker/cli
`docs/reference` and source, buildx `docs/reference` (all main, 2026-10-23).
Method: documentation only; no commands were run.
Confirmed: `context create --docker host=...` and `--description`, `context use` semantics and
the `~/.docker/config.json` update, `context export` default file name and stdout form,
`--context` and `DOCKER_CONTEXT` precedence over `DOCKER_HOST` (CLI reference), the SSH
ControlMaster snippet (protect-access page), the Docker 18.09 remote requirement (CLI source
`connhelper.go`), bind mounts on the daemon host (bind mounts page), and `buildx create
[CONTEXT|ENDPOINT]` and its driver list. Corrected: the earlier precedence order, which put
`DOCKER_HOST` above `DOCKER_CONTEXT`. Removed: the secrets-in-exports remark, the
`docker system dial-stdio` explanation, connection-time figures, and the claim that the
default buildx driver on a remote engine is `docker-container`.
