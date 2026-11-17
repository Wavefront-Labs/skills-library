---
id: computing-software.systems-network-administration.network-design.incorrect-dns-server-settings
name: incorrect-dns-server-settings
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-services, incorrect-dns, dns-client, resolver-settings, split-dns]
level: practitioner
status: docs-checked
description: "Troubleshoot clients pointing at the wrong DNS servers: symptoms, checking effective resolvers, the DHCP DNS option and RDNSS, VPN and public resolver pitfalls."
sources:
  - https://man7.org/linux/man-pages/man1/resolvectl.1.html
  - https://www.rfc-editor.org/rfc/rfc8106
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Incorrect DNS server settings

## Symptoms
- Internet names work but internal names (`fileserver.corp.local`, AD) fail -> client uses a public
  resolver (8.8.8.8) instead of internal DNS.
- Domain join/GPO/Kerberos failures, "no logon servers" -> DC SRV records not resolvable.
- Everything slow to start then works -> first listed DNS server dead, falling back after timeout.
- Ping by IP works, by name fails.

## Check effective resolvers
```
resolvectl status                   # Linux systemd-resolved: per-link servers and domains
```
On Windows and macOS use the OS's own tool to list the DNS servers per adapter, then query the
suspect resolver directly and compare it with the intended one.

## Where wrong settings come from
- The DHCP DNS-server option in the scope (typo, old server), or a rogue DHCP server (home router plugged in).
- Static settings on the adapter left from a past setup.
- IPv6 RA RDNSS / DHCPv6 handing out a different resolver that clients prefer.
- VPN client not registering split DNS or overriding with its own servers.
- Browsers using DNS-over-HTTPS bypassing the OS resolver.
- Router forwarding to ISP DNS for internal zones.

## Fix
Correct scope options and renew client leases; remove statics;
configure conditional forwarders for partner/internal zones; manage DNS-over-HTTPS in browsers through
enterprise policy.

## Verify
- [ ] Client shows only intended resolvers on all adapters/IPv6; internal and external names resolve; the domain controller locator succeeds.

## Checked

- Date: 2026-10-28
- Confirmed: resolvectl status shows global and per-link DNS settings in effect (resolvectl man page); IPv6 router advertisements carry recursive DNS server addresses and a search list (RFC 8106).
- Removed: Windows, macOS and resolv.conf commands, ipconfig renew, NRPT, the browser canary domain, nltest (none appear in the cited sources).

Method: documentation only; no commands were run.
