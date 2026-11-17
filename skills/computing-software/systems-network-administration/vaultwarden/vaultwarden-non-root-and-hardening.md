---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-non-root-and-hardening
name: vaultwarden-non-root-and-hardening
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, docker, non-root, rocket-port, hardening, podman, cap-net-bind-service, read-only-mount]
level: advanced
status: docs-checked
description: "Run Vaultwarden as a non-root container user, handle low ports with ROCKET_PORT or CAP_NET_BIND_SERVICE, fix data directory ownership, and apply Docker hardening advice."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/Running-docker-container-with-non-root-user", "https://github.com/dani-garcia/vaultwarden/wiki/Hardening-Guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden non-root and hardening

By default the container runs as root. To run unprivileged:

```
docker run -d --name vaultwarden --user nobody   -e ROCKET_PORT=1024 -v /vw-data/:/data/ -p 80:1024 vaultwarden/server:latest
```

Ports below 1024 need either a high `ROCKET_PORT` inside the container (mapped back with `-p 80:1024`) or, in compose, `cap_add: [CAP_NET_BIND_SERVICE]` with `user: nobody`.

The data directory must be writable by the container user; for `nobody` that is UID 65534:

```
mkdir /vw-data && chown 65534 /vw-data && chmod u+rwx /vw-data
```
The UID must exist in the container's `/etc/passwd`, not necessarily on the host. A numeric form works too: `docker run -u 1000:1000` or compose `user: 1000:1000`. Rootless Podman: `podman run --userns keep-id`.

Other hardening points from the guide: mount only the data directory and needed certificates (never the home directory or the Docker socket), add `:ro` to mounts Vaultwarden should not modify, put the app behind a reverse proxy rather than Rocket TLS, disable signups, invitations and password hints if unused, run Fail2Ban, and optionally serve under an unguessable subdirectory as defence in depth.

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: Running-docker-container-with-non-root-user and Hardening-Guide.
Removed or reworded: the unconfirmed claim that Docker 20.10.0+ lets non-root processes bind privileged ports.
Method: documentation only; no commands were run.
