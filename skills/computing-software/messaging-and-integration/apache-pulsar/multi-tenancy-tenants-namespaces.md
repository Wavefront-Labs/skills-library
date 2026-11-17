---
id: computing-software.messaging-and-integration.apache-pulsar.multi-tenancy-tenants-namespaces
name: multi-tenancy-tenants-namespaces
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [multi-tenancy, tenants, namespaces, topic-url, change-events, topic-level-policies]
level: practitioner
status: docs-checked
description: "Model Pulsar multi-tenancy with persistent://tenant/namespace/topic names, tenant vs namespace scope, and how __change_events carries topic-level policies."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-multi-tenancy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand how tenants and namespaces scope topics, policies and capacity.

Topic URLs have the form `persistent://tenant/namespace/topic`. The tenant is the most basic unit of categorization, above namespace and topic name.

Tenant: the administrative unit for allocating capacity and enforcing authentication or authorization. A tenant is assigned an authorization scheme and the set of clusters its configuration applies to, so tenants can span clusters.

Namespace: a logical grouping of topics and the administrative unit inside a tenant. Policies set on a namespace apply to every topic in it. A tenant can create its own namespaces through the REST API or `pulsar-admin`. For example, `persistent://tenant/app1/topic-1` and `persistent://tenant/app1/topic-2` share namespace `tenant/app1`.

Topic-level policies: policies such as retention and storage quota were historically namespace-only. Topic-level policy changes are propagated through a per-namespace system topic named `__change_events`:
1. An admin client calls the Admin REST API on a broker.
2. That broker publishes a policy change event to the namespace's `__change_events` topic.
3. Each broker owning bundles of the namespace subscribes to that topic.
4. Each broker applies events to its policy cache.
5. After the cache is updated the broker replies to the admin client.

This avoids loading ZooKeeper and uses Pulsar itself as the scalable event log.

## Checked

2026-11-03. Confirmed against the pulsar-site page concepts-multi-tenancy: topic URL form, tenant and namespace definitions, the `__change_events` flow and its ZooKeeper-load rationale. Removed the unsourced troubleshooting gotcha and the invented Verify step.

Method: documentation only; no commands were run.
