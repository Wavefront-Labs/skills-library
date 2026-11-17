---
id: computing-software.systems-network-administration.samba.ad-dc-ports
name: ad-dc-ports
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, ad-dc-ports, firewall, port-usage, active-directory, kerberos, ldap]
level: intro
status: docs-checked
description: "List the TCP and UDP ports a Samba AD DC needs open: DNS, Kerberos, LDAP, SMB, RPC, Global Catalog and the dynamic RPC range."
sources:
  - https://wiki.samba.org/index.php/Samba_AD_DC_Port_Usage
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
  - https://www.samba.org/samba/docs/current/man-html/smbd.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ad dc ports
Open these on a Samba AD DC firewall:

| Service | Port | Protocol |
|---|---|---|
| DNS | 53 | tcp/udp |
| Kerberos | 88 | tcp/udp |
| NTP (only if running) | 123 | udp |
| End Point Mapper | 135 | tcp |
| NetBIOS name | 137 | udp |
| NetBIOS datagram | 138 | udp |
| NetBIOS session | 139 | tcp |
| LDAP | 389 | tcp/udp |
| SMB over TCP | 445 | tcp |
| Kerberos kpasswd | 464 | tcp/udp |
| LDAPS | 636 | tcp (when `tls enabled = yes`, the default) |
| Global Catalog | 3268 | tcp |
| Global Catalog SSL | 3269 | tcp (when `tls enabled = yes`, the default) |
| Dynamic RPC | 49152-65535 | tcp |

The dynamic range comes from the smb.conf parameter `rpc server dynamic port range` (default `49152-65535`, matching Windows Server 2008 and later); Samba before 4.7 used TCP 1024 to 1300. It covers RPC services without well-known ports such as LSA, SAM and Netlogon. DNS may be served by the internal DNS server or BIND9, and NTP applies only if configured and running on the DC. Services other than samba can open further ports.

smbd listens on 139 and 445 by default (the `-p` option and `ports` parameter).

## Checked
2026-11-04: port table, footnotes and the pre-4.7 range compared with the Samba AD DC Port Usage wiki page; the dynamic range default compared with the smb.conf man page; the smbd default ports compared with the smbd man page. Removed: a netstat verification line and a reachability tip the pages do not state.
Method: documentation only; no commands were run.
