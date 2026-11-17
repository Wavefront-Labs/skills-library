---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-log-query-api
name: node-log-query-api
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, logs-events, node-log-query, kubelet-journal, kubelet]
level: practitioner
status: docs-checked
description: "Read node service logs (kubelet, containerd, journal) through the kubelet node log query API with kubectl get --raw, its enablement flags and query options."
sources: ["https://kubernetes.io/docs/concepts/cluster-administration/system-logs/", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node log query API

Lets admins read node logs through the API server without SSH. Introduced in v1.27; stable in v1.36, where the
`NodeLogQuery` feature gate is locked on (it was beta, off by default, from 1.30 to 1.35).

## Enable (KubeletConfiguration on each node)
```yaml
enableSystemLogHandler: true
enableSystemLogQuery: true
```
Before 1.36 also set `featureGates: {NodeLogQuery: true}`. `enableSystemLogHandler` defaults to false; leave it
off unless you are debugging. Restart the kubelet. The caller needs RBAC on `nodes/proxy`, which also
authorizes powerful kubelet APIs (admins only).

## Query
```bash
kubectl get --raw "/api/v1/nodes/worker-3/proxy/logs/?query=kubelet"
kubectl get --raw "/api/v1/nodes/worker-3/proxy/logs/?query=kubelet&tailLines=100"
kubectl get --raw "/api/v1/nodes/worker-3/proxy/logs/?query=containerd&sinceTime=2026-10-18T09:00:00Z&pattern=error"
kubectl get --raw "/api/v1/nodes/worker-3/proxy/logs/?query=/<file>"            # a file under /var/log
```
On Linux `query` maps to journald units; on Windows to services and event logs.
Parameters: `query` (required), `sinceTime`, `untilTime` (RFC 3339, inclusive), `tailLines` (default is the
whole log), `pattern` (Perl-compatible regex) and `boot` (messages from a specific system boot).

## When it does not help
The kubelet itself must be running and reachable from the API server; for a dead kubelet you need another
route to the node.

## Security
Files are only served from directories the kubelet allows for log fetches; whoever holds `nodes/proxy` can read
them, so keep the binding tight.

## Checked

2026-10-26: kubernetes.io system-logs page (log query section) and the NodeLogQuery feature-gate page (v1.37 docs, kubernetes/website main 2026-10-25). Confirmed: kubelet options and defaults, stable in 1.36 with the gate locked on (alpha 1.27, beta 1.30), the query parameters and their meanings, file fetch via query, journald on Linux, nodes/proxy warning. Removed the unconfirmed boot=-1 example, /logs/messages path and kubectl plugin remark.

Method: documentation only; no commands were run.
