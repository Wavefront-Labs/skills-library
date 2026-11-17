---
id: computing-software.database-administration.elasticsearch.ip-filtering
name: ip-filtering
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, ip-filtering, elasticsearch-security, network-security, transport-filter]
level: practitioner
status: docs-checked
description: "Restrict which IPs can connect to Elasticsearch transport and HTTP layers with xpack.security IP filtering, update rules dynamically, and combine with firewalls."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/security/ip-filtering-basic.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/security-settings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IP filtering

**Goal:** an extra allow-list inside Elasticsearch so only cluster nodes speak transport and only approved networks reach HTTP. Defence in depth, not a replacement for authentication or host firewalls.

## Static config (elasticsearch.yml)
```yaml
xpack.security.transport.filter.allow: ["10.20.0.0/24"]
xpack.security.transport.filter.deny: _all
xpack.security.http.filter.allow: ["10.10.0.0/16", "192.168.5.10"]
xpack.security.http.filter.deny: _all
```
Allow rules take precedence over deny rules. `_all` denies everything not explicitly allowed. Unless set explicitly, `xpack.security.http.filter.*` and `xpack.security.remote_cluster.filter.*` default to the matching `xpack.security.transport.filter.*` values. Hostnames work only when DNS lookups are available; prefer IPs or CIDRs. With operator privileges enabled, only operator users can change these settings.

## Dynamic update
```json
PUT _cluster/settings
{ "persistent": { "xpack.security.http.filter.allow": ["10.10.0.0/16", "172.16.4.0/22"] } }
```
These filter settings are dynamic, so you can change them without a restart; keep the source of truth in one place (config management or cluster settings) to avoid confusion.

## Profiles
Transport profiles (e.g. a client profile on another port) can have their own filters: `transport.profiles.client.xpack.security.filter.allow`.

## Gotchas
- Locking yourself out: deny `_all` on HTTP without your admin network allows means only console access to nodes can fix it (edit the file and restart, or remove the persistent setting from a node that still has access).
- Remember cross-cluster peers: certificate-based remote clusters use the transport interface, API-key based ones use the remote cluster interface (`xpack.security.remote_cluster.filter.*`, enabled or disabled together with `xpack.security.transport.filter.enabled`).

## Verify
`curl` from a disallowed host gets the connection closed; audit log records `connection_denied` events if `xpack.security.audit` includes them; `GET _cluster/settings?include_defaults=true&filter_path=**.filter` shows active rules.

## Checked

Checked 2026-10-25 against elastic/docs-content and elastic/elasticsearch `main` (Stack 9.x docs). Confirmed: setting names for transport, HTTP, remote cluster and transport profiles; allow takes precedence over deny; `_all`; defaults inherited from the transport filter; hostname filtering needs DNS; settings are dynamic and can be changed via `PUT _cluster/settings`. Removed the unconfirmed proxy-IP and security-disabled notes. The audit `connection_denied` event type was confirmed in the audit events reference; the `_cluster/settings` filter_path in Verify was not re-read.

Method: documentation only; no commands were run.
