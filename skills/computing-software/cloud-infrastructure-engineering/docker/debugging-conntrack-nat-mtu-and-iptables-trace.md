---
id: computing-software.cloud-infrastructure-engineering.docker.debugging-conntrack-nat-mtu-and-iptables-trace
name: debugging-conntrack-nat-mtu-and-iptables-trace
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, network-troubleshooting, network-debugging, conntrack, nat-table, iptables-trace, nft-trace, mtu-mismatch, path-mtu, iptables]
level: sme
description: "Trace container packets through Docker's NAT with conntrack, iptables TRACE and nft monitor trace, and fix MTU mismatches that hang TLS and large transfers."
sources: ["https://docs.docker.com/engine/network/packet-filtering-firewalls/", "https://manpages.debian.org/conntrack.8", "https://wiki.nftables.org/wiki-nftables/index.php/Ruleset_debug/tracing", "https://docs.docker.com/engine/network/drivers/bridge/#options"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Debugging conntrack, NAT, MTU and rule tracing

## See Docker's NAT
```sh
sudo iptables -t nat -L DOCKER -n -v --line-numbers       # DNAT for published ports
sudo iptables -t nat -L POSTROUTING -n -v                 # MASQUERADE for outbound
sudo iptables -L DOCKER-USER -n -v; sudo iptables -L FORWARD -n -v
sudo nft list ruleset | less                              # iptables-nft hosts show the same rules here
```
Counters (`-v`) that don't increase tell you the packet never reached that rule.

## conntrack
```sh
sudo conntrack -L -p tcp --dport 8080                  # tracked flows to a published port
sudo conntrack -L -d 172.18.0.5
sudo conntrack -E -p udp --dport 53                    # live events
sudo conntrack -D -p udp --dport 514                   # delete stale UDP entries
sudo sysctl net.netfilter.nf_conntrack_count net.netfilter.nf_conntrack_max
```
Classic issues:
- **Stale UDP entries**: a syslog/DNS container restarts with a new IP but the old flow
  keeps DNATing to the dead IP until timeout. Delete the entries.
- **Table full**: `nf_conntrack: table full, dropping packet` in dmesg -> raise
  `nf_conntrack_max` or reduce short-lived connections.

## Rule tracing
```sh
# iptables-legacy
sudo iptables -t raw -A PREROUTING -p tcp --dport 8080 -j TRACE
sudo dmesg -w | grep TRACE        # or: xtables-monitor --trace on iptables-nft
sudo iptables -t raw -D PREROUTING -p tcp --dport 8080 -j TRACE
# nftables
sudo nft add table inet trace_debug
sudo nft 'add chain inet trace_debug pre { type filter hook prerouting priority -301; }'
sudo nft add rule inet trace_debug pre tcp dport 8080 meta nftrace set 1
sudo nft monitor trace
sudo nft delete table inet trace_debug
```
Output lists each table/chain/rule the packet hits and the verdict - pinpoints which DROP wins.

## MTU mismatches
Symptoms: small requests work, TLS handshakes or large downloads hang (`apt-get update`
stalls), especially on VPNs, cloud overlays,
or nested Docker.
```sh
ip link show eth0 | grep mtu                                # host uplink
docker run --rm alpine ip link show eth0                    # container MTU
docker run --rm alpine ping -M do -s 1472 -c 2 1.1.1.1      # 1472+28=1500; lower until it passes
```
Fix by matching the smallest path MTU:
```json
{ "mtu": 1450 }
```
daemon.json applies to the default bridge; user networks: `docker network create -o com.docker.network.driver.mtu=1450 net`;
Compose `driver_opts: { com.docker.network.driver.mtu: 1450 }`. Overlay networks need a lower MTU than the underlay to leave room for VXLAN encapsulation.

## Verify
After fixes, `curl -o /dev/null https://large-file` completes; TRACE shows ACCEPT on the
expected chain; conntrack shows flows to the current container IP.

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed the `conntrack` commands (`-L`, `-E`, `-D` with `-p`, `--dport`, `-d`) in the conntrack man page, the nftables trace recipe (`meta nftrace set 1`, `nft monitor trace`, prerouting base chain at priority -301 as in the nftables wiki), Docker's `nat` table `DOCKER` chain and `DOCKER-USER`/`FORWARD` chains on the packet-filtering page, and the MTU options (`com.docker.network.driver.mtu`, daemon `mtu`) on the bridge page. Removed the unconfirmed GCP MTU figure, the DinD symptom and the VXLAN byte count.

Method: documentation only; no commands were run.
