---
id: computing-software.cloud-infrastructure-engineering.docker.checkpoint-restore-with-criu
name: checkpoint-restore-with-criu
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, criu, checkpoint-restore, docker-checkpoint, experimental-feature, live-migration, fast-restart, process-dump, podman-checkpoint, containerd-criu]
level: sme
status: docs-checked
description: "docker checkpoint/restore via CRIU: dumping a running container's full process state to disk and resuming it, what actually works today, and why it's not production-ready for most stacks."
sources: ["https://docs.docker.com/reference/cli/docker/checkpoint/", "https://docs.docker.com/reference/cli/docker/checkpoint/create/", "https://docs.docker.com/reference/cli/dockerd/", "https://criu.org/Installation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checkpoint/restore with CRIU (experimental, know its limits)

**Goal:** understand what `docker checkpoint` promises: freezing a running
container's state to files on disk and restoring it later. Docker documents it as an experimental feature focused on single-host use cases, so do not build production reliability on it without testing your exact Docker and CRIU versions.

## What it actually does
Docker uses the external tool CRIU (Checkpoint/Restore In Userspace; version 2.0 or newer) to turn container state into a collection of files on disk. `docker checkpoint create [--leave-running] [--checkpoint-dir DIR] <container> <name>` creates a checkpoint, `docker checkpoint ls` lists them, `docker checkpoint rm` deletes one, and `docker start --checkpoint <name> <container>` (with `--checkpoint-dir` if you used one) restores it.

## Enabling it
Requires `dockerd --experimental` (or `"experimental": true` in `daemon.json`) and CRIU installed on the host. Docker's page points to the CRIU Launchpad PPA for Debian systems or building from source (https://criu.org/Installation). The checkpoint commands are marked experimental in the CLI reference. Docker's own example starts the test container with `--security-opt=seccomp:unconfined`.

## Legitimate use cases, when it works
Docker's documented single-host use cases:
- Restarting the host machine without stopping and starting containers.
- Speeding up the start of slow-starting applications.
- "Rewinding" processes to an earlier point in time.
- Forensic debugging of running processes.

Live migration to another machine is described as possible with the current implementation but not a priority, so the workflow is not optimised for it.

## Limits
- The feature is experimental and depends on an external tool (CRIU), so treat it as a risk to evaluate rather than a guarantee.
- Docker's documentation does not list which kernel resources CRIU can or cannot restore; test your own workload (network connections, devices, mounts) on a single host before depending on it.
- Check the CRIU documentation (https://criu.org) for kernel and version requirements when moving a checkpoint between hosts.
- Other runtimes such as Podman have their own checkpoint commands; use their documentation rather than assuming Docker CLI parity.

## Verify
On a single host, checkpoint a trivial long-running container (Docker's example prints an incrementing counter in a shell loop), restore it with `docker start --checkpoint`, and confirm the counter continues from where it was dumped instead of restarting from zero.

## Checked

Checked against the `docker checkpoint` and `docker checkpoint create` references and `docker container start --checkpoint` in docker/docs (`data/cli/engine`), and the dockerd reference for `--experimental` (docker/docs latest commit 2026-10-23, Engine 29).

- Experimental status, CRIU 2.0 minimum, `create`/`ls`/`rm` subcommands, `--leave-running`, `--checkpoint-dir`, `docker start --checkpoint`, documented use cases (single-host focus, live migration possible but not a priority), `--experimental` and `"experimental": true`.
- Removed as unconfirmed: the checkpoint storage path, `apt install criu`, kernel option notes, the TCP, NFS, GPU and kernel-matching limitation claims, Podman and Kubernetes comparisons and the `docker version` grep.

Method: documentation only; no commands were run.
