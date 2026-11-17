---
id: computing-software.systems-network-administration.pi-hole.block-hardcoded-dns-with-firewall
name: block-hardcoded-dns-with-firewall
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [block-other-dns, hardcoded-dns, opnsense-firewall-rules]
level: advanced
status: docs-checked
description: "Stop devices with hardcoded DNS servers from bypassing Pi-hole using OPNsense alias and ordered firewall rules."
sources: ["https://docs.pi-hole.net/routers/OPNsense/", "https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Blocking other DNS servers

Some clients, such as Chromecasts, use hardcoded DNS servers. On OPNsense you can block DNS that does not come from Pi-hole.

**Limitations.** The guide does not cover blocking DoH or DoT. If a device has no fallback from its hardcoded DNS, this can break its DNS.

**Steps**

1. Firewall, Aliases: create an alias of type MAC address containing the Pi-hole's MAC (the `ether` line from `ifconfig eth0`).
2. Firewall, Rules, pick the interface to modify.
3. First rule: allow the Pi-hole (via the alias) to do DNS.
4. Second rule, placed after it: reject all DNS.

**Order matters.** OPNsense applies the first rule that matches. If the reject rule comes first, Pi-hole itself cannot reach any DNS servers.

**No extra rule for same-network clients.** A client on the same network as Pi-hole (for example 10.0.51.10 reaching 10.0.51.2) talks to it directly, so the DNS request does not route through OPNsense.

**Related defences in Pi-hole.** The `dns.specialDomains` options (Firefox canary, iCloud Private Relay, designated resolvers) stop some clients bypassing Pi-hole without firewall rules.

**Checklist**

1. Build the alias.
2. Add the allow rule before the reject rule.
3. Test a hardcoded-DNS device for working fallback.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: OPNsense (routers/OPNsense); FTL Configuration Reference (ftldns/configfile). Nothing needed removing.
Method: documentation only; no commands were run.
