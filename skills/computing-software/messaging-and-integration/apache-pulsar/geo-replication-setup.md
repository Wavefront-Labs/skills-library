---
id: computing-software.messaging-and-integration.apache-pulsar.geo-replication-setup
name: geo-replication-setup
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [geo-replication, clusters-create, allowed-clusters, set-clusters, replication-clusters, selective-replication]
level: practitioner
status: docs-checked
description: "Set up Pulsar geo-replication: connect clusters, grant tenant allowed-clusters, enable at namespace or topic level, selective replication and replication direction."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/administration-geo.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replicate topic data between clusters for disaster recovery or regional consumption.

Step 1, connect clusters. On each cluster register the others:
```shell
bin/pulsar-admin clusters create --broker-url pulsar://<DNS-OF-US-EAST>:<PORT> --url http://<DNS-OF-US-EAST>:<PORT> us-east
```
Use `--broker-url-secure` and `--url-secure` for TLS; `--auth-plugin` with `--auth-parameters` sets per-cluster authentication and overrides `brokerClientAuthenticationPlugin` and `brokerClientAuthenticationParameters`. Run the mirror commands on every other cluster.

Step 2, tenant permission: `bin/pulsar-admin tenants create my-tenant --admin-roles my-admin-role --allowed-clusters us-west,us-east,us-cent` (for an existing tenant use `tenants update`). The tenant `allowed-clusters` cannot be modified once the tenant has namespaces, so set it first.

Step 3, enable at namespace level or topic level:
```shell
bin/pulsar-admin namespaces create my-tenant/my-namespace
bin/pulsar-admin namespaces set-clusters my-tenant/my-namespace --clusters us-west,us-east,us-cent
bin/pulsar-admin topics set-replication-clusters --clusters us-west,us-east,us-cent my-tenant/my-namespace/my-topic
```
Changes take effect immediately and without disrupting traffic.

Selective replication: producers restrict one message with `producer.newMessage().value(...).replicationClusters(list).send()`.

Direction: with separate metadata stores, two-way replication needs each cluster to list the other in namespace `clusters` and `allowed-clusters`. For one-way, list only the local cluster in both on the non-replicating cluster. `allowed-clusters` cannot be overridden by the per-message list. Replicated subscriptions require two-way replication.

Check progress with `bin/pulsar-admin topics stats persistent://my-tenant/my-namespace/my-topic`; each cluster reports its own replication rates and backlogs.

## Checked

2026-11-03. Confirmed against the Pulsar geo-replication administration page: `clusters create` options, tenant `allowed-clusters` (cannot change once the tenant has namespaces), namespace `set-clusters`, topic `set-replication-clusters`, no disruption on changing replication clusters, `replicationClusters` per-message override and that it cannot override `allowed-clusters`, replication direction with separate metadata stores. Removed: the 2.10.x topic-level configuration sentence and the generic Verify line, neither of which the page supports.

Method: documentation only; no commands were run.
