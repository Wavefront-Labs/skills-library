---
id: computing-software.cloud-infrastructure-engineering.graylog.deployment-models-and-sizing
name: deployment-models-and-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [sizing, size-estimator, high-iops, core-model, conventional-model, capacity-planning]
level: practitioner
status: docs-checked
description: "Plan a Graylog deployment: Core versus Conventional models, the size estimator, storage IOPS and retention-driven capacity."
sources:
  - https://go2docs.graylog.org/current/planning_your_deployment/graylog_system_architecture.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# deployment models and sizing

Graylog documents standard deployment models. Two used in install guides:
- **Core**: one Graylog and MongoDB node plus one Data Node.
- **Conventional**: three Graylog and MongoDB nodes plus three Data Nodes. The architecture page recommends it for most larger-scale production environments; the Debian multi-node guide says medium-to-large. A third model, Custom, is also listed.

Key guidance:
- Choose high-IOPS storage such as SSDs; IOPS drives ingestion, indexing and search speed.
- Pick an architecture that can grow with log volume (cluster expansion, load balancing, resource allocation).
- Set a retention policy balancing compliance needs and storage capacity.

Use Graylog's size estimator for a first estimate, either from number of users and retention days, or from estimated daily log volume.

The estimate is general. Real requirements vary with log complexity, retention, search frequency and hardware, so load test and monitor system metrics to tune.

## Checked

2026-11-04. Confirmed against the System Architecture page and the Debian multi-node and Red Hat install guides. Removed: the user-count ranges for the size estimator, which are not in the page text. Page conflict: the Debian multi-node guide says the Conventional model suits medium-to-large deployments; the architecture page says larger-scale production environments.

Method: documentation only; no commands were run.
