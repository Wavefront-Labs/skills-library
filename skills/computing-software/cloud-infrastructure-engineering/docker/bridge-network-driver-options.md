---
id: computing-software.cloud-infrastructure-engineering.docker.bridge-network-driver-options
name: bridge-network-driver-options
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, bridge-network, bridge-options, bridge-name, enable-icc, ip-masquerade, host-binding-ipv4, network-mtu, docker-network-create, driver-opts]
level: advanced
status: docs-checked
description: "Set com.docker.network.bridge.* and driver options on user-defined bridges: fixed interface names, ICC off, no masquerade, default bind IP, MTU, and how to verify them."
sources: ["https://docs.docker.com/engine/network/drivers/bridge/", "https://docs.docker.com/reference/cli/docker/network/create/", "https://docs.docker.com/engine/network/packet-filtering-firewalls/", "https://docs.docker.com/engine/network/port-publishing/", "https://docs.docker.com/reference/compose-file/networks/#driver_opts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bridge driver options (com.docker.network.bridge.*)

**Goal:** shape a user-defined bridge for firewalls, monitoring and isolation instead of
accepting the random `br-<id>` defaults.

## The options
| Option | Default | Effect |
|---|---|---|
| `com.docker.network.bridge.name` | generated (`br-...`) | Interface name to use when creating the Linux bridge |
| `com.docker.network.bridge.enable_icc` | `true` | `false` blocks container-to-container traffic on this network |
| `com.docker.network.bridge.enable_ip_masquerade` | `true` | `false` disables SNAT for outbound traffic |
| `com.docker.network.bridge.host_binding_ipv4` | all IPv4 and IPv6 addresses | default host IP for `-p` on this network (an IPv6 address is accepted despite the name) |
| `com.docker.network.driver.mtu` | `0` (no limit) | containers' network MTU |
| `com.docker.network.container_iface_prefix` | `eth` | interface name prefix inside containers |
| `com.docker.network.bridge.gateway_mode_ipv4` / `_ipv6` | `nat` | `nat-unprotected`, `routed` or `isolated` (`isolated` needs `--internal`; see the nftables/gateway-modes skill) |
| `com.docker.network.bridge.inhibit_ipv4` | `false` | prevent Docker assigning an IP address to the bridge |

## Examples
```bash
# Stable name for firewall rules and tcpdump, internal-only east-west blocked, small MTU for a VPN underlay
docker network create -d bridge \
  --subnet 172.30.10.0/24 --gateway 172.30.10.1 \
  -o com.docker.network.bridge.name=br-web \
  -o com.docker.network.bridge.enable_icc=false \
  -o com.docker.network.driver.mtu=1400 \
  web

# Publish everything on this network to one host IP by default
docker network create -o com.docker.network.bridge.host_binding_ipv4=10.0.0.5 edge
docker run -d --network edge -p 8080:80 nginx      # binds 10.0.0.5:8080, not 0.0.0.0
```
Compose:
```yaml
networks:
  web:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.name: br-web
      com.docker.network.bridge.enable_icc: "false"
      com.docker.network.driver.mtu: "1400"
    ipam:
      config: [{ subnet: 172.30.10.0/24 }]
```
Values are strings in Compose (`"false"`, `"1400"`).

## Behaviour notes
- `enable_icc=false` disables inter-container connectivity on this network (the default bridge uses the daemon `icc` key instead).
- `enable_ip_masquerade=false` means outbound packets leave with the container IP; the
  upstream router needs a route back to the subnet (or use `gateway_mode_ipv4=routed`).
- Options are set at `docker network create`; the CLI has no command to change them, so recreate the network (which requires disconnecting its containers).
- The **default** `docker0` bridge is configured in `daemon.json` (`bip`, `mtu`, `icc`,
  `ip-masq`), not with these options.

## Verify
```bash
docker network inspect web -f '{{json .Options}}'
ip link show br-web                                  # MTU 1400
docker run --rm --network web alpine ping -c1 -W1 <other container ip>   # fails with icc=false
```

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Option names and defaults were checked against the bridge driver options table (name, enable_ip_masquerade, host_ipv4, gateway_mode_*, enable_icc, host_binding_ipv4, driver.mtu default 0, container_iface_prefix, inhibit_ipv4), the daemon.json equivalents for the default bridge (bip, mtu, icc, ip-masq) in the `dockerd` reference, and the gateway modes on the port publishing page. Removed unconfirmed claims: 15-character name limit, exact `br-` hex length, published-port behaviour under `icc=false`, name-collision behaviour, and the legacy isolation chain name.

Method: documentation only; no commands were run.
