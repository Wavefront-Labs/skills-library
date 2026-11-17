---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-container-users-and-namespaces
name: quadlet-container-users-and-namespaces
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, user, group, usernamespace, keep-id, uidmap, gidmap, groupadd]
level: advanced
status: docs-checked
description: "Set users and namespaces for Quadlet containers: User and Group mapping to --user, UserNS keep-id, UIDMap, GIDMap, SubUIDMap, GroupAdd and Umask."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the identity a container process runs as.

From the page's table: `User=bin` is `--user bin`; `Group=1234` is `--user UID:1234`; `GroupAdd=keep-groups` is `--group-add=keep-groups`; `UserNS=keep-id:uid=200,gid=210` is `--userns keep-id:uid=200,gid=210`, with `UserNS` generally of the form `MODE[:OPTIONS,...]`; `UIDMap=0:10000:10` and `GIDMap=0:10000:10` map to `--uidmap` and `--gidmap`; `SubUIDMap=utest` and `SubGIDMap=gtest` map to `--subuidname` and `--subgidname`; `Umask=0077` is `--umask 0077`.

Do not confuse these with the systemd `User=`, `Group=` and `DynamicUser=` options in `[Service]`: Quadlet does not support running a unit as a non-root user that way. To run rootless, create the user and put the unit file in a rootless search path.

Other process-level keys: `Ulimit=nofile=1000:10000`, `PidsLimit=10000`, `Memory=20g`, `Sysctl=name=value`, `Timezone=local` (uses the system default if unset).


Key semantics: `UserNS=` is equivalent to `--userns` with a mode such as `keep-id` followed by options; `Group=1234` is passed as the group part of `--user UID:1234`, while `User=bin` is `--user bin`; `GroupAdd=keep-groups` is `--group-add=keep-groups`. Resource keys in the same table include `Ulimit=nofile=1000:10000`, `PidsLimit=10000` and `Memory=20g`. `Timezone=local` uses the host time zone; when unset, the system-configured default applies.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
