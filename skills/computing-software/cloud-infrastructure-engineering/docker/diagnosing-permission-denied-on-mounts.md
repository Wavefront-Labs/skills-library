---
id: computing-software.cloud-infrastructure-engineering.docker.diagnosing-permission-denied-on-mounts
name: diagnosing-permission-denied-on-mounts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, mount-permissions, permission-denied, noexec, selinux-z, uid-mapping, apparmor]
level: practitioner
status: docs-checked
description: "Find the real cause of Permission denied on bind mounts and volumes: numeric UID/GID mismatch, SELinux labels, noexec, read-only mounts, rootless/userns mapping, AppArmor, CRLF."
sources: ["https://docs.docker.com/engine/storage/bind-mounts/", "https://docs.docker.com/engine/security/userns-remap/", "https://docs.docker.com/engine/security/rootless/troubleshoot/","https://docs.docker.com/engine/security/rootless/uid-gid-mapping/", "https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing Permission denied on mounts

Same message, many causes. Check them in this order.

## 1. Numeric ownership
Names lie; compare numbers on both sides.
```bash
docker exec <c> id                               # uid=1000(app) gid=1000(app)
docker exec <c> ls -ln /data                      # owner uid/gid as seen inside
ls -ln /srv/data                                  # owner as seen on the host
```
Container UID must own the files or match group/other permissions. Fix with matching UIDs,
`chown` on the host to the container UID, group permissions, or `--user`.

## 2. Read-only mount
```bash
docker inspect -f '{{range .Mounts}}{{.Destination}} rw={{.RW}}{{println}}{{end}}' <c>
```
`EROFS: read-only file system` vs `EACCES` tells them apart; `--read-only` rootfs also counts.

## 3. SELinux (Fedora, RHEL, CentOS)
```bash
getenforce
ls -Zd /srv/data
```
Fix: `-v /srv/data:/data:Z` (private, unshared) or `:z` (shared). Docker warns that relabelling
system directories such as `/home` or `/usr` with `Z` can render the host unusable.

## 4. Executing a script
`Permission denied` when **executing** a script on the mount: check the executable bit
(`docker exec <c> ls -l /scripts/run.sh`) and whether the mount or filesystem is `noexec`.
Call the script via the interpreter (`sh /scripts/run.sh`) or fix the mode.

Windows `\r\n` line endings make scripts fail with syntax errors in the container (Docker
Desktop troubleshooting page); convert with `dos2unix`.

## 5. User namespaces and rootless
```bash
docker info -f '{{.SecurityOptions}}'             # name=rootless or name=userns
cat /etc/subuid
```
Docker's UID/GID mapping page: with `userns-remap`, container UID 0 maps to the first
subordinate UID in `/etc/subuid` and UID `n` to `subuid + n`. In rootless mode, container
UID 0 maps to your host UID and UID `n` (n >= 1) to `subuid + (n - 1)`; GIDs use
`/etc/subgid`. So in rootless mode files you own appear as `root` inside the container.

## 6. Docker Desktop
The project directory must be in the file-sharing list if it is outside your home directory.
On Windows, shared volumes get a non-configurable default mode of `0777`; use a named volume
when an application needs different permissions.

## Checked
Date: 2026-10-26. Documentation: docker/docs main (last commit 2026-10-23): bind mounts (SELinux labels), rootless UID/GID mapping, Desktop troubleshooting topics. Confirmed: `z`/`Z` semantics and the system-directory warning, userns-remap and rootless mapping formulas, Windows 0777 default, file-sharing requirement, CRLF failure. Removed as unconfirmed: ausearch and dmesg commands, `chcon` label name, `findmnt noexec` check, `.gitattributes` advice, AppArmor and CAP_DAC_OVERRIDE section, rootlesskit/podman remedies, Postgres-specific claim, `ls -Zd` label comments.
Method: documentation only; no commands were run.
