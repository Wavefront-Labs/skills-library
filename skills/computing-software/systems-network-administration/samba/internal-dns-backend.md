---
id: computing-software.systems-network-administration.samba.internal-dns-backend
name: internal-dns-backend
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, internal-dns-backend, samba-internal, dns-forwarder, allow-dns-updates, dns]
level: practitioner
status: docs-checked
description: "Configure the Samba internal DNS server: dns forwarder, dynamic update policy, known limitations, and diagnosing port 53 conflicts."
sources:
  - https://wiki.samba.org/index.php/Samba_Internal_DNS_Back_End
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# internal dns backend
Select it at provision/join time with `--dns-backend=SAMBA_INTERNAL`. Recommended for simple DNS setups; it answers only the AD zones.

Forwarding (smb.conf `[global]`):
`dns forwarder = 8.8.8.8`
Default is none. Samba 4.5+ accepts several space-separated IPs (the smb.conf example includes IPv6 and a port: `[2001:db8:1:2::1]:54`). Without a forwarder, non-AD names fail.

Dynamic updates: `allow dns updates` defaults to `secure only` (Kerberos-signed). Other values: `disabled`, `nonsecure`.

Not supported by the internal server:
- caching resolver
- recursive queries (it can only forward)
- TSIG shared-key signatures
- stub zones
- zone transfers
- round-robin among DCs

Troubleshooting: look for `Failed to listen on 127.0.0.1:53 - NT_STATUS_ADDRESS_ALREADY_ASSOCIATED` in the logs, then find the other listener with `netstat -tulpn | grep ":53"` (the wiki example is dnsmasq). Stop and disable it at boot, restart Samba.

Records are managed with `samba-tool dns` (see samba-tool-dns).

## Checked

2026-11-04. Confirmed against the Samba wiki Internal DNS Back End page: recommended for simple setups, the limitations list, secure Kerberos updates by default, forwarder needed for non-AD names, multiple IPs from Samba 4.5, the port 53 conflict log line and netstat check with the dnsmasq example. Confirmed against smb.conf(5): dns forwarder default empty and its IPv6/port example, allow dns updates values and default secure only. Reworded the IPv6 example to match smb.conf.
Method: documentation only; no commands were run.
