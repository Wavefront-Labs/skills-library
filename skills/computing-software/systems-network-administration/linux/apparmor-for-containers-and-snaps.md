---
id: computing-software.systems-network-administration.linux.apparmor-for-containers-and-snaps
name: apparmor-for-containers-and-snaps
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, apparmor-containers, docker-default, lxd-apparmor, security-opt, bane]
level: practitioner
status: docs-checked
description: "Understand and adjust AppArmor confinement for Docker, LXD and Kubernetes: docker-default profile, custom container profiles and LXD profiles."
sources:
  - https://github.com/docker/docs/blob/main/content/manuals/engine/security/apparmor.md
  - https://github.com/moby/profiles/blob/main/apparmor/template.go
  - https://github.com/kubernetes/website/blob/main/content/en/docs/tutorials/security/apparmor.md
  - https://github.com/canonical/lxd/blob/main/lxd/metadata/configuration.json
  - https://github.com/canonical/lxd/blob/main/lxd/apparmor/instance.go
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AppArmor for containers and snaps

## Docker
On AppArmor hosts a Docker container runs under `docker-default` unless told otherwise. The profile template denies `mount` and writes to most of `/proc` and `/sys`, and limits `ptrace` to peers under the same profile.
```bash
docker inspect -f '{{.AppArmorProfile}}' app
cat /proc/$(docker inspect -f '{{.State.Pid}}' app)/attr/current
```
Custom profile:
```
# /etc/apparmor.d/containers/nginx-ro
#include <tunables/global>
profile nginx-ro flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>
  network inet tcp,
  /usr/sbin/nginx ix,
  /etc/nginx/** r,
  /var/log/nginx/** w,
  /run/nginx.pid rw,
  deny /bin/** wl,
  deny mount,
}
```
```bash
apparmor_parser -r -W /etc/apparmor.d/containers/nginx-ro
docker run --security-opt apparmor=nginx-ro nginx
docker run --security-opt apparmor=unconfined ...   # debug only
```
Kubernetes: `securityContext.appArmorProfile: {type: Localhost, localhostProfile: nginx-ro}` (1.30+), the profile must be loaded on every node.

## LXD
LXD generates a profile per instance, named `lxd-<instance>_<` plus the LXD var path plus `>`. `raw.apparmor` entries are appended to the generated profile (low-level, not recommended for production). `security.nesting` controls whether LXD can run nested inside the instance. Denials show `profile="lxd-c1_..."`.

## Snaps
Snap confinement is generated and managed by snapd; use the Snapcraft interface documentation for connecting interfaces and debugging snap denials.

## Verify
- [ ] Container shows the intended profile in `/proc/<pid>/attr/current`; forbidden writes fail with Permission denied and log DENIED.

## Checked
Checked 2026-10-26 against the Docker AppArmor docs (docker/docs), the moby/profiles docker-default template, the Kubernetes AppArmor tutorial, the LXD configuration metadata and the LXD instance profile naming code.
Confirmed: `docker-default` default and `--security-opt apparmor=NAME`; `apparmor_parser -r -W`; the template's deny rules for mount and /proc and /sys writes and its ptrace peer rule; the `AppArmorProfile` field of docker inspect (Docker swagger); Kubernetes `appArmorProfile` with `type: Localhost` and `localhostProfile` from v1.30, profile loaded on every node; LXD `raw.apparmor` and `security.nesting` semantics and the `lxd-<instance>_<path>` profile name.
Removed as unconfirmed: Podman profile names, the snap interface and snappy-debug section, and Incus.
Method: documentation only; no commands were run.
