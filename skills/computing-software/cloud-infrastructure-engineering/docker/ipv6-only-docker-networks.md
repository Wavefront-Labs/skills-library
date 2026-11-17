---
id: computing-software.cloud-infrastructure-engineering.docker.ipv6-only-docker-networks
name: ipv6-only-docker-networks
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, ipv6, ipv6-only, network-create, nat64, dns64, compose-ipv6]
level: advanced
status: docs-checked
description: "Create IPv6-only bridge networks with --ipv4=false --ipv6, publish ports, reach IPv4-only services through NAT64/DNS64, and handle images that assume IPv4 localhost."
sources: ["https://docs.docker.com/engine/daemon/ipv6/", "https://docs.docker.com/engine/network/", "https://docs.docker.com/reference/cli/docker/network/create/", "https://docs.docker.com/reference/compose-file/networks/#enable_ipv4", "https://docs.docker.com/engine/network/port-publishing/", "https://www.rfc-editor.org/rfc/rfc6052"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6-only Docker networks

Docker can create networks with IPv4 address assignment disabled (`--ipv4=false`, Compose `enable_ipv4: false`). The Engine API field `EnableIPv4` arrived in API 1.48 (Engine 28.0), where setting it to `false` required experimental mode; the current CLI reference lists the flag without that note.

## Create
```bash
docker network create --ipv4=false --ipv6 v6only                        # ULA subnet from the default pools
docker network create --ipv4=false --ipv6 --subnet 2001:db8:1::/64 v6pub
docker run --rm --network v6only alpine ip -6 addr
```
Compose:
```yaml
networks:
  v6only:
    enable_ipv4: false
    enable_ipv6: true
    ipam:
      config: [{ subnet: "fd00:db8:10::/64" }]
```
Without `--subnet` and without IPv6 entries in daemon.json `default-address-pools`, Docker allocates /64 Unique Local Address subnets; add IPv6 pools to control the ranges.

## Publishing ports
```bash
docker run -d --network v6only -p '[::]:8080:80' nginx
curl -g 'http://[::1]:8080/'
```
With the default `nat` gateway mode Docker sets up NAT and masquerading for IPv6. For routed global
addresses use `-o com.docker.network.bridge.gateway_mode_ipv6=routed` and route the prefix to
the host.

## Reaching IPv4-only services
An IPv6-only container cannot reach IPv4 addresses directly. Options:
- **DNS64 + NAT64** on the network (for example a provider NAT64 gateway): AAAA records are synthesised from the well-known prefix `64:ff9b::/96` (RFC 6052).
- Keep a dual-stack network for egress-heavy services.

## Application gotchas
- Apps binding `0.0.0.0` listen on IPv4 only; on an IPv6-only network they are unreachable.
  Bind `::` (most runtimes then accept both).
- Health checks using `127.0.0.1` fail; use `localhost` (resolves `::1` in most images) or `[::1]`.

## Verify
```bash
docker network inspect v6only -f '{{.EnableIPv4}} {{.EnableIPv6}} {{json .IPAM.Config}}'
docker run --rm --network v6only alpine sh -c 'ip -4 addr; ping -6 -c1 2001:4860:4860::8888'
```

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed `--ipv4=false`/`--ipv6` in the networking overview and `network create` reference, `enable_ipv4` in the Compose reference, ULA allocation when no IPv6 pools exist (IPv6 page), `nat`/`routed` gateway modes (port publishing page), the API 1.48 `EnableIPv4` entry in the Engine API changelog, and the 64:ff9b::/96 prefix in RFC 6052. Corrected the claim that IPv6 pools are required for allocation (ULA is used by default); removed JVM/Alpine and build-network claims.

Method: documentation only; no commands were run.
