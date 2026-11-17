---
id: computing-software.systems-network-administration.network-design.blocked-ports-and-services
name: blocked-ports-and-services
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-services, blocked-ports, firewall-troubleshooting, port-testing, path-filtering]
level: practitioner
status: docs-checked
description: "Find where a port or service is blocked along the path: telling closed from filtered, testing from both ends, host firewalls, ACLs, ISP blocks, and packet captures."
sources:
  - https://nmap.org/book/man-port-scanning-basics.html
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection
  - https://man7.org/linux/man-pages/man8/ss.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blocked ports and services

## Closed vs filtered
| Result | Meaning |
|---|---|
| Connection refused (RST) | host reachable, nothing listening (or a firewall rejecting with RST) |
| Timeout | packets dropped somewhere: host firewall, network ACL, security group, ISP block, routing |
| ICMP unreachable (administratively prohibited) | a firewall/router explicitly rejecting |

## Work from the server outward
1. Is the service listening, on which address?
   `ss -tlnp` lists listening TCP sockets with their processes (ss(8)). Bound to
   127.0.0.1 only means nothing remote will work.
2. Local test on the server: connect to the service from the server itself.
3. Host firewall: list the active rules with the platform's own firewall tool.
4. Same-subnet client, then remote subnet, then across firewalls/internet.

## Tools
```
Test-NetConnection 10.0.0.5 -Port 443      # Windows: TcpTestSucceeded True or False
```
On other systems use a TCP connect test, a traceroute that probes the service port over TCP, and a
packet capture on the server to see whether the SYN arrives. Nmap reports open, closed and
filtered states.
SYN arrives at the server but no SYN-ACK leaves -> host firewall or app. SYN never arrives -> network
path. SYN-ACK leaves but the client never sees it -> return path / asymmetric routing / stateful device.

## Common blockers
Cloud security groups/NACLs, ISP blocks on common ports,
guest Wi-Fi policies, corporate proxies requiring explicit configuration, IPS signatures.

## Verify
- [ ] The blocking hop is identified with evidence (capture or log entry), fixed with a scoped rule, and the test repeated from the original client.

## Checked

- Date: 2026-10-28
- Confirmed: Nmap port states (open, closed, filtered); Test-NetConnection -Port and TcpTestSucceeded; ss lists listening sockets (cited pages).
- Removed: specific ISP-blocked port numbers, ICMP type and code, Get-NetTCPConnection, nft, firewall-cmd, nc, tcptraceroute, tcpdump and curl invocations (not in the cited pages).

Method: documentation only; no commands were run.
