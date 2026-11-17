---
id: computing-software.cloud-infrastructure-engineering.docker.default-capabilities-cap-drop-all-and-setcap
name: default-capabilities-cap-drop-all-and-setcap
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, capabilities, cap-drop, cap-add, least-privilege, default-capabilities, bounding-set, cap-drop-all, setcap, file-capabilities]
level: advanced
description: "Know Docker's default capability set, run with --cap-drop ALL plus only what's needed, find which capability a failure needs, and use setcap file capabilities in images."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/engine/security/", "https://man7.org/linux/man-pages/man7/capabilities.7.html", "https://man7.org/linux/man-pages/man8/setcap.8.html"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Default capabilities, cap-drop ALL and file capabilities

## Docker's default set (14)
`CHOWN, DAC_OVERRIDE, FOWNER, FSETID, KILL, SETGID, SETUID, SETPCAP, NET_BIND_SERVICE,
NET_RAW, SYS_CHROOT, MKNOD, AUDIT_WRITE, SETFCAP`. Everything else (SYS_ADMIN, NET_ADMIN,
SYS_PTRACE, SYS_TIME, SYS_MODULE...) is dropped. These form the container's **bounding set**:
no process inside can ever gain more, even via setuid binaries.
```sh
docker run --rm alpine grep Cap /proc/1/status    # CapBnd is the bounding set; decode with: capsh --decode=<hex>
```

## Drop all, add back
```sh
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE --user 10001 nginx-unprivileged
```
```yaml
services:
  api:
    cap_drop: [ALL]
    cap_add: [NET_BIND_SERVICE]
```
Typical needs:
| App does | Needs |
|---|---|
| bind < 1024 | NET_BIND_SERVICE (or listen high) |
| `chown` files at start (entrypoint as root) | CHOWN, and DAC_OVERRIDE/FOWNER for others' files |
| drop to another user (gosu/su-exec) | SETUID, SETGID |
| `ping` (raw sockets) | NET_RAW |
| change network interfaces | NET_ADMIN |
| strace/gdb | SYS_PTRACE |
A non-root app that just serves HTTP on 8080 needs **none**.

## Finding the missing capability
- Errors: `EPERM`/`Operation not permitted` right after a change of cap set.
- Iterate: start from `--cap-drop ALL` and add one capability at a time until the failure stops.
- Dropping NET_RAW removes raw and packet sockets, so `ping` stops working.

## File capabilities in images
```dockerfile
RUN setcap cap_net_bind_service=ep /usr/local/bin/server
USER 10001
```
- The file's permitted capabilities are intersected with the container's bounding set; if the effective
  bit is set and the process cannot obtain the full permitted set, `execve` fails with `EPERM`
  (so `--cap-drop ALL` without `--cap-add NET_BIND_SERVICE` breaks this binary).
- File capabilities are stored in the `security.capability` extended attribute and writing it needs
  CAP_SETFCAP, which is in Docker's default set. `setcap` is provided by libcap (install it in the
  build stage); setcap(8) takes `capabilities|-|-r` and a file name.
- Check the result with `getcap` (see setcap(8) SEE ALSO).

## Verify
`docker inspect -f '{{.HostConfig.CapDrop}} {{.HostConfig.CapAdd}}' api`; inside,
`grep CapEff /proc/1/status` decodes to only the added caps.

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main: `docker run` reference, security overview, Rootless tips), man-pages capabilities(7) and setcap(8).
- Confirmed the default set is the 14 capabilities listed in the `docker run` reference and that Docker documents `--cap-drop`/`--cap-add`, and the `setcap cap_net_bind_service=ep` form (Rootless tips page).
- Confirmed bounding-set intersection, `security.capability` xattr, CAP_SETFCAP requirement and `EPERM` on execve in capabilities(7); `setcap` synopsis in setcap(8).
- Removed bcc `capable`, `ping_group_range` for rootful, ARP-spoofing and BuildKit xattr claims, and pinned package installs, none of which a checked source covers.
Method: documentation only; no commands were run.
