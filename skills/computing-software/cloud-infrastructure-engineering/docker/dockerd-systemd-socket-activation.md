---
id: computing-software.cloud-infrastructure-engineering.docker.dockerd-systemd-socket-activation
name: dockerd-systemd-socket-activation
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerd, fd-socket, socket-activation, systemd, docker-socket, daemon-config]
level: advanced
status: docs-checked
description: "Understand dockerd -H fd:// and docker.socket: how systemd socket activation starts the daemon, changing socket group and permissions, adding a TCP listener safely, and pitfalls."
sources: ["https://docs.docker.com/reference/cli/dockerd/#bind-docker-to-another-hostport-or-a-unix-socket", "https://docs.docker.com/engine/daemon/remote-access/", "https://github.com/moby/moby/tree/master/contrib/init/systemd", "https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dockerd and systemd socket activation

The packaged unit runs `dockerd -H fd:// --containerd=/run/containerd/containerd.sock`.
`fd://` means "use the sockets systemd passes in", defined by `docker.socket`.

## How it works
```ini
# docker.socket as shipped in the moby source tree (packaged path varies by distro)
[Socket]
ListenStream=/run/docker.sock
SocketMode=0660
SocketUser=root
SocketGroup=docker
```
- systemd owns `/run/docker.sock` (the unit notes that if `/var/run` is not a symlink to `/run` you may need `ListenStream=/var/run/docker.sock`).
- If `docker.service` is stopped but `docker.socket` is active, the first client connection
  starts dockerd. That is why `systemctl stop docker` prints
  a warning from systemd that the service can still be activated by `docker.socket`.
- To really stop it: `sudo systemctl stop docker.socket docker.service`.

## Change socket group or permissions
```bash
sudo systemctl edit docker.socket
```
```ini
[Socket]
SocketGroup=container-admins
```
```bash
sudo systemctl daemon-reload && sudo systemctl restart docker.socket docker.service
ls -l /run/docker.sock
```

## Add a TCP listener (with TLS)
Option A, systemd socket (keeps `fd://`):
```ini
# systemctl edit docker.socket
[Socket]
ListenStream=
ListenStream=/run/docker.sock
ListenStream=10.0.0.5:2376
```
TLS settings then go in `daemon.json` (`tlsverify`, `tlscacert`, `tlscert`, `tlskey`). Assigning an empty `ListenStream=` resets the listener list.

Option B, `hosts` in `daemon.json`: you must remove `-H fd://` from `ExecStart` or dockerd
fails with "directives are specified both as a flag and in the configuration file":
```ini
# systemctl edit docker.service
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd --containerd=/run/containerd/containerd.sock
```

## Gotchas
- Remote access without TLS (conventionally port `2375`; `2376` for TLS) can give remote users root on the host and is not recommended; Docker says it will require explicit opt-in in a future release.
- With `-H fd://`, if the socket-activated files are not found the daemon exits; keep `docker.socket` enabled (the packaged `docker.service` has `Requires=docker.socket`) or change `-H`.

## Verify
```bash
systemctl status docker.socket docker.service --no-pager
sudo ss -xlp | grep docker.sock; sudo ss -tlnp | grep 2376
```

## Checked

Checked against docker/docs `engine/daemon/remote-access.md` and the dockerd reference ("Bind Docker to another host/port or a unix socket"), the moby `contrib/init/systemd/docker.socket` and `docker.service` files, and the systemd `systemd.socket` man page source (docker/docs latest commit 2026-10-23).

- `docker.socket` contents (`ListenStream=/run/docker.sock`, `SocketMode=0660`, `SocketUser=root`, `SocketGroup=docker`), `docker.service` `ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock` and `Requires=docker.socket`.
- Docker documents `-H fd://` as systemd socket activation and says the daemon exits if the activated sockets are missing.
- Empty `ListenStream=` resets the list and `SocketUser`/`SocketGroup` exist in systemd.socket.
- Removed as unconfirmed: the verbatim `no sockets found` message, the exact systemd warning text and the rootless socket remark.

Method: documentation only; no commands were run.
