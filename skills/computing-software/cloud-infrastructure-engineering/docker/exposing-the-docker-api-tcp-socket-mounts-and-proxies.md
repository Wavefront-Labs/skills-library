---
id: computing-software.cloud-infrastructure-engineering.docker.exposing-the-docker-api-tcp-socket-mounts-and-proxies
name: exposing-the-docker-api-tcp-socket-mounts-and-proxies
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-socket, docker-sock, socket-exposure, dockerd-hosts-flag, tcp-2375, socket-mount, socket-alternatives, tecnativa-socket-proxy, socket-proxy-filter, socket-proxy]
level: advanced
description: "Assess Docker API exposure: why tcp://0.0.0.0:2375 and docker.sock mounts are root access, what to use instead, and filtering access with a socket proxy."
sources: ["https://docs.docker.com/engine/security/protect-access/", "https://docs.docker.com/engine/daemon/remote-access/", "https://github.com/Tecnativa/docker-socket-proxy"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Exposing the Docker API: TCP, socket mounts and proxies

## Anyone with API access is root on the host
```sh
docker -H tcp://victim:2375 run --rm -v /:/host --privileged alpine chroot /host sh
```
The same applies to a container that mounts `/var/run/docker.sock`. Docker warns that unsecured remote access can give remote non-root users root on the host.

## dockerd -H tcp
```json
{ "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2376"],
  "tls": true, "tlsverify": true,
  "tlscacert": "/etc/docker/ca.pem", "tlscert": "/etc/docker/server-cert.pem", "tlskey": "/etc/docker/server-key.pem" }
```
- 2375 = plaintext, no auth (the conventional port for unencrypted access). Do not bind it beyond `127.0.0.1`. Docker states that remote access without TLS is not recommended and will require explicit opt-in in a future release.
- 2376 = TLS; `tlsverify` with `tlscacert` makes it **mutual** TLS (only clients with a certificate signed by that CA connect). With only `tls`, `tlscert` and `tlskey` the server does not authenticate clients.
- Prefer SSH (`ssh://` contexts): Docker documents it as the way to protect the daemon socket without a network listener, using existing SSH keys.
- With `hosts` in daemon.json, clear `-H fd://` from the systemd `ExecStart` (the daemon fails to start otherwise). Configuring remote access in both the unit file and daemon.json also conflicts.

## Socket mounts: who needs them and alternatives
| Need | Alternative to raw socket |
|---|---|
| Reverse proxy discovering containers (Traefik) | socket proxy allowing only `CONTAINERS=1`, read-only (`POST` left at 0) |
| Monitoring | socket proxy with `POST` left at 0 (GET and HEAD only) |
| CI building images | a remote or rootless builder instead of the host socket |
| Tools that must start or stop containers | socket proxy with `POST=1` plus the narrow `ALLOW_START` / `ALLOW_STOP` / `ALLOW_RESTARTS` switches |

## Filtering socket proxy
```yaml
services:
  socket-proxy:
    image: tecnativa/docker-socket-proxy:latest
    environment:
      CONTAINERS: 1      # revoked by default; allows the containers API (GET and HEAD only unless POST=1)
      EVENTS: 1          # granted by default
      PING: 1            # granted by default
      POST: 0            # default: only GET and HEAD allowed
    volumes: ["/var/run/docker.sock:/var/run/docker.sock:ro"]
    networks: [proxy-internal]
  traefik:
    command: --providers.docker.endpoint=tcp://socket-proxy:2375
    networks: [proxy-internal, web]
networks:
  proxy-internal: { internal: true }
```
It is an HAProxy image with a small configuration that matches API sections (`IMAGES`, `NETWORKS`, `EXEC`, `BUILD`... are revoked by default) and returns `403 Forbidden` for blocked requests.
`:ro` on the socket mount does **not** make the API read-only - the proxy's `POST=0` does.
Keep the proxy on an internal network; it's still a privileged endpoint.

## Verify
```sh
ss -ltnp | grep dockerd                     # no 0.0.0.0:2375
docker run --rm --network proxy-internal curlimages/curl -s -XPOST socket-proxy:2375/containers/x/stop  # expect 403 Forbidden
curl https://host:2376/version             # fails without client cert
```

## Checked

Checked against docker/docs `engine/security/protect-access.md`, `engine/daemon/remote-access.md` and `engine/daemon/troubleshoot.md` (docker/docs latest commit 2026-10-23, Engine 29), and the README of Tecnativa/docker-socket-proxy.

- 2375 plaintext and 2376 TLS conventions, the `tlsverify`/`tlscacert`/`tls` combinations and what each authenticates, SSH contexts, the `hosts`/`-H` conflict.
- Socket proxy: HAProxy based, `EVENTS` and `PING` granted by default, `CONTAINERS`, `IMAGES`, `NETWORKS`, `EXEC`, `BUILD` revoked by default, `POST` disabled means only GET and HEAD, 403 responses, `ALLOW_START`/`ALLOW_STOP`/`ALLOW_RESTARTS`.
- Removed as unconfirmed: the claim about scanners and cryptominers, the "newer releases refuse to start" claim, and named tool alternatives for CI. The `:ro` socket mount statement is reasoning about the API surface; the socket proxy README confirms the `POST` switch is what enforces read-only access.

Method: documentation only; no commands were run.
