---
id: computing-software.cloud-infrastructure-engineering.etcd.dns-srv-discovery
name: dns-srv-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [dns-srv, discovery-srv, srv-records, discovery-srv-name, bootstrap, dns, tls]
level: advanced
status: docs-checked
description: "Bootstrap and client discovery through DNS SRV records using --discovery-srv, _etcd-server-ssl._tcp and _etcd-client."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/clustering/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

DNS SRV discovery lets you bootstrap from records instead of listing addresses.

Records for a domain `example.com`:

- Peers: `--discovery-srv example.com` looks up `_etcd-server-ssl._tcp.example.com` then `_etcd-server._tcp.example.com`; if the `-ssl` record is found, bootstrap is attempted over TLS. Each SRV record points at a host and the peer port (2380); DNS A records resolve the host.
- Clients look up `_etcd-client._tcp.example.com` then `_etcd-client-ssl._tcp.example.com`, pointing at port 2379; if the `-ssl` record is found, clients use TLS.

Check with `dig +noall +answer SRV _etcd-server._tcp.example.com`.

Start a member:

```bash
etcd --name infra0   --discovery-srv example.com   --initial-advertise-peer-urls http://infra0.example.com:2380   --initial-cluster-token etcd-cluster-1   --initial-cluster-state new   --advertise-client-urls http://infra0.example.com:2379   --listen-client-urls http://0.0.0.0:2379   --listen-peer-urls http://0.0.0.0:2380
```

Notes:

- The initial cluster is built from the SRV records, so do not set `--initial-cluster`.
- The resolved address in `--initial-advertise-peer-urls` must match one of the resolved addresses in the SRV targets. Since 3.2 `--listen-peer-urls` and `--listen-client-urls` reject domain names, so bind to an IP such as `0.0.0.0`.
- With TLS, the discovery SRV domain (for example `example.com`) must be in the certificate DNS SAN along with the hostname, or clustering fails with `bad certificate` errors. Without a custom CA the discovery domain must match the SRV record domain.
- `--discovery-srv-name` adds a suffix to the service name (for example `foo` gives `_etcd-server-ssl-foo._tcp.example.com`) to run several clusters under one domain.

## Checked

2026-11-03. Confirmed on the v3.5 clustering guide (DNS discovery section): lookup order for peer and client SRV records, the -ssl TLS behaviour, port 2380 and 2379 records with A records, the bootstrap command shape, the resolved-address match rule, domain names rejected in listen URLs since 3.2, TLS SAN requirement, and --discovery-srv-name. Fixed: the example used hostnames in the listen URLs, which the page says are rejected; it now uses 0.0.0.0 as the page does. Removed: etcdctl --discovery-srv (not on the page) and an invented -prod suffix example.

Method: documentation only; no commands were run.
