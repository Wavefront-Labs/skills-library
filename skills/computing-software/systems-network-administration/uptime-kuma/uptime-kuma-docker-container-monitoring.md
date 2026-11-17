---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-docker-container-monitoring
name: uptime-kuma-docker-container-monitoring
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [docker-monitor, docker-sock, docker-host, docker-tls, tcp-bridge, container-monitoring]
level: advanced
status: docs-checked
description: "Monitor Docker containers from Uptime Kuma via a shared docker.sock or a TCP/TLS Docker host, and understand the security cost."
sources: ["https://github.com/louislam/uptime-kuma/wiki/How-to-Monitor-Docker-Containers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Monitoring Docker containers

Available since 1.18.0. Uptime Kuma in a container cannot see the host Docker daemon unless you give it access. Warning from the docs: access to the Docker socket or TCP port gives full control of the daemon; do not expose Uptime Kuma to the internet when using it.

Method 1: share the socket.
```bash
-v /var/run/docker.sock:/var/run/docker.sock
```
(or the same line under `volumes:` in Compose).

Method 2: Docker over TCP. Edit `/etc/docker/daemon.json`:
```json
{
  "tls": true,
  "tlscacert": "/var/docker/ca.pem",
  "tlscert": "/var/docker/server.pem",
  "tlskey": "/var/docker/serverkey.pem",
  "hosts": ["unix:///var/run/docker.sock", "tcp://<host IP address>:2376"]
}
```
The unencrypted option (`tls: false`, port 2375) is for closed networks only. Restart with `sudo systemctl restart docker.service`. If the daemon fails with a duplicate `hosts`/`-H` key, clear and override ExecStart via `sudo systemctl edit docker.service` (an empty `ExecStart=` first, then the original without `-H`). For Snap Docker the file is `/var/snap/docker/current/config/daemon.json` and the service is `snap.docker.dockerd.service`.

In Uptime Kuma add a Docker Host and choose TCP with host and port. For TLS, put certificates in `data/docker-tls/<FQDN of the docker host>/` as `ca.pem`, `key.pem`, `cert.pem` (mount `-v /docker-cert:/app/data/docker-tls` in a container).

Rootless Uptime Kuma images cannot use the Docker monitor without extra configuration.

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: How to Monitor Docker Containers page (1.18.0, socket and TCP methods, daemon.json, systemd override, snap paths, certificate directory) and Docker Tags page (rootless limitation). Removed: The unconfirmed instruction to add the host in Settings using the socket path, and the generic verify line.

Method: documentation only; no commands were run.
