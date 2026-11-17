---
id: computing-software.systems-network-administration.restic.docker-image-niceness
name: docker-image-niceness
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, docker, container, hostname, nice, ionice]
level: practitioner
status: docs-checked
description: "Run restic from the official Docker images with a fixed hostname and NICE, IONICE_CLASS and IONICE_PRIORITY environment variables."
sources:
  - https://restic.readthedocs.io/en/stable/020_installation.html
  - https://restic.readthedocs.io/en/stable/040_backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run restic in a container

Two official images exist:

```
docker pull restic/restic
docker pull ghcr.io/restic/restic
```

## Set a static hostname

Restic relies on the hostname for various operations, and by default `backup` selects its parent snapshot by grouping on host and paths (`--group-by host,paths`). Docker assigns a random hostname each time unless you set one, so a new container looks like a new host. Always pass `--hostname`:

```
docker run --hostname myhost ghcr.io/restic/restic ...
```

## Lower the impact

The image reads these environment variables:

- `NICE`: adjustment passed to `nice -n` (default none)
- `IONICE_CLASS`: class passed to `ionice -c`
- `IONICE_PRIORITY`: priority for `ionice` (default 4)

Example from the docs:

```
docker run -e NICE=20 -e IONICE_CLASS=2 -e IONICE_PRIORITY=7 ghcr.io/restic/restic
```

The real-time IO class needs the `SYS_NICE` capability (`--cap-add SYS_NICE`).

This tells the CPU and IO schedulers to deprioritize restic, which typically means a longer runtime, drastically longer on a heavily loaded system.

## Checked

Checked 2026-11-08 against the restic Installation page (020_installation) and Backing up page (040_backup), both read in full. Confirmed: the restic/restic and ghcr.io/restic/restic images, the static --hostname advice, NICE, IONICE_CLASS and IONICE_PRIORITY with their defaults, the SYS_NICE capability for the real-time class, the example command, and the default parent selection by host and paths. Removed: the repository and password handling advice, which the page does not state.

Method: documentation only; no commands were run.
