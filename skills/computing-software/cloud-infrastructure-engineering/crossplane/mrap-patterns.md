---
id: computing-software.cloud-infrastructure-engineering.crossplane.mrap-patterns
name: mrap-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [mrap, activation-policy, wildcard, helm, default-activations]
level: practitioner
status: docs-checked
description: "Activate MRDs by exact name or leading-wildcard patterns with ManagedResourceActivationPolicy."
sources:
  - https://docs.crossplane.io/latest/managed-resources/managed-resource-activation-policies/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `ManagedResourceActivationPolicy` lists patterns in `spec.activate`. Crossplane lists MRDs, matches names, sets matching MRDs to `Active` and records the activated list in status. MRDs added later that match activate automatically.

```yaml
apiVersion: apiextensions.crossplane.io/v1alpha1
kind: ManagedResourceActivationPolicy
metadata:
  name: aws-core-resources
spec:
  activate:
  - buckets.s3.aws.m.crossplane.io
  - "*.ec2.aws.m.crossplane.io"
```

Matching rules:

- Use the plural in exact names: `buckets`, not `bucket`.
- Only a leading `*` is supported. `s3.*.aws.m.crossplane.io` and `*.s3.*` are invalid. Quote patterns that start with `*`.
- `.m.crossplane.io` domains are modern namespaced MRs; names without `.m` are legacy cluster-scoped ones.

The Helm chart creates a policy named `default` that activates `"*"`. Change it at install:

```shell
helm install crossplane crossplane-stable/crossplane \
  --set provider.defaultActivations={}
```

Or pass specific patterns in that value. Multiple policies can coexist.

Policies are additive: an MRD is active if any policy matches it.
Wildcard examples that are valid: `"*.s3.aws.m.crossplane.io"` for every S3 resource, and `"*"` for all. Inspect results with `kubectl get mrds` and `kubectl describe managedresourceactivationpolicy NAME`.

## Checked

Activation flow, exact and prefix-wildcard matching rules, legacy versus modern domains, the Helm default policy and additive policies confirmed on the page. A claim that deleting a policy never deactivates MRDs was removed because the page does not state it.

Method: docs-checked 2026-11-09 against the raw Managed Resource Activation Policies page (docs repo, current content folder), read in full.
