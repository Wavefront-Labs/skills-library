---
id: computing-software.cloud-infrastructure-engineering.docker.docker-user-chain-firewalld-and-iptables-false
name: docker-user-chain-firewalld-and-iptables-false
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, iptables, firewall, docker-user-chain, docker-user-rules, restrict-external-access, firewalld, firewalld-zone, docker-zone, iptables-false, ip-forward]
level: advanced
description: "Restrict who can reach published ports with DOCKER-USER rules, coexist with firewalld's docker zone, and what you must rebuild by hand if you set iptables false."
sources: ["https://docs.docker.com/engine/network/packet-filtering-firewalls/", "https://docs.docker.com/engine/network/firewall-iptables/", "https://docs.docker.com/engine/network/firewall-nftables/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DOCKER-USER, firewalld and iptables=false

Published ports are DNATed in `PREROUTING` and accepted in `FORWARD` before host INPUT
rules (ufw, plain iptables INPUT) ever see them. Filtering must happen in the FORWARD path.

## DOCKER-USER chain
Docker creates it as a placeholder for user rules that are processed before the `DOCKER-FORWARD` and `DOCKER` chains (rules appended to `FORWARD` run after Docker's). Put policy here:
```sh
EXT=eth0
# allow only the office range to published ports, drop the rest from outside
sudo iptables -I DOCKER-USER -i $EXT ! -s 203.0.113.0/24 -j DROP
# keep established return traffic working (insert above the DROP)
sudo iptables -I DOCKER-USER -m state --state RELATED,ESTABLISHED -j ACCEPT
# match the ORIGINAL destination port (after DNAT the dport is the container port)
sudo iptables -I DOCKER-USER -i $EXT -p tcp -m conntrack --ctorigdstport 5432 --ctdir ORIGINAL -j DROP
```
- Insert rules with `-I` so they land before the rules Docker adds.
- Packets sent to a container's own IP (direct routing) are dropped in the `raw` table before `DOCKER-USER`, so a rule there cannot allow them; use `com.docker.network.bridge.trusted_host_interfaces` or the daemon option `allow-direct-routing`.
- After DNAT, `-d` is the container IP and `--dport` the container port; use conntrack
  `--ctorigdst/--ctorigdstport` to match what clients connected to.
- With the experimental nftables backend (Docker 29.0.0) there is no `DOCKER-USER` chain; the equivalent is your own nft table with a base chain of the same type and hook, ordered by priority.

## firewalld
- With `iptables`/`ip6tables` enabled and firewalld running, Docker creates a firewalld zone named `docker` with target
  `ACCEPT`, puts all its bridge interfaces in it, and adds a `docker-forwarding` policy allowing forwarding from any zone to the `docker` zone.
```sh
firewall-cmd --get-active-zones           # docker zone lists docker0/br-* interfaces
firewall-cmd --zone=docker --list-all
```

## "iptables": false
```json
{ "iptables": false, "ip6tables": false }
```
Docker then skips most of its iptables/nftables rules, and it is not possible to stop it creating all firewall rules. Without replacement rules, containers in bridge networks cannot reach the internet by masquerading, while all their ports are reachable from the local network. You would have to provide yourself:
- IP forwarding and masquerading for each bridge subnet,
- DNAT for every published port,
- inter-network isolation.
Not recommended for most users. Prefer DOCKER-USER, or `--network host` behind a host
firewall for the few services that need it (Docker creates no firewall rules for host networking).

## Verify
From an external host outside the allowed range: `nc -zv host 8080` times out; from inside:
connects. `sudo iptables -L DOCKER-USER -n -v` counters increase on the DROP rule.

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the packet-filtering page (firewalld `docker` zone and `docker-forwarding` policy, `iptables: false` effects, no rules for host networking), the iptables page (`DOCKER-USER` role and ordering, conntrack `--ctorigdst/--ctorigdstport`, `-I DOCKER-USER ... ! -s ... -j DROP`, `RELATED,ESTABLISHED` accept rule, raw-table drop of direct-routed packets) and the nftables page (29.0.0, experimental, no `DOCKER-USER`). Removed the firewalld StrictForwardPorts claim and its source (the cited firewalld.org page returned 404), the Docker 20.10 version gate, the reload behaviour, persistence advice and the docker-proxy remark.

Method: documentation only; no commands were run.
