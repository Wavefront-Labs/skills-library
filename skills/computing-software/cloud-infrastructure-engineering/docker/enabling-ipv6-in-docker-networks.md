---
id: computing-software.cloud-infrastructure-engineering.docker.enabling-ipv6-in-docker-networks
name: enabling-ipv6-in-docker-networks
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, ipv6, enable-ipv6, ipv6-daemon-json, fixed-cidr-v6, ula-subnet, ip6tables, ipv6-nat, dual-stack, ipv6-publish, compose-ipv6, ndp-proxy, ipv6-routed]
level: advanced
description: "Enable IPv6 on the default bridge and user networks with ULA or global prefixes, ip6tables NAT vs routed mode, dual-stack port publishing and IPv6 in Compose."
sources: ["https://docs.docker.com/engine/daemon/ipv6/", "https://docs.docker.com/reference/compose-file/networks/#enable_ipv6", "https://docs.docker.com/engine/network/port-publishing/", "https://docs.docker.com/engine/network/packet-filtering-firewalls/", "https://docs.kernel.org/networking/ip-sysctl.html"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enabling IPv6 in Docker networks

## User-defined network (most common)
```sh
docker network create --ipv6 --subnet fd00:dead:beef::/64 v6net
# or omit --subnet and let Docker allocate a subnet: docker network create --ipv6 v6net
docker run --rm --network v6net alpine ip -6 addr
```
- Use a **ULA** (`fd00::/8`, pick a random /48 per RFC 4193) with NAT66, or a **global**
  prefix routed to the host without NAT.
- `ip6tables` is enabled by default, giving IPv6 isolation and port mapping; it can be disabled.
- Without an IPv6 pool in `default-address-pools` and without `--subnet`, Docker allocates /64 ULA subnets.

## Default bridge
```json
{
  "ipv6": true,
  "fixed-cidr-v6": "fd00:1::/64",
  "default-address-pools": [
    { "base": "172.30.0.0/16", "size": 24 },
    { "base": "fd00:2::/48", "size": 64 }
  ]
}
```
`fixed-cidr-v6` is the default bridge's subnet; pools feed user networks. If you configure pools, keep the default IPv4 pools in the list as well as your IPv6 pool.

## Compose
```yaml
networks:
  app:
    enable_ipv6: true
    ipam:
      config:
        - subnet: 172.31.5.0/24
        - subnet: fd00:5::/64
```
With `enable_ipv6: true` and no IPv6 subnet, the network uses the daemon's default address pools (ULA if no IPv6 pool).

## Publishing dual-stack
`-p 8080:80` binds `0.0.0.0:8080` and `[::]:8080`. If the network has no IPv6, Docker still
accepts IPv6 connections on the host and maps them to the container's IPv4 address, but only while `userland-proxy` is true (the default).
`-p [::1]:8080:80` binds IPv6 loopback only.

## Routed IPv6 without NAT
With a global /64 routed to the host:
```sh
docker network create --ipv6 --subnet 2001:db8:1:2::/64 \
  -o com.docker.network.bridge.gateway_mode_ipv6=routed gv6
```
If the upstream router only does on-link neighbour discovery (no route to the host), make the
host answer NDP for container addresses: `sysctl net.ipv6.conf.eth0.proxy_ndp=1` and
`ip -6 neigh add proxy 2001:db8:1:2::5 dev eth0` per address (or `ndppd`).

## Gotchas
- `net.ipv6.conf.all.forwarding=1` disables router-advertisement acceptance on the host's
  uplink unless `accept_ra=2` is set - hosts using SLAAC lose their default route.
- IPv6 is only supported on Docker daemons running on Linux hosts.

## Verify
```sh
docker run --rm --network v6net alpine ping -6 -c2 2606:4700:4700::1111
curl -6 http://[::1]:8080/
sudo ip6tables -t nat -L POSTROUTING -n
```

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the IPv6 page (`--ipv6`, `--subnet`, default bridge `ipv6`/`fixed-cidr-v6`, `ip6tables` on by default, ULA allocation, pool configuration needing IPv4 pools too, Linux-only), the port publishing page (dual-stack publishing, IPv6-to-IPv4 mapping with `userland-proxy=true`, `gateway_mode_ipv6=routed` example) and the Linux ip-sysctl documentation (`accept_ra=2`, `proxy_ndp`). Removed unconfirmed engine-version gates and the Docker Desktop remark.

Method: documentation only; no commands were run.
