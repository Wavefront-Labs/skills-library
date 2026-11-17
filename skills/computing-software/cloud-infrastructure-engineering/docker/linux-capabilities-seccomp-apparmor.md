---
id: computing-software.cloud-infrastructure-engineering.docker.linux-capabilities-seccomp-apparmor
name: linux-capabilities-seccomp-apparmor
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, linux-capabilities, cap-drop, cap-add, cap_net_bind_service, cap_sys_admin, seccomp, seccomp-profile, default-seccomp-profile, apparmor, apparmor-profile, docker-default-profile, privileged-container, no-new-privileges, readonly-rootfs, security-opt]
level: advanced
status: docs-checked
description: "Shrinking a container's blast radius below root-in-container: dropping Linux capabilities, custom seccomp syscall filters, AppArmor profiles, and why --privileged defeats all three."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/engine/security/seccomp/", "https://docs.docker.com/engine/security/apparmor/", "https://man7.org/linux/man-pages/man7/capabilities.7.html", "https://github.com/moby/profiles/blob/main/seccomp/default.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux capabilities, seccomp, and AppArmor for containers

**Goal:** a container running as root (the common case, before you've even gotten to
`rootless-containers` or `userns-remap`) is still not equivalent to real host root, *unless*
someone granted it `--privileged` or extra capabilities. This skill is what actually
enforces that gap, and how to tighten it further than the defaults.

## Linux capabilities — root is not one thing
Traditional Unix root is really many independent privilege bits (`CAP_NET_ADMIN`,
`CAP_SYS_ADMIN`, `CAP_SYS_PTRACE`, `CAP_NET_BIND_SERVICE`, …). Docker's default container
already drops most of them — not full root — keeping only a curated subset (`CAP_CHOWN`,
`CAP_SETUID`, `CAP_NET_BIND_SERVICE`, etc.; the Docker `docker run` reference lists the
current default set). Two directions to move
from there:
```
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp   # start from nothing, add back only what's needed
docker run --cap-add=SYS_PTRACE myapp                        # add one specific capability on top of defaults
```
`--cap-drop=ALL` then adding back only what the app actually needs (verify with `strace` or
by testing what breaks) is the correct default posture for anything internet-facing. A
container that just needs to bind port 80/443 as non-root only needs
`CAP_NET_BIND_SERVICE` — not full root, not `--privileged`.
- `CAP_SYS_ADMIN` is informally "the new root" — it alone enables mounting filesystems,
  among many other things; treat any request to add it as a design smell worth questioning.
- Check what a container actually holds: `docker exec <id> capsh --print` (if `capsh`
  available) or `cat /proc/<pid>/status | grep Cap` and decode with `capsh --decode=<hex>`.

## `--privileged` defeats everything in this skill
`--privileged` grants **all** capabilities, disables the seccomp and AppArmor profiles
below, and gives access to host devices — it is not "more capabilities," it's "capabilities
and syscall filtering and MAC enforcement off." Needed genuinely rarely (some
Docker-in-Docker setups, certain hardware access); almost every "I need `--privileged` to
make X work" is actually a missing single capability or device mount
(`--device=/dev/foo`) once you track it down.

## seccomp — filtering syscalls, not just capabilities
Capabilities gate *what a privileged operation can do*; seccomp gates *which syscalls can
be made at all*, privileged or not. Docker's default seccomp profile
(`default.json` in moby/moby) blocks around 44 of 300+ syscalls (for example `keyctl`, `add_key`, kernel module
syscalls, and `clone` for new namespaces unless CAP_SYS_ADMIN is held; see the table on the Docker
seccomp page). `docker run --security-opt seccomp=unconfined` disables it (debugging
only - never in production, it widens the attack surface). Writing a custom tighter profile: copy
`default.json`, remove syscalls the app doesn't need, test with
`docker run --security-opt seccomp=custom.json` and watch for `EPERM` in app logs or
`dmesg`/`audit.log` for the specific blocked syscall and PID.

## AppArmor — path/resource-level mandatory access control
Where capabilities and seccomp are about *verbs* (operations, syscalls), AppArmor is about
*objects* — which files, network operations and capabilities a confined process may touch,
by profile. Docker auto-generates and loads a `docker-default` AppArmor profile on
AppArmor-enabled hosts; on SELinux hosts the equivalent is SELinux labels. Check which applies
with `docker info`: its Security Options list shows `name=apparmor` or `name=selinux`. Custom profiles: write one, `apparmor_parser -r
/etc/apparmor.d/my-profile`, then `docker run --security-opt apparmor=my-profile`.
SELinux-equivalent: `--security-opt label=type:my_container_t`.

## Pairing with a read-only root filesystem
`--read-only` plus `--tmpfs /tmp --tmpfs /run` (for the directories that genuinely need
write access) removes an entire class of "attacker writes a file to the container
filesystem" attacks regardless of capabilities — cheap to add, worth doing by default for
anything that doesn't need to write to its own image layer at runtime.

## Verify
`docker inspect <id> --format '{{.HostConfig.CapAdd}} {{.HostConfig.CapDrop}}'` matches
intent; `docker exec <id> capsh --print` (or `/proc/<pid>/status` Cap lines) shows only the
intended bits set; a deliberately blocked syscall (e.g. `mount` inside a default-seccomp
container) returns `EPERM`, confirming the filter is actually loaded, not just configured.

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main: `docker run` reference, seccomp, AppArmor pages), man-pages capabilities(7), moby/profiles default.json, Docker Engine API (SecurityOptions).
- Confirmed `--cap-drop`/`--cap-add`, `--privileged` giving all capabilities and reconfiguring AppArmor or SELinux, `--security-opt seccomp=unconfined`, `--security-opt apparmor=<name>`, `apparmor_parser -r -W`, `docker-default` generated by the Docker binary, `label=type:` options, and `--read-only`.
- Confirmed the "around 44 of 300+" default seccomp figure and that the Rootless docs say `--privileged` is needed to disable seccomp, AppArmor and mount masks.
- Confirmed `docker info` Security Options entries (`name=apparmor`, `name=selinux`) in the Engine API description.
- Removed the "~40 capabilities" count and the RHEL default-MAC claim.
Method: documentation only; no commands were run.
