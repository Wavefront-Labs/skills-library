---
id: computing-software.cloud-infrastructure-engineering.docker.container-networking
name: container-networking
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, container-networking, docker-network, bridge-network, user-defined-bridge, docker0, embedded-dns, 127-0-0-11, host-network, none-network, macvlan, ipvlan, overlay-network, port-publishing, iptables, docker-user-chain, ufw-bypass, host-docker-internal, network-namespace, nsenter, mtu, ipv6, daemon-json, default-address-pools, bip, subnet-conflict, vpn, netshoot, podman-networking]
level: practitioner
status: docs-checked
description: "Understand and debug Docker networking: default vs user-defined bridges, embedded DNS, port publishing and the iptables/UFW bypass, host/macvlan/overlay drivers, subnet clashes with VPNs, MTU."
sources: ["https://docs.docker.com/engine/network/", "https://docs.docker.com/engine/network/drivers/bridge/", "https://docs.docker.com/engine/network/packet-filtering-firewalls/", "https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file", "https://github.com/nicolaka/netshoot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker container networking — how packets get in, out and between

**Goal:** containers find each other by name, only the ports you mean are reachable from
outside, Docker's subnets do not clash with your VPN, and you can trace a broken connection
hop by hop. Kubernetes networking is a different model — see
`computing-software.cloud-infrastructure-engineering.kubernetes.k8s-networking-and-ingress`.

## 1. Drivers
| Driver | What it is | Use |
|---|---|---|
| `bridge` (default `docker0`) | NAT'd private subnet on the host | legacy; **no DNS by container name** |
| user-defined bridge | `docker network create app` | the normal choice: name DNS, isolation per network |
| `host` | shares the host's network namespace | max performance, no port mapping, no isolation (on Docker Desktop 4.34+ host networking is an opt-in setting) |
| `none` | loopback only | batch jobs that must not touch the network |
| `macvlan` / `ipvlan` | container gets an IP on the physical LAN | legacy apps expecting a LAN address; host-to-container traffic needs extra setup |
| `overlay` | VXLAN across hosts (Swarm) | multi-host Swarm services |

Compose creates a user-defined bridge `<project>_default` automatically, which is why
service names resolve there.

## 2. DNS
- On user-defined networks Docker runs an embedded DNS server at `127.0.0.11` inside each
  container: service/container names and `--network-alias` resolve; other queries forward
  to the host's resolvers.
- The default bridge gets a copy of the host's `/etc/resolv.conf` (loopback nameservers removed). `--link` on the default bridge is deprecated (a warning from Engine 29.6, removal scheduled for 30.0) - do not use it.
- If no usable nameserver is left, Docker falls back to `8.8.8.8` and `8.8.4.4`, which breaks internal/split DNS. On a host whose only nameserver is the systemd-resolved stub `127.0.0.53`, Docker reads `/run/systemd/resolve/resolv.conf` instead for default-bridge containers. Set
  `"dns": [...]` in `/etc/docker/daemon.json` or `--dns` when in doubt.

## 3. Publishing ports
- `-p 8080:80` publishes on **all host interfaces** (0.0.0.0 and `::`). Use
  `-p 127.0.0.1:8080:80` for local-only.
- `EXPOSE` is documentation only; it publishes nothing.
- Published ports are handled in the `nat` table before the host's `INPUT` rules, so **UFW rules do not block them**. Filter in the
  `DOCKER-USER` chain, bind to localhost, or don't publish. (Docker 29.0.0 added an experimental nftables backend that has no `DOCKER-USER` chain and cannot be enabled in Swarm mode; see the packet-filtering and nftables pages.)
- Container-to-container traffic on the same network needs no publishing at all.

## 4. Reaching the host and the outside
- From a container to the host: `host.docker.internal` works on Docker Desktop; on Linux add
  `--add-host=host.docker.internal:host-gateway` (Compose: `extra_hosts`).
- Outbound traffic is SNAT'd to the host IP (masquerade); remote firewalls see the host.
- Connecting a container to two networks (`docker network connect`) is how you join a
  front-end network and a back-end network without exposing the DB to the proxy's network.
- `--internal` networks have no outbound route — good for databases that should never call out.

## 5. Subnet clashes and MTU
- Docker allocates 172.17.0.0/16 then other 172.x/192.168.x ranges per network; if they
  overlap your VPN or office LAN, hosts become unreachable from containers (or the host loses
  routes). Fix in `daemon.json`:
```json
{ "bip": "10.200.0.1/24",
  "default-address-pools": [{"base": "10.201.0.0/16", "size": 24}] }
```
  then restart the daemon and recreate the networks.
- MTU: inside a VPN or cloud overlay with MTU < 1500, large TLS handshakes or `git clone`
  hang while small requests work. Set `"mtu": 1400` (or the right value) in `daemon.json` or
  `--opt com.docker.network.driver.mtu=1400` per network.

## 6. Debugging routine
```bash
docker network ls && docker network inspect app        # subnet, attached containers, IPs
docker inspect -f '{{json .NetworkSettings.Networks}}' <CONTAINER>
docker run --rm -it --network container:<CONTAINER> nicolaka/netshoot   # share its netns
  # inside: dig api; curl -v http://api:8080; ss -tlnp; tcpdump -i eth0 port 8080
sudo iptables -t nat -L DOCKER -n -v; sudo iptables -L DOCKER-USER -n -v
```
Common root causes: app listening on `127.0.0.1` inside the container (must bind
`0.0.0.0`), containers on different networks, wrong port (container port vs published
port), or DNS falling back to the default bridge.

## Gotchas
- Inside a container, `localhost` is the container itself, never the host or another service.
- Restarting a container can change its IP; always address by name.
- Docker Desktop runs containers in a VM, so `--network host` and host-gateway semantics
  differ from Linux.
- Rootless Docker networking differs from rootful Docker; see the rootless documentation before relying on this page there.
- Setting `"iptables": false` prevents Docker creating most of its firewall rules: containers lose masquerading (no internet) while all their ports become reachable from the local network, so it is not recommended.

## Verify
- [ ] Services reach each other by name on a user-defined network.
- [ ] `ss -tlnp` on the host shows only intended published ports, bound to intended addresses.
- [ ] An external scan (`nmap` from another machine) cannot reach a port you "firewalled" with UFW alone.
- [ ] Docker subnets do not overlap VPN/LAN ranges (`ip route` with VPN connected).
- [ ] A large download from inside a container completes over the VPN (MTU OK).

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the networking overview (drivers, embedded DNS 127.0.0.11, default address pools, `--internal`), port publishing (default bind to all addresses), packet-filtering (ufw bypass, `iptables: false` effects), the legacy links page (default-bridge `--link` deprecation, removal in 30.0), the nftables page (29.0.0, experimental, no Swarm) and, for the resolv.conf handling, the moby source `daemon/libnetwork/internal/resolvconf` plus the daemon troubleshooting page (8.8.8.8/8.8.4.4 fallback). Removed the claim that UFW/firewalld both fail to filter (only ufw is documented), Podman/slirp4netns details and the statement about existing networks keeping old subnets.

Method: documentation only; no commands were run.
