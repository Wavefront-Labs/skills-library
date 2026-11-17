---
id: computing-software.cloud-infrastructure-engineering.docker.nftables-backend-masquerade-and-gateway-modes
name: nftables-backend-masquerade-and-gateway-modes
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, nftables, nftables-backend, firewall-backend, ip-masq, masquerade, gateway-mode, nat-unprotected, routed-networks, bridge-network]
level: sme
description: "Control how bridge networks reach the world: enable_ip_masquerade, gateway_mode nat, nat-unprotected and routed, and Docker's nftables firewall backend."
sources: ["https://docs.docker.com/engine/network/packet-filtering-firewalls/", "https://docs.docker.com/engine/network/drivers/bridge/#options", "https://docs.docker.com/engine/network/firewall-nftables/", "https://docs.docker.com/engine/network/port-publishing/#gateway-modes"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nftables backend, masquerade and gateway modes

## IP masquerade
Default: outbound traffic from a bridge network is SNATed (MASQUERADE) to the host's IP.
```sh
docker network create -o com.docker.network.bridge.enable_ip_masquerade=false nonat
```
Without masquerade, containers egress with their own IPs - only useful when the upstream
router has a route back to the bridge subnet. Daemon-wide default bridge: `"ip-masq": false`.
Pin a source IP for egress instead: `-o com.docker.network.host_ipv4=198.51.100.10` (masquerading must stay enabled for this option to take effect).

## Gateway modes
`-o com.docker.network.bridge.gateway_mode_ipv4=<mode>` (and `_ipv6`):
| Mode | Behaviour |
|---|---|
| `nat` (default) | NAT and masquerading; only published ports reachable; direct routing to container IPs not allowed |
| `nat-unprotected` | NAT as above but no port filtering: unpublished ports are also reachable by direct routing (kept for legacy default behaviour) |
| `routed` | no NAT or masquerading: containers use their own addresses; firewall rules still accept only published ports |
| `isolated` | only with `--internal`; no address is assigned to the bridge, so the host cannot reach the network |

```sh
docker network create --subnet 192.0.2.0/24 \
  -o com.docker.network.bridge.gateway_mode_ipv4=routed routednet
docker run -d --network routednet -p 80 nginx      # reachable at its own IP:80 from routed peers
```
`routed` needs remote hosts to have a route to the container network via the Docker host (static routes, BGP, or hosts on the same L2 segment). It suits IPv6 with global addresses. By default remote hosts cannot reach container IPs directly in `nat` networks; the daemon option `allow-direct-routing` and the network option `com.docker.network.bridge.trusted_host_interfaces` allow direct routing to published ports, while `nat-unprotected` opens all ports (use only on trusted networks).

## nftables firewall backend
Docker 29.0.0 introduced experimental support for an nftables firewall backend (options and behaviour may change). It cannot be enabled while the daemon is in Swarm mode, because overlay network rules have not been migrated from iptables:
```json
{ "firewall-backend": "nftables" }
```
- Docker creates two tables, `ip docker-bridges` and `ip6 docker-bridges`; do not modify them.
- There is no `DOCKER-USER` chain: add your rules in separate tables with base chains of the same type and hook as Docker's, using the base-chain priority to order them.
- Docker does not enable IP forwarding itself with this backend and reports an error when forwarding is needed but disabled (`--ip-forward=false` skips the check); it also creates no default drop policy.
- Many hosts already run iptables-nft (iptables syntax on nf_tables): Docker's iptables rules
  appear in `nft list ruleset` as `table ip filter` etc. - that is not the native backend.

## Verify
```sh
docker network inspect routednet -f '{{json .Options}}'
sudo nft list tables                      # docker-bridges tables with the nftables backend
docker run --rm --network nonat alpine wget -qO- ifconfig.me   # shows container IP or pinned host IP as configured
```

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the port publishing page (masquerade options, `host_ipv4`, gateway modes and their semantics, `isolated` requiring `--internal`, `allow-direct-routing`, `trusted_host_interfaces`) and the nftables page (Docker 29.0.0, experimental, no Swarm mode, table names, no `DOCKER-USER`, forwarding behaviour). Removed unconfirmed version labels on individual gateway modes and the Engine 28 hardening claim.

Method: documentation only; no commands were run.
