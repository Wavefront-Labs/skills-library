---
id: computing-software.database-administration.patroni.patroni-consul-zookeeper-dcs-config
name: patroni-consul-zookeeper-dcs-config
category: computing-software
field: database-administration
product: patroni
tags: [patroni, consul, zookeeper, exhibitor, dcs]
level: practitioner
status: docs-checked
description: "Key settings for the Consul, ZooKeeper and Exhibitor DCS sections."
sources:
  - https://patroni.readthedocs.io/en/latest/yaml_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure a non-etcd DCS.

Consul (one of `host` or `url` is required):
- `host`, `url`, `port`, `scheme` (default http), `token`, `verify`, `cacert`, `cert`, `key`, `dc` (default: host datacenter).
- `consistency`: `default`, `consistent` or `stale`.
- `checks`: Consul health checks for the session (default empty list).
- `register_service` (default false): register a service named by `scope` with a tag `primary`, `replica` or `standby-leader` per role (the master tag is also mentioned). `service_tags` adds static tags; `service_check_interval` defaults to '5s'; `service_check_tls_server_name` overrides SNI.
- Token ACL: write on `service_prefix` scope, `key_prefix` `namespace/scope`, and all `session_prefix`.

ZooKeeper:
- `hosts`: list such as ['host1:port1', 'host2:port2'].
- `use_ssl` (default false), `cacert`, `cert`, `key`, `key_password`, `verify` (default true).
- `set_acls`: default ACL for created ZNodes with x509 schema, for example `{CN=principal1: [CREATE, READ], CN=principal2: [ALL]}`; permissions are CREATE, READ, WRITE, DELETE, ADMIN.
- `auth_data`: scheme-to-credential dictionary. SSL requires kazoo>=2.6.0.

Exhibitor (ZooKeeper discovery):
- `hosts`: initial list `host1,host2`, updated automatically as topology changes.
- `poll_interval`: how often the node list is refreshed from Exhibitor.
- `port`: Exhibitor port.

## Checked

2026-11-03. Confirmed against YAML Configuration Settings (Consul, ZooKeeper and Exhibitor sections): option names, defaults, ACL permissions list, kazoo>=2.6.0 requirement.

Method: documentation only; no commands were run.
