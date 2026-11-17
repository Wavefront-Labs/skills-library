---
id: computing-software.cloud-infrastructure-engineering.cortex.mirror-requests-to-a-secondary-cluster
name: mirror-requests-to-a-secondary-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [mirroring, shadowing, envoy, testing, distributor]
level: advanced
status: docs-checked
description: "Mirror write traffic from a primary Cortex cluster to a secondary test cluster using Envoy when you cannot add a second remote_write."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/operations/requests-mirroring-to-secondary-cluster.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Request mirroring (shadowing) sends the same writes to a secondary cluster, for example a test cluster that should receive the series a primary one ingests when you do not control Prometheus remote_write config. If you do control it, configuring two remote_write entries is preferred.

With Envoy, run the proxy in front of both clusters' distributors. It proxies every request to the primary and mirrors it to the secondary in the background. The example config listens on port 9900, with the admin interface on 9901, and routes prefix `/` to `cortex-primary:80` with a request mirror policy to `cortex-secondary:80`.

Point Prometheus remote_write at Envoy's port rather than at the primary. The secondary's performance and availability have no effect on requests to the primary: the client always receives the primary's response, and the mirrored request is fire-and-forget.

## Checked

Method: docs-checked 2026-11-09 against the Cortex requests mirroring guide (raw markdown, read in full).
