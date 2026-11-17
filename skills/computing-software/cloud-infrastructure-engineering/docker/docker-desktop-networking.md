---
id: computing-software.cloud-infrastructure-engineering.docker.docker-desktop-networking
name: docker-desktop-networking
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-desktop, desktop-networking, host-docker-internal, host-networking, vpn, port-publishing]
level: practitioner
status: docs-checked
description: "Understand Docker Desktop networking: VM boundary, host.docker.internal, published ports on localhost, optional host networking, VPN and proxy conflicts, and subnet clashes."
sources: ["https://docs.docker.com/desktop/features/networking/", "https://docs.docker.com/desktop/features/networking/networking-how-tos/", "https://docs.docker.com/engine/network/drivers/host/#docker-desktop", "https://docs.docker.com/desktop/settings-and-maintenance/settings/#network"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker Desktop networking

On Docker Desktop, containers run inside a Linux VM. Each container gets an internal IP address
(for example `172.17.0.2`) inside the VM; Desktop forwards published ports to the host.

## What works
| Goal | How |
|---|---|
| Host -> container | `-p 8080:80` then `http://localhost:8080` |
| Container -> host service | `host.docker.internal` (resolves to the host); gateway alias `gateway.docker.internal` |
| Container -> other container | User-defined network + container name (same as Linux) |
| Container -> internet / VPN | NAT inside the VM; traffic reaches the host through the Desktop backend process (`com.docker.backend`), so firewalls and VPNs see it coming from that process |

`host.docker.internal` is built in on Desktop. On Linux Engine add it yourself:
`--add-host=host.docker.internal:host-gateway`.

## Host networking
The **Enable host networking** setting (Settings > Resources > Network; the settings table lists it
for Mac) allows containers started with `--net=host` to use `localhost` to reach TCP and UDP
services on the host, and lets host software use `localhost` to reach services in the container.
See the host network driver page for Docker Desktop. Without it, publish ports with `-p`.

## Common problems
- **Port published but unreachable from other machines**: `docker run -p` listens on all
  interfaces (`0.0.0.0`) by default, but you can restrict it to an address such as `127.0.0.1`, and
  Desktop's network settings can make it bind to `localhost` by default. Host firewalls can allow or
  deny inbound connections by filtering on `com.docker.backend`.
- **VPN clients**: Desktop networking can work when attached to a VPN by intercepting container
  traffic and injecting it into the host as if it originated from the Docker application. See the
  networking how-to page for VPN guidance.
- **Subnet clash with corporate network**: the **Docker subnet** setting (default
  `192.168.65.0/24`, used for internal services such as a DNS server and HTTP proxy) can be changed in
  Settings > Resources > Network.
- **Proxy**: Settings > Resources > Proxies. The Containers proxy governs `docker image pull`
  traffic; CLI plugins and tools that use the Docker API directly must be configured separately with
  the `HTTP_PROXY`, `HTTPS_PROXY` and `NO_PROXY` environment variables.
- **`host.docker.internal` unreachable**: confirm the name resolves from the container (it resolves
  to the host's internal IP) and that the host service listens on an address reachable from the VM.

## Verify
```bash
docker run --rm alpine ping -c1 host.docker.internal
docker run -d -p 8080:80 --name web nginx && curl -sI localhost:8080 | head -1
```

## Gotchas
- Inbound connections pass through the Desktop backend process (`com.docker.backend` on Mac,
  `com.docker.backend.exe` on Windows, `qemu` on Linux), which forwards ports into the VM.

## Checked

Date: 2026-10-24. Documentation release: Docker Desktop networking overview, networking how-tos and settings pages (docker/docs main).
Confirmed: container IPs inside the VM and published-port forwarding via the backend process, `host.docker.internal`
and `gateway.docker.internal`, NAT outbound path, the default `0.0.0.0` binding of `-p`, the Enable host networking setting
(Mac) and its behaviour, Docker subnet default `192.168.65.0/24`, proxy behaviour and environment variables, and
VPN traffic handling. Removed: vpnkit, the claim that container IPs are not routable, firewall prompt guidance,
`default-address-pools` advice, the VM-restart claim, and the Linux bridge-gateway statement, which the pages do
not state.

Method: documentation only; no commands were run.
