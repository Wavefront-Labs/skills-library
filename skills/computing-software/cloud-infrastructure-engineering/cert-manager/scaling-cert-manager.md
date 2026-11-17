---
id: computing-software.cloud-infrastructure-engineering.cert-manager.scaling-cert-manager
name: scaling-cert-manager
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [scaling, kubernetesapiqps, serversideapply, revisionhistorylimit, memory, optimistic-locking]
level: advanced
status: docs-checked
description: "Scale cert-manager on busy clusters: size controller memory, lift client-side API rate limits, cap revision history, and enable ServerSideApply to stop conflicts."
sources:
  - https://cert-manager.io/docs/devops-tips/scaling-cert-manager/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Memory: for certificate-heavy clusters (mounted TLS Secrets, gateway-shim), controller memory scales roughly with the total size of TLS Secrets, because it caches their full contents. Large keys (RSA 4096) cost more than ECDSA. Non-TLS Secrets cache metadata only. CertificateRequest-heavy workloads (csi-driver, istio-csr) need less.

Client-side rate limit: default 20 QPS to the API server. Raise with Helm `config.kubernetesAPIQPS: 10000` and `config.kubernetesAPIBurst: 10000`. This does not disable the limiter, just sets values never reached, and relies on API Priority and Fairness being enabled.

Large RSA keys use CPU; under pressure the reconcile queue grows and delays every Certificate, so one tenant creating many RSA 4096 certificates can deny service to others. Mitigate with an approval policy or Certificate defaults (for example via Kyverno).

`revisionHistoryLimit`: the default was unlimited CertificateRequest history, and became `1` in v1.18.0+. On older versions set `Certificate.spec.revisionHistoryLimit: 1` everywhere (Kyverno can override across namespaces; Ingress has its own annotation). Unbounded history strains API server memory, CPU and storage.

Server-Side Apply: default Update requests produce frequent optimistic-locking conflicts. Symptom in logs: `re-queuing item due to optimistic locking on resource`, each with exponential backoff. Fix: enable the `ServerSideApply` feature gate (Helm `config.featureGates.ServerSideApply: true`); controllers then PATCH only fields they own.

## Checked

2026-11-03: Confirmed against the Scaling cert-manager page: memory proportional to TLS Secret size with metadata-only caching of other Secrets, lower memory for CertificateRequest-heavy use, the 20 QPS default and the `kubernetesAPIQPS`/`kubernetesAPIBurst` 10000 values, large RSA keys and CPU, `revisionHistoryLimit` with the v1.18.0 default change, optimistic-locking log line, and the `ServerSideApply` feature gate Helm value. Nothing removed.

Method: documentation only; no commands were run.
