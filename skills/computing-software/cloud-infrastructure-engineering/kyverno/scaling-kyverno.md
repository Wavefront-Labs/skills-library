---
id: computing-software.cloud-infrastructure-engineering.kyverno.scaling-kyverno
name: scaling-kyverno
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [scaling, sizing, latency, replicas, global-context, policy-reports, oom]
level: advanced
status: docs-checked
description: "Size Kyverno by policy scope rather than node count, read the published latency and report-load numbers, and avoid the OOM-blocks-admission failure."
sources:
  - https://kyverno.io/docs/installation/scaling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Size by policy scope, not Node or Pod count. A wildcard (`"*"`) match forces Kyverno to process every operation on every resource; a policy matching only `Pod` adds no load when no Pods are sent. Set requests and limits from your own tests; the page recommends no CPU limits.

Admission controller: replicas share AdmissionReview load but do not partition policies, and each replica caches all policies, so memory grows with policy count. Count active policies with `kyverno_policy_rule_info_total`. Prefer fewer, broader policies plus Global Context to thousands of near-identical `Policy` resources.

Published numbers (their test setups):
- Legacy ClusterPolicy (pre-v1.14), 17 Enforce policies on Pods, 1 replica: 100 VUs 37.71 ms average; 500 VUs 92.73 ms average, 3.15 s max.
- CEL policies (v1.18.1), 16 ValidatingPolicies at 500 VUs: p99 1,247 ms on 1 replica, 649 ms on 3. One MutatingPolicy at 500 VUs: p99 427 ms on 1 replica.
- Alert `KyvernoAdmissionHighLatency` fires at p99 above 1 s for 5 minutes.
- Reports controller, 16 PSS policies: 1,284 PolicyReports used 373 MB etcd; 10,254 used 483 MB.

Caveats:
- Thousands of policies can require extra kube-apiserver memory headroom, or the cluster may crash.
- With `failurePolicy: Fail`, losing all replicas to OOM blocks matching admission cluster-wide until one recovers.
- Client rate-limit flags are not covered on this page (see the configuration skill).

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
