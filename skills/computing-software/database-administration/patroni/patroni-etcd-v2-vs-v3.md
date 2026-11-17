---
id: computing-software.database-administration.patroni.patroni-etcd-v2-vs-v3
name: patroni-etcd-v2-vs-v3
category: computing-software
field: database-administration
product: patroni
tags: [patroni, etcd, etcd3, migration, api-version]
level: advanced
status: docs-checked
description: "The difference between the etcd and etcd3 sections and why they are not interchangeable."
sources:
  - https://patroni.readthedocs.io/en/latest/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the right etcd API version.

`etcd` uses etcd API version 2; `etcd3` uses API version 3. All etcd3 configuration parameters are the same as for etcd.

Key points:
- Keys created with protocol v2 are not visible with v3 and the other way around, so you cannot switch from `etcd` to `etcd3` by only editing the Patroni config file.
- Patroni talks to the V3 API through Etcd's gRPC-gateway (proxy), so TLS common name authentication is not possible.
- The FAQ recommends `etcd3` because API v2 is disabled by default from Etcd v3.4 onward and will be removed completely in Etcd v3.6.

Release notes: 4.1.3 maps a mislabeled Etcd "Unknown error" (when the Etcd leader is lost during a lease update) to Unavailable; 4.1.1 improved Etcd3 error handling for broken JSON responses and handled the Etcd authentication changes in 3.6.9, 3.5.28 and 3.4.42.

## Checked

2026-11-03. Confirmed against YAML Configuration Settings (etcd and etcd3 sections), the FAQ recommendation of etcd3 and the release notes entries for 4.1.1 and 4.1.3. Removed: the README-sourced `--enable-v2=true` example and the 3-or-5-node DCS sizing paragraph, which are not on the fetched pages.

Method: documentation only; no commands were run.
