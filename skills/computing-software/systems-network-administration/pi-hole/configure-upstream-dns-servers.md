---
id: computing-software.systems-network-administration.pi-hole.configure-upstream-dns-servers
name: configure-upstream-dns-servers
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-upstreams, dns-upstream, upstream-port]
level: intro
status: docs-checked
description: "Set the upstream DNS servers Pi-hole forwards to, including hostnames and non-standard ports such as a local Unbound."
sources: ["https://docs.pi-hole.net/ftldns/configfile/", "https://docs.pi-hole.net/docker/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upstream DNS servers

`dns.upstreams` lists the servers Pi-hole asks for anything it cannot answer itself. If it is empty, Pi-hole does not resolve any non-local queries.

Allowed values are an array of IP addresses and/or hostnames, each optionally followed by a port after `#`:

```toml
[dns]
  upstreams = [ "8.8.8.8", "127.0.0.1#5335", "docker-resolver" ]
```

From the command line:

```bash
sudo pihole-FTL --config dns.upstreams '["1.1.1.1", "127.0.0.1#5335"]'
```

In Docker use a semicolon-delimited value: `FTLCONF_dns_upstreams: '8.8.8.8;8.8.4.4'`.

**Port.** `dns.port` (default `53`) is the port Pi-hole itself listens on; it is separate from the upstream port.

**Related options**

- `dns.CNAMEdeepInspect` (default `true`) inspects CNAME chains so blocked targets are caught; disabling may help very low-end devices.
- `dns.queryLogging` (default `true`) writes queries and replies to `pihole.log`.

**Local resolver.** The configuration reference's own example points to a local resolver as `127.0.0.1#5335`.

**Checklist**

1. Add at least one upstream; otherwise only local names resolve.
2. Include `#port` for a resolver not on 53.
3. Test with `dig pi-hole.net @127.0.0.1`.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: FTL Configuration Reference (ftldns/configfile); Docker Configuration (docker/configuration). Removed the unconfirmed pointer to provider lists; the Unbound port is now stated as the reference page example.
Method: documentation only; no commands were run.
