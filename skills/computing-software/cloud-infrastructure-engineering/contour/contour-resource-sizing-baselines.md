---
id: computing-software.cloud-infrastructure-engineering.contour.contour-resource-sizing-baselines
name: contour-resource-sizing-baselines
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [resource-limits, performance, memory, cpu, iperf3, scale-testing, 10k-services]
level: advanced
status: docs-checked
description: "Contour and Envoy resource baselines from the project load test: memory for 5k/10k Services and Ingresses, CPU at 30k-300k RPS, and measuring network bandwidth with iperf3."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/guides/resource-limits.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour and Envoy resource sizing

The guide reports a test on Kubernetes 1.12: 5 nodes (2 CPU, 8 GB), 10 Gb network, one Contour, 4 Envoys as a hostNetwork DaemonSet. Treat figures as relative orders of magnitude, not current guarantees.

Measure network bandwidth first with `iperf3` (server on one node, client on another): the test saw about 4.96 Gbit/s, which bounds achievable requests per second.

Observed memory (Contour / Envoy):
- Idle: 10 MB / 15 MB.
- 5k Services: 46 MB / 15 MB. 10k Services: 77 MB / 205 MB.
- 5k Ingress: 36 MB / 230 MB. 10k Ingress: 63 MB / 10 MB.
- 5k Services plus 5k Ingress: 244 MB / 221 MB.
- 10k Services plus 10k Ingress: 2600 MB / 430 MB (Contour 6% CPU, Envoy 4%).

Observed traffic (no config objects), Envoy only:
- 30k RPS, 600 connections: 17 MB, 3% CPU.
- 100k RPS: 118 MB, 14%.
- 200k RPS: 191 MB, 31%.
- 300k RPS: 225 MB, 40%.

Takeaways from the table: Contour memory jumps at 10k Services plus 10k Ingresses, while Envoy CPU rises with request rate. Measure your own workload before setting limits.

## Checked

2026-11-08: read the Contour docs guides/resource-limits in full. Confirmed: cluster spec (Kubernetes v1.12.6, 5 nodes of 2 CPU and 8 GB, 10 GB network, single Contour, 4 Envoys on HostNetwork DaemonSet), the iperf3 result of 4.96 Gbits/sec, and every memory and CPU row quoted. Removed: the overload-manager advice, which is not in the guide.

Method: documentation only; no commands were run.
