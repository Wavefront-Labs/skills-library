---
id: computing-software.cloud-infrastructure-engineering.kyverno.high-availability
name: high-availability
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [high-availability, leader-election, replicas, genworkers, admission-controller, reports-controller]
level: practitioner
status: docs-checked
description: "Run Kyverno highly available: replica counts and leader election per controller, what extra replicas buy, vertical scaling and the genWorkers flag."
sources:
  - https://kyverno.io/docs/guides/high-availability/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each controller is its own Deployment. Use the Helm chart for production HA.

- Admission controller: minimum three replicas for HA. Webhook requests are not leader-elected, so every replica serves AdmissionReviews. Leader election covers only certificate and webhook management. Each replica loads the whole policy set (no sharding), so scale out for throughput and up for a large policy cache.
- Reports controller: leader-elected, one replica processes reports. Extra replicas give availability only; vertical scaling helps only the leader.
- Background controller: leader-elected, one replica does generate and mutate-existing work. Extra replicas are availability only; scale vertically or raise internal workers with `--genWorkers`.
- Cleanup controller: certificate and webhook management is leader-elected but the cleanup handler is not, so extra replicas add throughput and availability. Each deletion rule maps to one CronJob.

Related: with all admission pods down and fail-closed policies matching Pods the API server stalls; see the troubleshooting skill. The page does not cover PodDisruptionBudgets, anti-affinity, resource sizing or failover timing.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
