---
id: computing-software.cloud-infrastructure-engineering.docker.custom-apparmor-and-selinux-for-containers
name: custom-apparmor-and-selinux-for-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, apparmor, apparmor-parser, custom-apparmor, selinux, container-t, selinux-z, z-label, mac]
level: sme
description: "Load and apply a custom AppArmor profile with apparmor_parser, and run Docker under SELinux (container_t, :z/:Z relabels, svirt categories) without disabling it."
sources: ["https://docs.docker.com/engine/security/apparmor/", "https://docs.docker.com/engine/storage/bind-mounts/", "https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/reference/cli/dockerd/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom AppArmor and SELinux for containers

## AppArmor (Ubuntu/Debian/SUSE)
Containers get `docker-default` unless told otherwise. Custom profile:
```
# /etc/apparmor.d/containers/docker-nginx
#include <tunables/global>
profile docker-nginx flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>
  network inet tcp,
  network inet6 tcp,
  capability chown,
  capability setuid,
  capability setgid,
  capability net_bind_service,
  /usr/sbin/nginx ix,
  /etc/nginx/** r,
  /usr/share/nginx/html/** r,
  /var/cache/nginx/** rw,
  /var/run/nginx.pid rw,
  deny /bin/** mrwklx,
  deny /proc/sys/** w,
  deny mount,
}
```
```sh
sudo apparmor_parser -r -W /etc/apparmor.d/containers/docker-nginx   # load/replace
docker run --security-opt "apparmor=docker-nginx" -p 80:80 nginx
sudo aa-status                              # lists loaded profiles
sudo dmesg                                  # look for apparmor="DENIED" lines
```
- Profiles must be loaded on **every** host before containers start (ship via config
  management; they don't travel with images).
- Unload a profile with `apparmor_parser -R /path/to/profile`.
- `--security-opt apparmor=unconfined` disables it - avoid.

## SELinux (RHEL/Fedora/CentOS)
```json
{ "selinux-enabled": true }
```
Without a correct label, the security system might stop container processes using mounted content, and
by default Docker does not change labels set by the OS. Add a suffix to a bind mount to relabel it:
```sh
docker run -v /srv/app:/data:z app     # shared: content is shared among multiple containers
docker run -v /srv/app:/data:Z app     # private and unshared
```
- **Never** `:Z` system directories such as `/home` or `/usr`: it can render the host inoperable and
  you may need to relabel host files by hand. The labels change the host files themselves.
- Per-container label options of `--security-opt`: `label=user:USER`, `label=role:ROLE`,
  `label=type:TYPE`, `label=level:LEVEL` (for example `label=level:s0:c100,c200`), `label=disable`.

## Verify
`docker inspect -f '{{.AppArmorProfile}}' web` shows the AppArmor profile set for the container; a denied
action appears in `dmesg` as an `apparmor="DENIED"` line.

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main: AppArmor page, bind-mounts page, `docker run` reference, `dockerd` reference), Docker Engine API (AppArmorProfile).
- Confirmed the AppArmor example profile structure (`profile docker-nginx flags=(attach_disconnected,mediate_deleted)`, one `capability` rule per line, `network inet tcp`), the load commands `apparmor_parser -r -W` and `-R`, `--security-opt "apparmor=docker-nginx"`, `aa-status`, `dmesg` DENIED lines and the `docker-default` profile.
- Confirmed the `selinux-enabled` daemon option, the `:z` (shared) and `:Z` (private) bind-mount suffixes and the warning about system directories, and the `label=` security-opt forms.
- Removed `container_t`/MCS descriptions, `ausearch`, `ls -Z`, udica, `aa-logprof` and `/proc/1/attr/current` claims that no checked source covers.
Method: documentation only; no commands were run.
