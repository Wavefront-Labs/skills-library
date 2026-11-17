---
id: computing-software.systems-network-administration.network-design.ports-protocols-and-ephemeral-ranges
name: ports-protocols-and-ephemeral-ranges
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, well-known-ports, port-numbers, ip-protocol-numbers, ephemeral-ports, port-exhaustion, snat-port-exhaustion, secure-protocols, iana, services-file, firewall-rules, flow-matrix]
level: practitioner
status: verified
description: "Working reference for ports and IP protocol numbers, secure replacements for legacy protocols, OS ephemeral port ranges and diagnosing source-port exhaustion on NAT and proxies."
sources:
  - https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
  - https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
  - https://datatracker.ietf.org/doc/html/rfc6056
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ports, protocols and ephemeral ranges

## IP protocol numbers (not ports)
ICMP 1, IGMP 2, TCP 6, UDP 17, GRE 47, ESP 50, AH 51, ICMPv6 58, EIGRP 88, OSPF 89, PIM 103,
VRRP 112, SCTP 132. Firewall rules for GRE/ESP/OSPF/VRRP must use the protocol, not a port.

## Ports you must know (every row checked against the IANA service-names and port-numbers registry; 465/tcp is `submissions` since RFC 8314)
| Service | Port | Secure replacement |
|---|---|---|
| FTP | 20/21 TCP | SFTP (22) or FTPS (990/explicit 21) |
| SSH/SFTP/SCP | 22 TCP | n/a |
| Telnet | 23 TCP | SSH |
| SMTP | 25 TCP (relay), 587 submission (STARTTLS), 465 (implicit TLS) | 587/465 with TLS |
| DNS | 53 UDP/TCP | DoT 853, DoH 443 |
| DHCP | 67/68 UDP (v6: 546/547) | n/a |
| TFTP | 69 UDP | SCP/HTTPS |
| HTTP/HTTPS | 80 / 443 TCP (443 UDP for QUIC) | HTTPS |
| NTP | 123 UDP | NTS (4460 TCP for key exchange) |
| SNMP | 161 / 162 UDP | SNMPv3 |
| LDAP / LDAPS | 389 / 636 TCP | LDAPS or StartTLS |
| SMB | 445 TCP | SMB3 with encryption |
| Syslog | 514 UDP, 6514 TLS | TLS syslog |
| RDP | 3389 TCP/UDP | behind VPN/gateway |
| SQL Server / MySQL / PostgreSQL | 1433 / 3306 / 5432 | TLS-enabled |
| SIP | 5060 / 5061 TLS | SIP-TLS + SRTP |
| IKE / NAT-T | 500 / 4500 UDP | n/a |
| RADIUS | 1812/1813 UDP | RadSec 2083 TCP |
| TACACS+ | 49 TCP (RFC 8907) | TACACS+ over TLS 1.3 (RFC 9887, TCP 300 `tacacss` in the IANA registry) |
| Kerberos | 88 | n/a |

## Ephemeral (source) ports
| OS | Default range |
|---|---|
| IANA recommendation (RFC 6335) | 49152-65535 |
| Linux | 32768-60999 (`sysctl net.ipv4.ip_local_port_range`) |
| Windows Vista+ | 49152-65535 (ran `netsh int ipv4 show dynamicport tcp`: start 49152, 16384 ports) |
Firewalls between clients and servers only need the server port inbound; stateful inspection
handles the return. Stateless ACLs need the ephemeral range back (or `established`).

## Port exhaustion
Each (source IP, destination IP, destination port, protocol) can only use ~64k source ports at
once; TIME_WAIT holds them for a minute or more (OS dependent). Busy proxies, NAT gateways (cloud NAT has per-IP limits)
and load balancers hit it:
- Symptoms: intermittent connection failures to one popular destination, `EADDRNOTAVAIL`,
  "SNAT port exhaustion" (Azure Load Balancer outbound docs) and the port-allocation error metrics that cloud NAT gateways expose (look up the metric name in the provider's docs).
- Check: `ss -s` and `ss -tan state time-wait | wc -l` (Linux), `netstat -ano | find /c "TIME_WAIT"` (Windows; ran).
- Fix: connection pooling/keep-alive, more NAT source IPs, widen the range, avoid
  `tcp_tw_recycle` (absent from current kernel docs); `tcp_tw_reuse` (kernel doc: 0 off, 1 global, 2 loopback only, default 2) can help outbound clients, but the doc says not to change it without expert advice.

## Verify
- [ ] Firewall flow matrix lists protocol + port for every rule, with secure variants preferred.
- [ ] NAT/proxy port utilisation monitored with an alert well below the limit.
