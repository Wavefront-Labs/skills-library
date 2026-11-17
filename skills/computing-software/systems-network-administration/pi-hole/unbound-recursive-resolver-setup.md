---
id: computing-software.systems-network-administration.pi-hole.unbound-recursive-resolver-setup
name: unbound-recursive-resolver-setup
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [unbound-pihole, recursive-dns, unbound-config]
level: advanced
status: draft
description: "Install Unbound as a local recursive resolver for Pi-hole on port 5335 and point Pi-hole at 127.0.0.1#5335."
sources: ["https://docs.pi-hole.net/guides/dns/unbound/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Unbound as a recursive resolver for Pi-hole

A recursive resolver walks from the root servers down to the authoritative servers itself, so no single upstream provider sees all your queries. The drawback is speed: the first request to a new TLD may take up to a second (more with DNSSEC); later requests under the same TLD usually finish in under 0.1 s.

**Install**

```bash
sudo apt install unbound
```

A package-manager install brings `root.hints` via `dns-root-data` and keeps it updated. Only if you download `named.root` yourself, refresh it roughly every six months and uncomment `root-hints:`.

**Config** goes in `/etc/unbound/unbound.conf.d/pi-hole.conf` (some Red Hat family distros use `/etc/unbound/conf.d/`). The recommended `server:` block listens only on `127.0.0.1` port `5335`, enables UDP and TCP, keeps `prefer-ip6: no`, sets `harden-glue: yes`, `harden-dnssec-stripped: yes`, `use-caps-for-id: no`, `edns-buffer-size: 1232`, `prefetch: yes`, `num-threads: 1`, `so-rcvbuf: 1m`, and lists `private-address` ranges to protect local IPs.

**Start and test**

```bash
sudo service unbound restart
dig pi-hole.net @127.0.0.1 -p 5335
```

**Point Pi-hole at it:** upstream `127.0.0.1#5335`, with all other upstreams removed. CLI:

```bash
sudo pihole-FTL --config dns.upstreams '["127.0.0.1#5335"]'
```

**Checklist**

1. Test root-server reachability first (see the Unbound troubleshooting skill).
2. Install and write the config.
3. Restart, test, then change the upstream.
