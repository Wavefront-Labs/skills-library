---
id: computing-software.systems-network-administration.linux.podman-rootless-containers
name: podman-rootless-containers
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, podman, rootless, rootless-containers, quadlet, podman-systemd, subuid, subgid, user-namespaces, loginctl-linger, podman-generate-systemd, container-registries, skopeo, buildah, podman-pod, podman-auto-update, selinux-containers, pasta, slirp4netns, rhcsa, containers, sysadmin, podman-network]
level: practitioner
status: docs-checked
description: "Run containers as an unprivileged user with Podman: subuid/subgid, registries, volumes with SELinux labels, Quadlet units so systemd owns the container, auto-update, rootless networking limits."
sources:
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-systemd.unit.5.md
  - https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-auto-update.1.md.in
  - https://github.com/containers/container-libs/blob/main/image/docs/containers-registries.conf.5.md
  - https://github.com/torvalds/linux/blob/master/Documentation/networking/ip-sysctl.rst
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Podman rootless containers — services in containers, owned by systemd, without root

**Goal:** a non-root service account runs containers that start at boot, survive
logout, mount data with correct labels, update themselves, and need no daemon.

## 1. Prerequisites for the user
```bash
# install podman and the user-namespace helpers (uidmap/newuidmap) and passt (pasta) from your distribution
useradd -m svc-web
grep svc-web /etc/subuid /etc/subgid      # format USERNAME:UID:RANGE; ranges must not overlap between users; else add one:
usermod --add-subuids 200000-265535 --add-subgids 200000-265535 svc-web
loginctl enable-linger svc-web            # a user manager starts at boot and stays after logout
sysctl -w net.ipv4.ip_unprivileged_port_start=80   # first unprivileged port; persist in /etc/sysctl.d, or publish 8080 instead
```
Run everything below in a real login session of that user so that `XDG_RUNTIME_DIR` is set (normally `/run/user/<uid>` on systemd hosts).
Run `podman system migrate` after changing subuid ranges (it restarts containers with the new mappings).

## 2. Images and registries
```bash
podman login registry.example.com                      # creds in ${XDG_RUNTIME_DIR}/containers/auth.json
podman pull docker.io/library/nginx:1.27              # always fully qualify; or set unqualified-search-registries
```
Registry configuration is read from `$XDG_CONFIG_HOME/containers/registries.conf` (default `~/.config/containers/registries.conf`) per user and from the system files under `/etc/containers/` (`unqualified-search-registries`, mirrors and `insecure` registry entries are set there).
Storage: `${XDG_DATA_HOME}/containers/storage` (rootless graphroot) vs the rootful graphroot under `/var/lib/containers/storage` — images aren't shared between them.

## 3. Run with data and SELinux
```bash
mkdir -p ~/web/html
podman run -d --name web -p 8080:80 -v ~/web/html:/usr/share/nginx/html:Z,ro \
   --userns=keep-id --memory 512m --restart=no docker.io/library/nginx:1.27
podman unshare ls -ln ~/web/html        # view ownership from inside the user namespace
podman logs -f web; podman exec -it web sh; podman top web; podman stats
```
- `:Z` relabels the bind mount `container_file_t` (private); `:z` shared between containers.
  Without a relabel, SELinux can deny the container access to the mount.
- Rootless UID mapping: container root = your UID; container UID 1000 = subuid start+999. Files
  written by a non-root container user look owned by a weird high UID on the host — that's the
  map. `--userns=keep-id` makes the container's user equal your host UID (good for bind mounts).
- The Podman docs say not to use `--restart` for containers run in systemd services; let systemd restart them (below).
- Secrets: `podman secret create db_pass -` then `--secret db_pass` (file at `/run/secrets/db_pass`).

## 4. Quadlet: systemd owns the container
`$XDG_CONFIG_HOME/containers/systemd/web.container` (usually `~/.config/containers/systemd/`; root: `/etc/containers/systemd/`):
```ini
[Unit]
Description=web nginx
After=network-online.target

[Container]
Image=docker.io/library/nginx:1.27
ContainerName=web
PublishPort=8080:80
Volume=%h/web/html:/usr/share/nginx/html:Z,ro
AutoUpdate=registry
Environment=TZ=UTC
HealthCmd=curl -fs http://localhost/ || exit 1
HealthInterval=30s
Notify=healthy

[Service]
Restart=always
TimeoutStartSec=300

[Install]
WantedBy=default.target
```
```bash
systemctl --user daemon-reload          # generator turns web.container into web.service
systemctl --user start web; systemctl --user status web
systemctl --user enable podman-auto-update.timer   # daily at midnight by default; AutoUpdate=registry checks the registry for a changed image digest
/usr/lib/systemd/system-generators/podman-system-generator --user --dryrun   # view generated files and errors
journalctl --user -u web -f
```
Other Quadlet file types: `.volume`, `.network`, `.build`, `.pod` and `.kube` (a Kubernetes YAML run via `podman kube play`), plus `.artifact`. Auto-update with `AutoUpdate=registry` requires a fully-qualified image reference; if restarting the unit after an update fails, `podman auto-update` rolls back to the previous image by default (`--rollback`).

## 5. Networking and limits of rootless
- Rootless networking uses `pasta` (from the passt package) by default; rootful uses netavark. Unprivileged users cannot create host network interfaces, and ports below the sysctl's first unprivileged port need the sysctl above. Rootless users can also create netavark bridge networks.
- Anything needing host-level privileges runs as root Podman (`/etc/containers/systemd/*.container`, same syntax).
- Resource ownership is per user: `podman system df`, `podman system prune -a` affect only that user's storage.

## Failure modes
- Rootless Podman fails to start containers when the user has no `/etc/subuid` and `/etc/subgid` range.
- `Error: ... permission denied` after reboot: `loginctl enable-linger` missing → units never started.
- Container starts via `podman run` but not via systemd: SELinux denial on the volume (`ausearch -m avc`)
  or `%h` paths with a different `HOME`; check `systemctl --user status`.
- Port in use from a previous `podman run`: `podman ps -a` and remove the stale container; without `ContainerName` Quadlet names containers `systemd-<unit name>`.

## Verify
- [ ] `systemctl --user is-active web` after a full reboot with the user logged out; `curl localhost:8080` serves.
- [ ] `podman inspect web | grep -i userns` shows the mapping; files created by the container are owned as expected on the host.
- [ ] `podman auto-update --dry-run` reports the unit as eligible; a changed image digest gets pulled on the next timer run.

## Checked
Checked 2026-10-25 against the Podman documentation source on GitHub (containers/podman docs/, main, last commit 2026-10-23; latest release v5.8.9), the containers/container-libs registries.conf page, the systemd loginctl and systemd.unit manuals and the Linux ip-sysctl documentation: subuid/subgid file format and uniqueness (rootless tutorial), `podman system migrate`, `loginctl enable-linger` semantics, `ip_unprivileged_port_start` meaning, auth file `${XDG_RUNTIME_DIR}/containers/auth.json`, per-user `registries.conf` path, rootless graphroot default, `-v ...:Z,ro`, `--userns=keep-id`, `podman unshare`, Quadlet search paths, file types and generator `--dryrun` command, container keys `Image`, `ContainerName`, `PublishPort`, `Volume`, `AutoUpdate`, `Environment`, `HealthCmd`, `HealthInterval`, `Notify=healthy` (requires a healthcheck), `[Service]`/`[Install]` sections, `%h` specifier (systemd.unit), `podman-auto-update.timer` (daily at midnight), `--rollback` default true, registry policy needing a fully-qualified image, pasta as the rootless default, `--restart` guidance. Removed unconfirmed claims: package commands, the `sudo -u` failure remark, the skopeo/jq pipeline, Quadlet and pasta version gates, the deprecation of `podman generate systemd`, the rootless limitation list, cgroup v2 requirement, user-defined-network remark and the exact error text.

Method: documentation only; no commands were run.
