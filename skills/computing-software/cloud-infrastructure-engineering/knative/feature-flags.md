---
id: computing-software.cloud-infrastructure-engineering.knative.feature-flags
name: feature-flags
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [feature-flags, config-features, extension-flags, podspec-flags, multi-container]
level: advanced
status: docs-checked
description: "Enable alpha and beta features and Kubernetes podspec extensions through config-features."
sources:
  - https://knative.dev/docs/serving/configuration/feature-flags/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn optional Serving capabilities on or off.

Flags live in the `config-features` ConfigMap in `knative-serving`. Values:
- `Enabled`: in use.
- `Allowed`: usable, for example via an extra annotation or spec setting on a resource.
- `Disabled`: cannot be used.

Lifecycle stages are alpha (may contain bugs, may be dropped, for short-lived test clusters), beta (well tested and safe to enable, details may change) and GA (stable, flag removed).

Features: alpha is disabled by default, beta enabled by default, GA always on. Extensions surface implementation or environment specifics, are never part of the core API for lack of portability, are always flag-controlled and are never enabled by default.

Examples of keys:
- Feature `multi-container` and `multi-container-probing`.
- Feature `domainmapping-direct-route-traffic`.
- Extensions `kubernetes.podspec-volumes-emptydir`, `kubernetes.podspec-persistent-volume-claim` with `kubernetes.podspec-persistent-volume-write`, `kubernetes.podspec-affinity`, `kubernetes.podspec-nodeselector`, `kubernetes.podspec-tolerations`, `kubernetes.podspec-securitycontext`, `kubernetes.podspec-init-containers`, `kubernetes.podspec-topologyspreadconstraints`, `kubernetes.podspec-dnspolicy`.
- Extension `tag-header-based-routing` and `queueproxy.mount-podinfo`.

For extensions the page gives alpha as disabled by default and beta and GA as allowed by default, but also says an extension is never enabled by default.

## Checked

2026-11-04. Confirmed against the Feature and extension flags page (knative/docs source): flags live in the `config-features` ConfigMap in `knative-serving`, values `Enabled`, `Allowed` and `Disabled`, alpha, beta and GA descriptions, feature defaults per stage, extension rules (never in the core API, always flag-controlled, never enabled by default), and every flag key listed in the skill (`multi-container`, `multi-container-probing`, `domainmapping-direct-route-traffic`, the `kubernetes.podspec-*` keys, `tag-header-based-routing`, `queueproxy.mount-podinfo`). Removed the claim that with the Operator flags are set only in the Serving custom resource, which this page does not state. Added the page's extension-stage defaults, which sit awkwardly with its 'never enabled by default' sentence (beta and GA extensions are 'allowed' by default).

Method: documentation only; no commands were run.
