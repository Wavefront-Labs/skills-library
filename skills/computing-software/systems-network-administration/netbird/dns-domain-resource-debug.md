---
id: computing-software.systems-network-administration.netbird.dns-domain-resource-debug
name: dns-domain-resource-debug
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, domain-resources, dns-forwarder, port-22054, routing-peer-debug]
level: advanced
status: docs-checked
description: "Debug NetBird domain-based network resources: test reachability from the routing peer, query its DNS forwarder on port 22054, check routes and clear caches."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/dns/troubleshooting.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When a domain resource does not work, test in this order.

1. Routing peer reaches the service: `nc -vz <host> <port>` for TCP, `nc -vz -u <host> <port>` for UDP.
2. Routing peer DNS forwarder answers on port 22054:
```
nslookup -timeout=1 -port=22054 <domain> <routing-peer-ip>
```
3. Trigger the resource through the client's local forwarder (a `100.x.255.254` style address on macOS/Windows), then verify:
```
nslookup <domain> <local-forwarder-ip>
netbird networks ls
ip route show table all
```
Grep the route table for the resource's address.
4. Clear all caches: `sudo netbird service restart`.

Notes:
- Port 5353 can conflict with other software on older clients; update to 0.59.10 or later (forwarder uses 22054).
- `ping` needs an ICMP policy; when testing through a routing peer prefer a TCP check such as `Test-NetConnection <host> -Port <port>` on Windows.
- Domain resources resolve only A/AAAA records.

## Checked

2026-11-04: read the DNS troubleshooting page (Debugging Access to Domain Resources, Issue 8 and the ICMP note). Confirmed the test order, the nc and nslookup commands, port 22054 and the 0.59.10 recommendation, the 100.x.255.254 forwarder address on macOS and Windows, the service restart cache purge and the A/AAAA-only limit. Nothing removed.

Method: documentation only; no commands were run.
