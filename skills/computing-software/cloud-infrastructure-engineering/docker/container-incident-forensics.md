---
id: computing-software.cloud-infrastructure-engineering.docker.container-incident-forensics
name: container-incident-forensics
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, runtime-security, container-forensics, incident-response, docker-diff, docker-export, checkpoint]
level: sme
status: docs-checked
description: "Handle a compromised container without destroying evidence: isolate networks, pause, capture inspect, logs, diff and filesystem export, then contain and rebuild."
sources: ["https://docs.docker.com/reference/cli/docker/container/pause/", "https://docs.docker.com/reference/cli/docker/container/diff/", "https://docs.docker.com/reference/cli/docker/container/export/", "https://docs.docker.com/reference/cli/docker/container/top/", "https://docs.docker.com/reference/cli/docker/container/logs/", "https://docs.docker.com/reference/cli/docker/network/disconnect/", "https://docs.docker.com/reference/cli/docker/container/commit/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container incident forensics

Instinct says remove the container at once. That destroys its writable layer and logs. Order
of operations: isolate, freeze, collect, then contain.

## 1. Isolate without stopping
```bash
C=web-1
docker network disconnect <NETWORK> "$C"        # repeat per attached network
```
`docker network disconnect NETWORK CONTAINER` requires the container to be running. Disconnecting
cuts command-and-control and lateral movement; published ports stop working for that network.

## 2. Capture volatile state first
```bash
docker top "$C" -eo pid,ppid,user,args > ps.txt   # docker top accepts ps options
```

## 3. Freeze and collect
```bash
docker pause "$C"                       # suspends all processes via the freezer cgroup on Linux
docker inspect "$C" > inspect.json
docker logs --timestamps "$C" > stdout-stderr.log 2>&1
docker diff "$C" > diff.txt             # A = added, C = changed, D = deleted
docker export --output rootfs.tar "$C"  # container filesystem as a tar archive
```
The freezer cgroup means the processes cannot observe that they are paused (unlike SIGSTOP).
`docker export` does not include volume contents (if a volume is mounted over an existing
directory, it exports the underlying directory, not the volume), so copy volumes separately.
Store the output in an evidence directory with restricted permissions and record hashes of the files.

## 4. Contain and recover
- Keep the paused container, or `docker commit` it to an evidence image, until analysis is done;
  then remove it.
- Rotate every secret the container had access to.
- Rebuild from a known-good image digest and find the entry point (vulnerable package, exposed
  admin port, socket mount).

## Analysis starting points
`diff.txt` additions in temporary directories and web roots; unexpected binaries; scheduled jobs;
outbound connections recorded by your network or audit tooling around the start time.

## Checked
2026-11-01. Confirmed on the Docker CLI reference pages: `pause` (freezer cgroup, unobservable by the process), `diff` (A/C/D codes), `export` (volumes not exported, `--output`), `top` (ps options), `logs --timestamps`, `network disconnect` (container must be running), `commit`. Removed (not stated on those pages): the `docker checkpoint` / CRIU step and its flags, claims that export works while paused, the `nsenter`, `/proc` and `/var/lib/docker` copy steps, the firewall chain name, specific temp paths.
Method: documentation only; no commands were run.
