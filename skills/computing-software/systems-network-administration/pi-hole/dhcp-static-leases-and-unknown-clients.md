---
id: computing-software.systems-network-administration.pi-hole.dhcp-static-leases-and-unknown-clients
name: dhcp-static-leases-and-unknown-clients
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [static-dhcp-leases, dhcp-hosts, ignore-unknown-clients]
level: advanced
status: docs-checked
description: "Reserve addresses with dhcp.hosts static leases and optionally ignore unknown DHCP clients."
sources: ["https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Static DHCP leases

`dhcp.hosts` assigns per-host parameters so a machine with a given hardware address always gets the same hostname, IP address and lease time.

**Format**

```text
"[<hwaddr>][,id:<client_id>|*][,set:<tag>][,tag:<tag>][,<ipaddr>][,<hostname>][,<lease_time>][,ignore]"
```

**Example**

```toml
[dhcp]
  hosts = [ "00:20:e0:3b:13:af,192.168.0.123,laptop,24h",
            "00:20:e0:ab:cd:ef,192.168.0.124,desktop,24h" ]
```

**Ignore unknown clients.** Setting `dhcp.ignoreUnknownClients` to `true` makes Pi-hole ignore every client not explicitly configured in `dhcp.hosts`. Note:

- it is not a security feature: a client can still assign itself an address and use the network;
- you must then configure each new client in `dhcp.hosts` before it can get an address automatically.

**Pitfalls**

- The hostname must follow the domain rules in `dns.domain.name`: with no domain set, a DHCP hostname containing a period is disallowed and logged; with a domain set, a suffix must match it.
- `dhcp.hosts` can also carry a `set:` or `tag:` entry and a per-host lease time, such as `24h`, in the same string.

**Checklist**

1. Read each device's MAC address.
2. Add one `dhcp.hosts` line per device.
3. Renew the lease on the client.
4. Confirm the client received the reserved address.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: FTL Configuration Reference (ftldns/configfile). Reworded the unconfirmed check step about the web interface lease table.
Method: documentation only; no commands were run.
