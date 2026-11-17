---
id: computing-software.systems-network-administration.netbird.install-docker
name: install-docker
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, docker, container-client, cap-net-admin, rootless-image]
level: practitioner
status: docs-checked
description: "Run the NetBird client in Docker or Compose: required capabilities, setup key variable, state volume, IPv6 sysctls and the rootless image."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/get-started/install/docker.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Join a container to an existing (cloud or self-hosted) NetBird deployment:

```
docker run --rm --name PEER_NAME --hostname PEER_NAME \
  --cap-add=NET_ADMIN --cap-add=SYS_ADMIN --cap-add=SYS_RESOURCE -d \
  -e NB_SETUP_KEY=<SETUP KEY> \
  -v netbird-client:/var/lib/netbird netbirdio/netbird:latest
```

- The example adds `NET_ADMIN`. The page recommends `SYS_ADMIN` and `SYS_RESOURCE` because NetBird uses eBPF and raw sockets; the experience may vary by daemon, OS and kernel.
- The volume keeps client state across restarts.
- Other settings are passed as environment variables.

Compose: set `cap_add`, `network_mode: host`, `NB_SETUP_KEY`, the `netbird-client` volume, and `devices: /dev/net/tun` for userspace mode or when the kernel module is missing.

IPv6 overlay without host networking: add `--sysctl net.ipv6.conf.all.disable_ipv6=0 --sysctl net.ipv6.conf.all.forwarding=1`.

Rootless: image `netbirdio/netbird:rootless-latest` needs no privileges and uses a userspace WireGuard stack. It supports inbound access or acting as a routing peer; outbound works only through a SOCKS proxy.

Self-hosted gotcha: without `--management-url` the client defaults to the cloud API. Fix with `netbird down` then `netbird up --management-url <URL>`.

## Checked

2026-11-04. Confirmed against the NetBird Docker installation page: docker run example, capability recommendation, volume, environment variables, Compose settings, IPv6 sysctls, rootless image behaviour, default management URL troubleshooting. Softened the NET_ADMIN wording, which the page does not call required.
Method: documentation only; no commands were run.
