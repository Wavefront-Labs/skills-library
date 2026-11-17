---
id: computing-software.database-administration.patroni.patroni-etcd-dcs-config
name: patroni-etcd-dcs-config
category: computing-software
field: database-administration
product: patroni
tags: [patroni, etcd, dcs, srv-discovery, configuration]
level: practitioner
status: docs-checked
description: "Configure Patroni's etcd section: endpoints, SRV discovery, proxies, authentication and TLS."
sources:
  - https://patroni.readthedocs.io/en/latest/yaml_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: point Patroni at etcd correctly.

One of `host`, `hosts`, `url`, `proxy` or `srv` must be specified.

- `host`: host:port of an endpoint.
- `hosts`: list `host1:port1,host2:port2` (a comma-separated string or YAML list).
- `use_proxies: true`: treat `hosts` as proxies and skip topology discovery of the etcd cluster.
- `url` and `proxy`: use `proxy` instead of `url` when connecting through a proxy.
- `srv`: domain to search for SRV records for autodiscovery. Patroni tries these service names in order until the first success: `_etcd-client-ssl`, `_etcd-client`, `_etcd-ssl`, `_etcd`, `_etcd-server-ssl`, `_etcd-server`. If `_etcd-server*` records are found, the etcd peer protocol is used to query members; otherwise the hosts from SRV are used.
- `srv_suffix`: with `srv`, appends a suffix to the SRV name to tell multiple etcd clusters under one domain apart, for example `_etcd-client-ssl-foo._tcp.example.org`.
- `protocol`: http (default) or https; taken from `url`/`proxy` if given.
- `username`, `password`, `cacert` (enables validation), `cert`, `key`.

The DCS data lives under `namespace` (default `/service`) plus `scope`.

## Checked

2026-11-03. Confirmed against YAML Configuration Settings (etcd section): host, hosts, use_proxies, url, proxy, srv with its ordered service names and `_etcd-server*` behaviour, srv_suffix, protocol and credentials. Removed: the environment variable sentence (`PATRONI_ETCD_*`, URL form), which the fetched pages do not state.

Method: documentation only; no commands were run.
