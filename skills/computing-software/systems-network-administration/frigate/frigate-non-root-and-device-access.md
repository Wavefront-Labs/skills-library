---
id: computing-software.systems-network-administration.frigate.frigate-non-root-and-device-access
name: frigate-non-root-and-device-access
category: computing-software
field: systems-network-administration
product: frigate
tags: [non-root-user, puid-pgid, extra-groups, device-acl-paths, read-only-rootfs, frigate-root-services]
level: advanced
status: docs-checked
description: "Understand Frigate's unprivileged runtime user, choose between PUID/PGID, Docker user and root modes, and grant hardware device access with EXTRA_GROUPS."
sources: ["https://github.com/blakeblackshear/frigate/blob/dev/docs/docs/configuration/non_root.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running Frigate as a non-root user

Frigate's main process and nginx run as the `frigate` user and go2rtc as a more restricted `go2rtc` user; only the s6 init system and the certsync helper stay root. The default runtime uid/gid is `1000:1000`. This page exists in the project's development docs; it was not on the published docs site when reviewed, so it may describe a newer release than yours. Most upgrades need nothing, since Frigate aligns ownership of `/config` and `/media/frigate` on first boot.

Run modes:
- Default: ownership aligned to `1000:1000`; `read_only: true` supported.
- `PUID` and `PGID` environment variables: ownership aligned to your values on first boot; read-only root not supported because `usermod` writes `/etc/passwd`.
- Docker `user: "1001:1001"`: you own the ownership and Frigate never changes it; read-only supported.
- `FRIGATE_RUN_AS_ROOT=true`: root escape hatch; matched against the exact lowercase string `true` only.
- `FRIGATE_ROOT_SERVICES` with a comma list of `frigate`, `go2rtc`, `nginx`: those services stay root while the rest remain unprivileged, useful if detector hardware will not work unprivileged or you want root but files owned by `PUID` and `PGID`.

Hardware access: pass devices with `--device` or `devices:` and Frigate adds ACL entries for the runtime user at startup (GPU render nodes, NPUs in `/dev/accel`, Coral, Hailo, Rockchip, Jetson, `/dev/video*`, USB). Add globs with `DEVICE_ACL_PATHS`, for example `"/dev/mydev*"`, or set `FRIGATE_DEVICE_ACLS=false` (exact lowercase) to manage permissions yourself.

Manual setup, needed for hardware the grant misses or for Docker `user:` mode: inspect the node with `ls -ln /dev/dri/renderD128`, work out which permission set applies to the runtime user (not the owner; group only if it belongs to that GID), then add numeric host GIDs with `EXTRA_GROUPS: "105,44"`; it applies to both the frigate and go2rtc users. A USB Coral commonly has group 0 and read-only "other", so the runtime user cannot write and Frigate reports `No EdgeTPU was detected`. Docker's `group_add` has no effect in default or `PUID` modes, and `privileged: true` does not help the unprivileged user.

## Checked

2026-11-04. Confirmed against the non_root page in the Frigate development docs (the published docs URL returned 404, so the source now points at the docs file on GitHub): runtime users, default 1000:1000, PUID/PGID and usermod, read-only root limits, Docker user mode, FRIGATE_RUN_AS_ROOT and FRIGATE_DEVICE_ACLS exact-string matching, FRIGATE_ROOT_SERVICES, DEVICE_ACL_PATHS, EXTRA_GROUPS applying to both users, group_add and privileged behaviour, and the Coral 'No EdgeTPU was detected' example. Added a note that the page is dev-only.
Method: documentation only; no commands were run.
