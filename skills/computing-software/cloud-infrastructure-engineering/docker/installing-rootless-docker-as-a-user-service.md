---
id: computing-software.cloud-infrastructure-engineering.docker.installing-rootless-docker-as-a-user-service
name: installing-rootless-docker-as-a-user-service
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, rootless, rootless-docker, dockerd-rootless-setuptool, rootless-install, enable-linger, loginctl, systemd-user]
level: advanced
description: "Install rootless Docker with dockerd-rootless-setuptool.sh, set DOCKER_HOST, keep it running after logout with loginctl enable-linger, and uninstall cleanly."
sources: ["https://docs.docker.com/engine/security/rootless/", "https://docs.docker.com/engine/security/rootless/tips/", "https://docs.docker.com/engine/security/rootless/troubleshoot/", "https://github.com/moby/moby/blob/master/api/swagger.yaml"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing rootless Docker as a user service

## Prerequisites (as root, once)
```sh
sudo apt-get install -y uidmap dbus-user-session           # newuidmap/newgidmap; user D-Bus session
grep "^$USERNAME:" /etc/subuid /etc/subgid                 # need >= 65536 ids each
# if missing, add a non-overlapping range of at least 65536 IDs to /etc/subuid and /etc/subgid
sudo systemctl disable --now docker.service docker.socket  # optional: no rootful daemon
```
Ubuntu 24.04 and later restrict unprivileged user namespaces by default. The `docker-ce-rootless-extras`
deb package bundles the AppArmor profile for `rootlesskit`; with the install script you must add one
for `$HOME/bin/rootlesskit` manually (see the Rootless troubleshooting page).

## Install (as the user, real login session - not `su`)
```sh
dockerd-rootless-setuptool.sh install          # from docker-ce-rootless-extras
# or without packages:  curl -fsSL https://get.docker.com/rootless | sh
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock    # only if an application needs it
docker context use rootless                     # the tool creates and selects this context (Engine 23.0+)
systemctl --user status docker
```
Switching users with `sudo su` or `sudo -iu` breaks systemd detection and the user bus; log in with
`ssh user@localhost` or `machinectl shell user@` (from `systemd-container`).

## Survive logout and start at boot
```sh
sudo loginctl enable-linger $USERNAME
systemctl --user enable docker
```
Without lingering, the daemon does not start automatically at boot or outside a login session.

## Config locations
- daemon config: `~/.config/docker/daemon.json`
- data-root: `~/.local/share/docker`
- socket: `$XDG_RUNTIME_DIR/docker.sock` (usually `/run/user/<uid>/docker.sock`)
- unit: `~/.config/systemd/user/docker.service` (environment overrides go in
  `~/.config/systemd/user/docker.service.d/override.conf`, e.g.
  `Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_NET=lxc-user-nic"`; then `systemctl --user daemon-reload`)

## Uninstall
```sh
dockerd-rootless-setuptool.sh uninstall
rootlesskit rm -rf ~/.local/share/docker        # the uninstall tool does not remove binaries or data
```

## Verify
```sh
docker info -f '{{.SecurityOptions}}'          # contains name=rootless
docker run --rm alpine id                       # uid=0 inside, mapped to your user outside
```

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main) Rootless mode, Tips and Troubleshooting pages; Docker Engine API (SecurityOptions).
- Confirmed `uidmap` prerequisite and 65,536 subordinate IDs, `dockerd-rootless-setuptool.sh install` and `uninstall`, the `get.docker.com/rootless` script, the `rootless` context (automatic since Engine 23.0), `loginctl enable-linger`, `systemctl --user` management, config, data and socket locations, `dbus-user-session`, `machinectl shell user@`, Ubuntu 24.04 AppArmor handling, and `rootlesskit rm -rf ~/.local/share/docker`.
- Confirmed `name=rootless` in `docker info` SecurityOptions.
- Removed slirp4netns/passt package names, the `usermod` command, the linger check command and the `ps` check that no checked source covers.
Method: documentation only; no commands were run.
