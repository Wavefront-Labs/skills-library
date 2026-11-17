---
id: computing-software.cloud-infrastructure-engineering.kubernetes.service-env-vars-vs-dns-and-enableservicelinks
name: service-env-vars-vs-dns-and-enableservicelinks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service-env-vars, enableservicelinks, service-discovery, dns, ckad]
level: practitioner
status: docs-checked
description: "Choose DNS over injected Service env vars, and turn off enableServiceLinks when big namespaces bloat pod env, slow startup, or collide with app variables."
sources: ["https://kubernetes.io/docs/concepts/services-networking/service/#environment-variables", "https://kubernetes.io/docs/tutorials/services/connect-applications-service/", "https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Service env vars vs DNS, and enableServiceLinks

## What kubelet injects
When a Pod runs on a Node, the kubelet adds environment variables for each active Service in the
Pod's namespace: `{SVCNAME}_SERVICE_HOST` and `{SVCNAME}_SERVICE_PORT`, with the Service name
upper-cased and dashes converted to underscores, plus Docker-links style variables. For a Service
named `redis-primary` on port 6379 (documented example):
```
REDIS_PRIMARY_SERVICE_HOST=10.0.0.11
REDIS_PRIMARY_SERVICE_PORT=6379
REDIS_PRIMARY_PORT=tcp://10.0.0.11:6379
REDIS_PRIMARY_PORT_6379_TCP=tcp://10.0.0.11:6379
REDIS_PRIMARY_PORT_6379_TCP_PROTO=tcp
REDIS_PRIMARY_PORT_6379_TCP_PORT=6379
REDIS_PRIMARY_PORT_6379_TCP_ADDR=10.0.0.11
```
`KUBERNETES_SERVICE_HOST` and `KUBERNETES_SERVICE_PORT` are always present.

## Why DNS is the right default
- A Service created after the Pod does not appear in the Pod's environment: the Service must exist
  before the client Pod starts.
- DNS (`redis-primary.data.svc.cluster.local`) works across namespaces and has no ordering
  requirement.

## When to disable service links
```yaml
spec:
  enableServiceLinks: false
```
The Kubernetes tutorial suggests setting it to `false` when the injected variables clash with
variables the program expects, or there are too many variables to process, or you only use DNS.
A Service named `redis` produces `REDIS_PORT=tcp://...`, which clashes with an application that
reads `REDIS_PORT` as a number.

The field is per Pod spec; set it in the Pod template of your charts. For a cluster-wide default
use an admission or mutation policy engine.

## Verify
```bash
kubectl exec deploy/api -- env
kubectl exec deploy/api -- getent hosts redis-primary.data.svc.cluster.local
```
After disabling, confirm the application does not read `*_SERVICE_HOST` or `*_SERVICE_PORT`.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Service concept page (variable naming rule, the redis-primary example, namespace and ordering behaviour) and the Connecting Applications tutorial (when to set enableServiceLinks to false). Removed unconfirmed claims about argument-list limits, startup slowdown, specific client libraries, secrets hygiene and the absence of a cluster-wide switch.

Method: documentation only; no commands were run.
