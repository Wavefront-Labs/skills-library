---
id: computing-software.cloud-infrastructure-engineering.docker.iptables-legacy-vs-iptables-nft
name: iptables-legacy-vs-iptables-nft
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, iptables, iptables-legacy, iptables-nft, nftables, update-alternatives, firewall]
level: advanced
status: docs-checked
description: "Fix container networking broken by mixed iptables backends: identify legacy vs nft, switch with update-alternatives, keep Docker, firewalld, ufw and kube-proxy aligned."
sources: ["https://docs.docker.com/engine/network/packet-filtering-firewalls/", "https://docs.docker.com/engine/network/firewall-nftables/", "https://wiki.debian.org/nftables"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iptables-legacy vs iptables-nft

The `iptables` command exists in two implementations:
- **iptables-legacy**: writes the old x_tables kernel tables.
- **iptables-nft**: same syntax, writes nftables tables (`table ip filter` etc.).

Rules written by one are invisible to the other. If Docker uses one and your firewall or
another tool uses the other, packets traverse both rule sets in unexpected order and published
ports or outbound traffic break.

## Identify
```bash
iptables --version                        # "(nf_tables)" or "(legacy)"
update-alternatives --display iptables    # Debian/Ubuntu
sudo iptables-legacy -S | grep -c DOCKER
sudo iptables-nft -S | grep -c DOCKER
sudo nft list ruleset | grep -c DOCKER
```
Rules present in **both** legacy and nft = a mixed setup.

## Align everything on one backend (Debian's wiki: nft has been the default since Debian 10)
```bash
sudo update-alternatives --set iptables /usr/sbin/iptables-nft
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-nft
# flush leftovers from the other backend, then restart services that write rules
sudo iptables-legacy -F; sudo iptables-legacy -t nat -F; sudo iptables-legacy -X
sudo systemctl restart docker
```

## Tools that must agree
- Docker (via the `iptables` binary it finds, or its experimental native nftables backend, available from Docker 29.0.0 with
  `"firewall-backend": "nftables"` and not usable in Swarm mode).
- firewalld, ufw and any other tool that writes rules on the same host.

## Gotchas
- With Docker's nftables backend there is no `DOCKER-USER` chain; customisations must be rewritten as nftables rules (see the nftables backend skill).
- After switching, re-test published ports from outside the host and outbound DNS from a
  container.

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed the Debian `update-alternatives --set iptables|ip6tables ... -nft|-legacy` procedure, the nft default since Debian 10 and the advice against mixing rulesets on the Debian nftables wiki, and the Docker nftables backend facts (29.0.0, experimental, no Swarm, no `DOCKER-USER`) on the Docker nftables page. Removed the kube-proxy/CNI, old-image and RHEL claims and the Kubernetes blog source (no longer needed).

Method: documentation only; no commands were run.
