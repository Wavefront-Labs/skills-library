---
id: computing-software.cloud-infrastructure-engineering.docker.rootless-docker-host-and-context-setup
name: rootless-docker-host-and-context-setup
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, rootless, rootless-docker-host, docker-context, docker-host-env, xdg-runtime-dir, rootless-mode]
level: practitioner
status: docs-checked
description: "Point the CLI, Compose and tools at a rootless daemon: per-user socket path, the rootless context, DOCKER_HOST for tools ignoring contexts, running both daemons."
sources: ["https://docs.docker.com/engine/security/rootless/tips/", "https://docs.docker.com/engine/security/rootless/troubleshoot/", "https://docs.docker.com/engine/manage-resources/contexts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rootless Docker: DOCKER_HOST and contexts

The rootless daemon listens on a per-user socket:
`unix://$XDG_RUNTIME_DIR/docker.sock` (usually `/run/user/<uid>/docker.sock`).

## Pick the daemon
```bash
# The setup tool creates a "rootless" context
docker context ls
docker context use rootless
# Or explicitly
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
docker info -f '{{.SecurityOptions}}'      # contains name=rootless
```
`DOCKER_HOST` overrides the current context (as do `DOCKER_CONTEXT` and the `--context`/`--host` flags).
Tools that do not read Docker contexts need `DOCKER_HOST`; set it in the shell profile for those.

## Persisting the environment
```bash
cat >> ~/.bashrc <<'EOF'
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
EOF
```
`XDG_RUNTIME_DIR` is set to `/run/user/$UID` when you log in through `pam_systemd`. Switching with
`sudo -iu` loses it (`systemctl --user` then fails with "Failed to connect to bus"; rootlesskit reports
"could not get XDG_RUNTIME_DIR"). Log in with `ssh user@localhost` or `machinectl shell user@`, and
enable lingering (`sudo loginctl enable-linger user`) so the daemon starts without a session.

## Rootful and rootless side by side
- Rootful socket `/var/run/docker.sock` (the `default` context), rootless socket under `/run/user/<uid>`;
  the rootless data dir is `~/.local/share/docker`, separate from the rootful one.
- Switch per command: `docker --context default ps` vs `docker --context rootless ps`.

## Compose, buildx, SDKs
- For tools that talk to the socket directly (SDKs, test frameworks), set `DOCKER_HOST` to the rootless
  socket path and check that tool's own documentation for socket-mount settings.

## Verify
```bash
docker context inspect rootless -f '{{.Endpoints.docker.Host}}'
systemctl --user status docker
ls -l $XDG_RUNTIME_DIR/docker.sock
```

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main) Rootless Tips and Troubleshooting pages and the Docker contexts page.
- Confirmed the socket path `$XDG_RUNTIME_DIR/docker.sock` (`/run/user/$UID`), the automatic `rootless` context, `DOCKER_HOST`/`DOCKER_CONTEXT`/`--context` overriding the current context, the `default` context at `/var/run/docker.sock`, `pam_systemd`, `machinectl shell`, `loginctl enable-linger` and the data directory.
- Confirmed the `docker context inspect` output carries `Endpoints` (Docker context page).
- Removed Testcontainers, Python SDK, Compose/buildx and Ansible claims that this lane could not confirm from primary documentation.
Method: documentation only; no commands were run.
