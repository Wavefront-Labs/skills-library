---
id: computing-software.cloud-infrastructure-engineering.rancher.helm-external-tls-termination
name: helm-external-tls-termination
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [tls-external, layer-7, load-balancer, websocket, healthz, x-forwarded-proto]
level: advanced
status: docs-checked
description: "Terminate TLS on an external layer 7 load balancer with tls=external: required headers, 1800 second timeouts, websocket support, healthz check, and privateCA caveat."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/installation-references/helm-chart-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The recommendation is a layer 4 balancer forwarding plain 80/tcp and 443/tcp to the cluster nodes, with the in-cluster ingress terminating TLS. You may instead terminate TLS on a layer 7 balancer outside the cluster. Install with `--set tls=external` and point the balancer at **HTTP port 80** on every Rancher cluster node.

Be aware that clients able to reach the cluster nodes directly will not be encrypted, so the page recommends restricting direct access at the network level to just the load balancer.

If the certificate is signed by a private CA, or `agent-tls-mode` is `strict`, add `--set privateCA=true` and add the CA certificate to Rancher as described in the Adding TLS Secrets page, so agents can validate Rancher.

Load balancer requirements from the page:

- Support long-lived **websocket** connections.
- Insert the headers `Host`, `X-Forwarded-Proto`, `X-Forwarded-Port` and `X-Forwarded-For` so Rancher can route links correctly.
- Recommended timeouts: read 1800 seconds, write 1800 seconds, connect 30 seconds.
- Health checks: Rancher answers `200` on `/healthz`.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Rancher Helm Chart Options (External TLS Termination). Nothing removed.

Method: documentation only; no commands were run.
