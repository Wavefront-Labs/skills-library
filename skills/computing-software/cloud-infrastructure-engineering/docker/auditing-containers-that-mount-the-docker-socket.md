---
id: computing-software.cloud-infrastructure-engineering.docker.auditing-containers-that-mount-the-docker-socket
name: auditing-containers-that-mount-the-docker-socket
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-socket, socket-mount-audit, docker-inspect, compose-file, falco, security-audit]
level: practitioner
status: docs-checked
description: "Find containers and Compose/stack files exposing the Docker API: socket bind mounts, /var/run mounts, DOCKER_HOST tcp endpoints; then gate them in CI and at runtime."
sources: ["https://docs.docker.com/reference/cli/docker/container/inspect/", "https://docs.docker.com/engine/cli/formatting/", "https://github.com/moby/moby/blob/master/api/swagger.yaml", "https://docs.docker.com/reference/compose-file/services/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing containers that mount the Docker socket

## Running containers
```bash
docker ps -aq | xargs docker inspect -f \
  '{{.Name}}{{range .Mounts}}{{if or (eq .Source "/var/run/docker.sock") (eq .Source "/run/docker.sock") (eq .Source "/var/run") (eq .Source "/run")}} MOUNTS {{.Source}} -> {{.Destination}} rw={{.RW}}{{end}}{{end}}' \
  | grep MOUNTS
```
Also look for:
```bash
# API over TCP passed via env
docker ps -aq | xargs docker inspect -f '{{.Name}} {{range .Config.Env}}{{if (index (split . "=") 0 | eq "DOCKER_HOST")}}{{.}}{{end}}{{end}}' | grep DOCKER_HOST
# containerd / podman sockets
docker ps -aq | xargs docker inspect -f '{{.Name}} {{range .Mounts}}{{.Source}} {{end}}' | grep -E 'containerd.sock|podman.sock'
```
Mounting the whole `/var/run` or `/run` directory exposes the socket too.

## Files in repositories
```bash
grep -rnE 'docker\.sock|/var/run:|/run:' --include='*compose*.y*ml' --include='*stack*.y*ml' .
grep -rnE 'docker\.sock' --include='*.y*ml' k8s/ charts/       # hostPath mounts in manifests
```
CI gate: a simple grep step with an allowlist file, or a policy check on the Compose file, that fails
when a service mounts the socket.

## Runtime detection
Re-run the `docker inspect` mount check above on a schedule, and use a Docker authorization plugin
(see `docker-authorization-plugins-with-opa`) to deny container creation requests whose bind mounts
include the socket.

## For each finding decide
1. Remove: does the tool have a non-socket mode?
2. Restrict: socket proxy with only the needed endpoints.
3. Accept: document owner, reason and review date; the container is effectively root on the
   host, so harden it (pinned digest, minimal image, no exposed ports).

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main) formatting page (Go template functions `split`, `join`, `json`), Docker Engine API (container inspect `Mounts` with `Source`, `Destination`, `RW`; `Config.Env`).
- Confirmed the `docker inspect --format` Go template functions used (`split`, `join`, `json`) and the `.Mounts[].Source/Destination/RW`, `.Name` and `.Config.Env` fields in the API schema.
- Removed the trivy, conftest and Falco rule claims (rule syntax and tool behaviour not confirmed from primary documentation).
Method: documentation only; no commands were run.
