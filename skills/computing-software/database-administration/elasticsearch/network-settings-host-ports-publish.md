---
id: computing-software.database-administration.elasticsearch.network-settings-host-ports-publish
name: network-settings-host-ports-publish
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, network-host, http-port, transport-port, publish-host, elasticsearch-setup]
level: practitioner
status: docs-checked
description: "Configure Elasticsearch network.host, http.port, transport.port and publish_host/bind_host correctly for multi-node, NAT and container setups, and verify reachability."
sources:
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/networking-settings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network settings

**Goal:** nodes find each other on the transport layer, clients reach HTTP, and nothing is exposed that should not be.

## Core settings (elasticsearch.yml)
```yaml
network.host: _site_            # or a specific IP; default is _local_ (loopback only)
http.port: 9200                 # default range 9200-9300, pin it
transport.port: 9300            # default range 9300-9400, pin it
# remote cluster (API-key) interface defaults to port 9443
```
Special values: `_local_`, `_site_`, `_global_` and `_[networkInterface]_` (for example `_en0_`); they yield IPv4 and IPv6 addresses unless you add an `:ipv4` or `:ipv6` suffix. Security auto-configuration adds `http.host: 0.0.0.0` to `elasticsearch.yml` on first start.

Binding to a non-loopback address switches Elasticsearch to **production mode**: bootstrap checks become fatal (vm.max_map_count, file descriptors, heap, etc.).

## Bind vs publish
- `network.bind_host`: interfaces to listen on (can be `0.0.0.0`).
- `network.publish_host`: the address clients and other nodes use to contact this node (must be reachable by them).
- Per layer: `http.bind_host`, `http.publish_host`, `transport.publish_host`, `transport.publish_port`.

Example behind NAT or in a container:
```yaml
network.bind_host: 0.0.0.0
network.publish_host: 10.20.0.15     # address peers can reach
transport.publish_port: 9300
```
A wrong publish address (for example an internal container IP) means other nodes cannot connect back to this node.

## Separate client and cluster networks
```yaml
http.host: 10.10.0.5        # client-facing NIC
transport.host: 10.20.0.5   # cluster backplane NIC
```

## Gotchas
- Never expose 9200 publicly without security; recent versions auto-configure TLS and authentication on first start, so keep them on.
- `discovery.seed_hosts` must use transport addresses (`host:9300`).
- Firewalls: open 9300 between all nodes, 9200 only from clients/proxies.

## Verify
```bash
curl -s --cacert ca.crt -u elastic https://10.10.0.5:9200/_nodes/_local/http,transport?filter_path=**.publish_address
```
Shows the published addresses you intended; `GET _cat/nodes?v` lists all nodes.

## Checked

Checked 2026-10-25 against elastic/elasticsearch `main` docs (Stack 9.x). Confirmed: `network.host` default `_local_`; special values; `http.port` default 9200-9300, `transport.port` default 9300-9400, remote cluster port default 9443; bind and publish host semantics; `http.host: 0.0.0.0` added by auto-configuration. Removed the unconfirmed log message and the "single address" wording. Firewall advice and the Verify `filter_path` call were not re-read.

Method: documentation only; no commands were run.
