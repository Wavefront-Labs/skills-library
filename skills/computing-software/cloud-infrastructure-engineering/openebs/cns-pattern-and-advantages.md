---
id: computing-software.cloud-infrastructure-engineering.openebs.cns-pattern-and-advantages
name: cns-pattern-and-advantages
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [cns, container-native-storage, architecture, blast-radius, concepts, kubernetes]
level: intro
status: docs-checked
description: "Explain Container Native Storage as OpenEBS frames it: per-volume containerised controllers, per-volume policy, no lock-in, and a smaller blast radius."
sources:
  - https://openebs.io/docs/concepts/cns
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Container Native Storage (CNS) is storage software built from microservice controllers that Kubernetes orchestrates. It runs anywhere Kubernetes runs, and the data itself is reached through containers instead of an off-platform shared scale-out system. OpenEBS describes itself as an implementation of this pattern.

The OpenEBS docs give these advantages:

- **Agility.** Each volume has its own containerised controller and replicas, so Kubernetes rolling upgrades apply to storage, and CPU and memory can be tuned with cgroups.
- **Granular policy.** A dedicated controller per volume means storage policies are set per volume, and each volume can be monitored and tuned on its own.
- **No lock-in.** Controllers can migrate data in the background per workload, which eases moving stateful workloads between clusters or clouds.
- **Cloud-native management.** Disks and pools are represented as CRDs, so Prometheus, Grafana and similar tools can manage and observe them.
- **Lower blast radius.** Because components are per workload and loosely coupled, a failure touches far less than in a typical distributed storage system. High availability comes from synchronous replication; the metadata is only which nodes hold replicas and their status for quorum. If a node fails, the stateless controller starts on a node holding another replica.

Use this page when you need to justify why OpenEBS runs one controller per volume rather than a single shared storage controller. The page points to the OpenEBS Architecture page for the concrete components.

## Checked

Method: 2026-11-08 read the raw markdown of the cited CNS page in full; the five advantages match. Replaced a cross-reference to another skill with the page's own pointer to the Architecture page.
