---
id: computing-software.systems-network-administration.pi-hole.reverse-servers-conditional-forwarding
name: reverse-servers-conditional-forwarding
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [rev-servers, conditional-forwarding, local-hostnames]
level: practitioner
status: draft
description: "Configure dns.revServers so local hostnames and reverse lookups are answered by your router or DHCP server."
sources: ["https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Reverse servers (conditional forwarding)

If Pi-hole is not your DHCP server it usually cannot learn local device names, so Top Clients shows only IP addresses. The fix is `dns.revServers`, formerly called conditional forwarding: forward local-range reverse lookups to your DHCP server (usually the router).

**Format** (an array of strings):

```text
"<enabled>,<ip-address>[/<prefix-len>],<server>[#<port>][,<domain>]"
```

Example:

```toml
[dns]
  revServers = [ "true,192.168.0.0/24,192.168.0.1,fritz.box" ]
```

**Components**

- `<enabled>`: `true` or `false`.
- `<ip-address>[/<prefix-len>]`: the address range in CIDR notation, such as `192.168.0.0/24`. If the prefix is omitted, 32 (IPv4) or 128 (IPv6) is used, an exact-address match, which is almost certainly not wanted.
- `<server>[#<port>]`: where to send the queries, such as `192.168.0.1#53`.
- `<domain>`: the local domain such as `fritz.box`.

When a reverse server is configured for exactly the local domain set in `dns.domain.name`, all queries for that domain, including reverse lookups, go to that server only.

**Checklist**

1. Find the router address and subnet.
2. Add the entry with the correct prefix length.
3. Confirm hostnames appear in the dashboard.
4. In Docker, use `FTLCONF_dns_revServers`.
