---
id: computing-software.cloud-infrastructure-engineering.kyverno.configuring-kyverno
name: configuring-kyverno
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [configmap, resourcefilters, excludegroups, webhooktimeout, flags, certificates, http-blocklist]
level: advanced
status: docs-checked
description: "Tune Kyverno via the kyverno ConfigMap keys, container flags, environment variables, HTTP call defaults and webhook certificate lifecycle."
sources:
  - https://kyverno.io/docs/installation/customization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ConfigMap `kyverno` in namespace `kyverno` (name overridable with env `INIT_CONFIG`; read at runtime). Keys and defaults:
- `defaultRegistry` `docker.io`; `enableDefaultRegistryMutation` `"true"`
- `excludeGroups` `system:serviceaccounts:kube-system,system:nodes`; `excludeUsernames` `!system:kube-scheduler` (`!` negates); `excludeRoles`, `excludeClusterRoles` undefined
- `generateSuccessEvents` `"false"`; `updateRequestThreshold` 1000
- `resourceFilters`: `[kind,namespace,name]` with `*`; not applied in background scans; defaults skip Nodes, Events, APIService, SubjectAccessReview and others
- `webhooks`: default namespaceSelector excludes `kube-system` and `kyverno`; `matchConditions` (CEL) needs Kubernetes 1.27+ with `AdmissionWebhookMatchConditions`

Selected flags: `autoUpdateWebhooks` true (when false, wildcard webhooks with `Ignore` and ConfigMap webhook settings ignored); `backgroundScanInterval` 1h; `backgroundScanWorkers` 2; `genWorkers` 10; `webhookTimeout` 10 (1 to 30); `clientRateLimitQPS` 300; `eventsRateLimitQPS` 1000; `enablePolicyException` false (needs `exceptionNamespace`); `allowInsecureRegistry` testing only; `imageVerifyCacheTTLDuration` 60m; `otelConfig` `prometheus` (use `grpc` for OpenTelemetry); `tlsKeyAlgorithm` RSA; `renewBefore` 360h0m0s; ports 9443 webhook, 443 service, 8000 metrics.

HTTP in CEL: disabled in namespaced policies, allowed in cluster-scoped ones, so restrict who may create cluster-scoped policies. Default blocklist: 169.254.169.254, 169.254.169.253, metadata.google.internal, 127.0.0.0/8, ::1/128 (`httpBlocklist`, `httpAllowlist`).

Certificates: CA valid one year, TLS 150 days, checked at least every 12 hours, renewed about 15 days early. With custom or cert-manager certificates you manage rotation.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
