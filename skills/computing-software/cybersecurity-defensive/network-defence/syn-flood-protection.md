---
id: computing-software.cybersecurity-defensive.network-defence.syn-flood-protection
name: syn-flood-protection
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ddos-mitigation, syn-cookies, syn-flood, tcp-backlog, sysctl, firewall-syn-proxy, connection-limits, protocol-attacks]
level: practitioner
status: docs-checked
description: "Mitigate SYN floods and other protocol attacks on hosts and edges: SYN cookies, backlog tuning, SYN proxy on firewalls and load balancers, and monitoring."
sources: ["https://datatracker.ietf.org/doc/html/rfc4987", "https://docs.kernel.org/networking/ip-sysctl.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SYN flood protection

**Goal:** half-open connection floods cannot fill connection tables on servers, firewalls or
load balancers and deny service to legitimate clients.

## Host (Linux)
```
sysctl -w net.ipv4.tcp_syncookies=1          # kernel default is 1 (needs CONFIG_SYN_COOKIES)
sysctl -w net.ipv4.tcp_max_syn_backlog=4096
sysctl -w net.core.somaxconn=4096              # kernel default is 4096 since 5.4 (128 before)
sysctl -w net.ipv4.tcp_synack_retries=2      # fewer retries frees slots sooner
```
Persist in `/etc/sysctl.d/90-synflood.conf`. Applications must use a large listen backlog
too (the `backlog` argument of `listen()`).
SYN cookies encode connection state in the sequence number so no state is kept until the
handshake completes; the kernel documentation calls them a fallback facility that does not allow TCP extensions and is not meant to carry
legitimate load.

## Windows
See Microsoft's documentation for the TCP SYN attack protection of your Windows version.

## Network edge
- **SYN proxy or cookie features** on firewalls/load balancers complete the handshake on behalf of the server.
- Firewall flood protection: SYN, UDP, ICMP flood thresholds set from baseline traffic.
- Connection limits per source IP for public services.
- Upstream: cloud DDoS protection and scrubbing absorb large floods; host tuning only helps for small ones.

## Monitor
- `netstat -s | grep -i -E "SYNs to LISTEN|cookies"`, `ss -s`.
- Firewall session table utilisation; alert on a rising trend.

## Gotchas
- Stateful firewalls in front of servers often fail first: protect the firewall's session table.
- Overly aggressive thresholds block legitimate bursts (e.g. after an outage when all clients reconnect).
- Other protocol floods (UDP reflection/amplification, ACK floods) need different filters.

## Verify
- [ ] Lab test with a SYN flood tool against a test host shows cookies sent and service still responding.
- [ ] Zone protection thresholds documented with the baseline they came from.

## Checked
2026-10-28. Confirmed against official pages: tcp_syncookies, tcp_max_syn_backlog, tcp_synack_retries and somaxconn names and defaults, syncookies as a fallback with TCP-extension limits (Linux ip-sysctl docs); SYN cache and SYN cookie mitigations (RFC 4987).
Removed or rewritten: the Windows automatic-protection claim, NGINX backlog, vendor product list, SYNPROXY, nstat counter, kernel log string and the 70-80% figure; non-URL sources replaced.
Method: documentation only; no commands were run.
