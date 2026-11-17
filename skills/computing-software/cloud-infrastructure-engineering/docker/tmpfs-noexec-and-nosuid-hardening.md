---
id: computing-software.cloud-infrastructure-engineering.docker.tmpfs-noexec-and-nosuid-hardening
name: tmpfs-noexec-and-nosuid-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, read-only-rootfs, tmpfs-noexec, tmpfs-options, nosuid, tmpfs-size, hardening]
level: advanced
status: docs-checked
description: "Harden writable tmpfs mounts: Docker's --tmpfs defaults (noexec, nosuid, nodev), size and mode limits, when apps need exec (JNI, ctypes) and how --mount type=tmpfs differs."
sources: ["https://docs.docker.com/engine/storage/tmpfs/", "https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/reference/compose-file/services/", "https://github.com/moby/moby/blob/master/daemon/oci_linux.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tmpfs noexec and nosuid hardening

A read-only rootfs with an executable `/tmp` still lets an attacker drop and run a binary.
`noexec` closes that; `nosuid` and `nodev` stop setuid binaries and device files.

## --tmpfs flag
```bash
docker run --read-only --tmpfs /tmp app                         # daemon adds noexec,nosuid,nodev as base options
docker run --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m,mode=1777 app   # explicit options, capped size
docker run --read-only --tmpfs /tmp:exec,size=256m app          # explicitly allow exec when required
docker exec <c> grep ' /tmp ' /proc/self/mounts                 # shows the options actually applied
```
In the daemon source (`daemon/oci_linux.go`) tmpfs mounts start from `noexec`, `nosuid`, `nodev` and your
options are merged over them, so `exec` re-enables execution. The Docker tmpfs page lists `suid` as the
generic default and does not state the daemon's base options, so confirm the applied options in the
mount table as above. `--tmpfs` options include `ro`/`rw`, `nosuid`/`suid`, `nodev`/`dev`,
`exec`/`noexec`, `size`, `mode`, `uid`, `gid`, `nr_inodes` and `nr_blocks`; `--tmpfs` cannot be used
with Swarm services (use `--mount`).

## --mount type=tmpfs
```bash
docker run --mount type=tmpfs,dst=/tmp,tmpfs-size=67108864,tmpfs-mode=1777 app
```
`--mount type=tmpfs` supports `tmpfs-size` (bytes; if unset the maximum is 50% of the host's RAM) and
`tmpfs-mode` (octal, default `1777`). The Docker tmpfs page lists no exec/suid flags for `--mount`, so use
`--tmpfs` when you need to set mount flags explicitly.

Compose: the `tmpfs` service attribute takes `<path>` or `<path>:<options>`; the Compose reference lists
the options `mode`, `uid` and `gid`:
```yaml
services:
  app:
    tmpfs:
      - /tmp:mode=1777
```

## Apps that break with noexec
Programs that extract native libraries or scripts into `/tmp` and execute them from there fail when the
mount is `noexec`. Either ship those files in the image, or give the program its own tmpfs path mounted with
`exec` (for example `--tmpfs /app/jtmp:exec,size=64m`) and point its temp-directory setting there.
Keep exec scoped to a dedicated directory rather than `/tmp` as a whole.

## Sizing
tmpfs data counts toward the container's memory cgroup limit (a large `size` does not raise it), so an
unbounded tmpfs filled by logs or uploads can cause OOM kills. Always set `size` on writable tmpfs mounts.
tmpfs data may be written to swap, so it can still reach disk.

## Verify
```bash
docker exec <c> sh -c 'cp /bin/true /tmp/t && /tmp/t'   # fails with a permission error when noexec applies
docker exec <c> grep ' /tmp ' /proc/self/mounts           # options and size= of the tmpfs
```

## Checked
Date: 2026-10-24. Documentation: Docker docs tmpfs mounts page, `docker run` reference and Compose services reference (docker/docs main); moby/moby `daemon/oci_linux.go` (master).
- Confirmed `--tmpfs` option list and example (`size=`, `mode=`, `exec`, `noexec`, `nosuid`, `nodev`), the `--mount type=tmpfs` keys `tmpfs-size` (default max 50% of host RAM) and `tmpfs-mode` (default 1777), `--tmpfs` not usable with Swarm services, tmpfs counting toward the memory limit and possibly reaching swap, and the Compose `tmpfs` attribute options (`mode`, `uid`, `gid`).
- Confirmed in the daemon source that tmpfs mounts start from `noexec`, `nosuid`, `nodev` with user options merged over them; the tmpfs docs page lists `suid` as default, so the skill tells readers to read the applied options.
- Removed the `tmpfs-options` claim, Compose long-syntax tmpfs, the error-message table for JNI/ctypes, the exit-code claim and `findmnt`.
Method: documentation only; no commands were run.
