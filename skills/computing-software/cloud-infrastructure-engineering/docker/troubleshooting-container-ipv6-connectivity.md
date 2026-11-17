---
id: computing-software.cloud-infrastructure-engineering.docker.troubleshooting-container-ipv6-connectivity
name: troubleshooting-container-ipv6-connectivity
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, ipv6, ipv6-troubleshooting, ip6tables, ndp-proxy, network-troubleshooting, dual-stack]
level: advanced
status: docs-checked
description: "Work out why containers have no IPv6: network not IPv6-enabled, no host route or forwarding, ip6tables off, NDP or router advertisements, and apps binding IPv4 only."
sources: ["https://docs.docker.com/engine/daemon/ipv6/", "https://docs.docker.com/engine/network/packet-filtering-firewalls/", "https://docs.kernel.org/networking/ip-sysctl.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting container IPv6 connectivity

Work from the container outwards.

## 1. Does the container have an IPv6 address?
```bash
docker network inspect <net> -f '{{.EnableIPv6}} {{json .IPAM.Config}}'
docker exec <c> ip -6 addr show eth0       # expect a non-fe80 address
```
No address: the network was created without `--ipv6` (Compose: `enable_ipv6: true`); recreate it with IPv6 enabled. The default bridge needs `"ipv6": true` and
`"fixed-cidr-v6"` in daemon.json.

## 2. Default route and gateway
```bash
docker exec <c> ip -6 route                 # default via <bridge gw> dev eth0
docker exec <c> ping -6 -c1 <gateway-ipv6>
```

## 3. Host forwarding and firewall
```bash
sysctl net.ipv6.conf.all.forwarding         # must be 1 (Docker enables it at start if it is off)
sudo ip6tables -t nat -S | grep -i docker   # MASQUERADE for ULA subnets in nat mode
sudo ip6tables -S DOCKER-USER
```
`ip6tables` is enabled by default; if it was set to `false`, Docker adds no IPv6 isolation or port-mapping rules.

Turning on forwarding can make the host ignore router advertisements on its uplink
(`accept_ra` drops to 0 unless set to 2), so the **host** loses its IPv6 default route:
```bash
sudo sysctl -w net.ipv6.conf.eth0.accept_ra=2
```

## 4. Routed (global) prefixes
If containers have global addresses without NAT, the upstream router must route the container
prefix to the host, or the host must answer neighbour solicitations: enable NDP proxy
(`net.ipv6.conf.eth0.proxy_ndp=1` plus `ip -6 neigh add proxy <addr> dev eth0`).

## 5. Name resolution and app binding
```bash
docker exec <c> getent ahosts example.com   # AAAA results present?
docker exec <c> ss -ltnp                     # listening on [::]: or only 0.0.0.0:?
```
Embedded DNS forwards to the host resolvers; if they have only IPv4 upstreams that is fine,
AAAA records still come back.

## 6. Published ports
`-p 8080:80` binds IPv4 and IPv6 on the host. If IPv6 clients cannot connect, check
`userland-proxy` settings and `ip6tables -t nat -L DOCKER`.

## Gotchas
- IPv6 is only supported on Docker daemons running on Linux hosts.

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the IPv6 page (`--ipv6`, default bridge `ipv6`/`fixed-cidr-v6`, `ip6tables` default, Linux-only), the packet-filtering page (Docker enables `net.ipv6.conf.all.forwarding`), the port publishing page (dual-stack publishing, routed mode) and the Linux ip-sysctl documentation (`accept_ra` value 2 overrules forwarding, `proxy_ndp`). Replaced the dead `engine/network/ipv6/` link. Removed in-place-switch, `docker info` output, prefix-delegation, Desktop and cloud-VPC claims.

Method: documentation only; no commands were run.
