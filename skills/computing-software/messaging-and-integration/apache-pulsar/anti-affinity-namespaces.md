---
id: computing-software.messaging-and-integration.apache-pulsar.anti-affinity-namespaces
name: anti-affinity-namespaces
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [anti-affinity, failure-domain, create-failure-domain, set-anti-affinity-group, namespace-placement]
level: advanced
status: docs-checked
description: "Spread related Pulsar namespaces across failure domains: create domains and register brokers, assign anti-affinity groups, and how the load manager distributes them."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/administration-anti-affinity-namespaces.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep at least one of a group of namespaces available by placing them on different failure domains.

Concept: a group of namespaces with anti-affinity are distributed to different failure domains in a load-balanced way. The load manager assigns them evenly across domains, and within a domain evenly across the brokers of that domain. Example from the page: two domains with two brokers each and four namespaces in one group lead to assignments Domain1:Broker1, Domain2:Broker3, Domain1:Broker2, Domain2:Broker4. If there are more namespaces than domains, they are spread evenly across all domains and then across the brokers in each domain.

Rules:
- A namespace belongs to only one anti-affinity group. Assigning a namespace that already has a group to another group drops the original assignment.
- A broker can be registered to only one failure domain.

Create a failure domain and register brokers:
```bash
pulsar-admin clusters create-failure-domain <cluster-name> --domain-name <domain-name> --broker-list <broker-list-comma-separated>
```
Domains can also be viewed, updated and deleted under a cluster (see the pulsar-admin reference).

Assign a namespace to an anti-affinity group; the group is created automatically when the first namespace is assigned:
```bash
pulsar-admin namespaces set-anti-affinity-group <namespace> --group <group-name>
```

## Checked

2026-11-03. Confirmed against the pulsar-site page administration-anti-affinity-namespaces: the distribution rules and four-namespace example, one group per namespace, one domain per broker, and both commands. Removed the unsourced geo-replication gotcha and the invented Verify step.

Method: documentation only; no commands were run.
