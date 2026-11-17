---
id: computing-software.cloud-infrastructure-engineering.kubernetes.openfeature-flags-vs-deployment-strategies
name: openfeature-flags-vs-deployment-strategies
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, deployment-strategies, openfeature, feature-flags, flagd, progressive-delivery]
level: practitioner
status: docs-checked
description: "Decide when to use feature flags (OpenFeature with flagd on Kubernetes) instead of canary or blue-green deployments, and run flagd with the OpenFeature Operator."
sources: ["https://openfeature.dev/docs/reference/intro", "https://github.com/open-feature/go-sdk", "https://github.com/open-feature/open-feature-operator/tree/main/docs", "https://flagd.dev/reference/flag-definitions/", "https://github.com/open-feature/flagd/blob/main/docs/reference/flag-definitions.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Feature flags with OpenFeature vs deployment strategies

## Which tool for which risk
| Need | Use |
|---|---|
| Test a new build (crashes, latency, memory) on a slice of traffic | canary or blue-green |
| Turn a feature on for some users, independent of deploys | feature flag |
| Instant off switch for a feature without redeploying | feature flag (kill switch) |
| Schema or infra changes | neither alone; expand-contract migrations |
Flags decouple deploy from release; canaries make deploys safe. Most teams use both.

## OpenFeature
A vendor-neutral flag-evaluation API with SDKs for several languages and pluggable providers
(for example flagd). Go example:
```go
client := openfeature.NewClient("checkout")
enabled := client.Boolean(ctx, "new-checkout", false, openfeature.NewEvaluationContext(userID, map[string]any{"country": "DE"}))
```

## flagd on Kubernetes (OpenFeature Operator)
```yaml
apiVersion: core.openfeature.dev/v1beta1
kind: FeatureFlag
metadata: {name: checkout-flags, namespace: shop}
spec:
  flagSpec:
    flags:
      new-checkout:
        state: ENABLED
        variants: {"on": true, "off": false}
        defaultVariant: "off"
        targeting: {if: [{in: [{var: country}, [DE, NL]]}, "on", "off"]}
---
apiVersion: core.openfeature.dev/v1beta1
kind: FeatureFlagSource
metadata: {name: checkout-source, namespace: shop}
spec:
  sources: [{source: shop/checkout-flags, provider: kubernetes}]   # namespace/name of the FeatureFlag
```
Annotate the workload's pod template:
```yaml
annotations:
  openfeature.dev/enabled: "true"
  openfeature.dev/featureflagsource: "checkout-source"
```
The operator injects a flagd sidecar (port set by the FeatureFlagSource `port`); the app's flagd
provider talks to it on localhost. `openfeature.dev/featureflagsource` takes a comma-separated
list.

## Hygiene
Every flag has an owner and removal date; stale flags become permanent branches in code.

## Verify
Editing the FeatureFlag `defaultVariant` changes app behaviour without a rollout.

## Checked
2026-10-27, against the OpenFeature Operator docs (open-feature/open-feature-operator main: `feature_flag.md`, `feature_flag_source.md`, `annotations.md`), the flagd flag-definition reference (open-feature/flagd main) and the OpenFeature Go SDK README. Confirmed: `core.openfeature.dev/v1beta1` `FeatureFlag` with `spec.flagSpec.flags` (`state`, `variants`, `defaultVariant`, `targeting`), `FeatureFlagSource` `sources[].source`/`provider: kubernetes` and `port`, the `openfeature.dev/enabled` and `openfeature.dev/featureflagsource` annotations, JsonLogic `if`/`in`/`var` targeting, and the Go `NewClient`, `NewEvaluationContext`, `client.Boolean` API.
Method: documentation only; no commands were run.
