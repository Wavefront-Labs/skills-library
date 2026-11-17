---
id: computing-software.cybersecurity-defensive.authentik.outpost-docker-integration
name: outpost-docker-integration
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, outpost, docker, docker-socket-proxy, ssh, traefik-labels]
level: advanced
status: docs-checked
description: "Use the authentik Docker outpost integration: settings, Traefik labels, required Docker API permissions, socket proxy over HTTP, remote hosts via TLS or SSH."
sources:
  - https://docs.goauthentik.io/add-secure-apps/outposts/integrations/docker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let authentik deploy and upgrade outpost containers through the Docker API; outposts upgrade with authentik.

## Settings used
`object_naming_template`, `container_image`, `docker_network` (change it if outposts reach authentik by internal hostname), `docker_map_ports` (disable behind Traefik), `docker_labels`. The container always gets label `io.goauthentik.outpost-uuid`. Proxy outposts also get Traefik labels (`traefik.enable`, a router `ak-outpost-<outpost-name>-router` with a `Host(...)` rule and tls, and a service whose healthcheck path is `/outpost.goauthentik.io/ping` on port `9300` with server port `9000`).

## Docker API permissions needed
Images/Pull, Containers/Read, Containers/Create, Containers/Kill, Containers/Remove, System/Info.

## Socket proxy
Mounting the Docker socket gives full API access and possible root escalation, so use a filtering docker-socket-proxy allowing only those calls. authentik must reach the proxy over HTTP, for example `http://<proxy hostname>:<port>`, not TCP.

## Remote host via TLS
Follow Docker's TLS guide, then create two keypairs in authentik: `Docker CA` (contents of `~/.docker/ca.pem`) and `Docker Cert` (`cert.pem` as certificate, `key.pem` as private key). In the integration use CA as TLS Verification Certificate and Cert as TLS Authentication Certificate.

## Remote host via SSH
```shell
ssh-keygen -t rsa -f authentik  -N "" -m pem
openssl req -x509 -sha256 -nodes -days 365 -out certificate.pem -key authentik
```
Add `authentik.pub` to the target user's `~/.ssh/authorized_keys`, import `authentik` and `certificate.pem` as a keypair, and set Docker URL `ssh://hostname` (default user `authentik` unless specified). For custom SSH config mount it at `/authentik/.ssh/config`, other files under `/opt`, use `ssh://hostname` and select no keypair.

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/add-secure-apps/outposts/integrations/docker/ (read in full).
