---
id: computing-software.cloud-infrastructure-engineering.crossplane.disable-unused-managed-resources
name: disable-unused-managed-resources
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [mrd, mrap, crd-scaling, selective-activation, workflow]
level: practitioner
status: docs-checked
description: "Workflow to install a large provider but activate only the managed resources you need."
sources:
  - https://docs.crossplane.io/latest/guides/disabling-unused-managed-resources/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Steps for a provider with the `safe-start` capability:

1. Remove automatic activation. At install: `--set provider.defaultActivations={}`. On an existing cluster: `kubectl delete managedresourceactivationpolicy default`.
2. Install the provider normally. Crossplane converts its CRDs into inactive MRDs. Wait with `kubectl wait --for=condition=Healthy provider/provider-aws-ec2 --timeout=5m`.
3. Confirm all MRDs are inactive:

```shell
kubectl get mrds -o jsonpath='{.items[*].spec.state}' | tr ' ' '\n' | sort | uniq -c
```

4. Check no CRDs exist yet, for example `kubectl get crds | grep ec2.aws.m.crossplane.io` returns nothing.
5. Create a ManagedResourceActivationPolicy listing only needed resources, such as `instances`, `securitygroups` and `vpcs`.
6. Verify with `kubectl get mrds -o jsonpath='{range .items[*]}{.metadata.name}: {.spec.state}{"\n"}{end}' | grep Active` and by counting CRDs again.

The guide's example drops from about 200 CRDs (roughly 600 MiB of API server memory at 3 MiB each) to 3.

MRDs and MRAPs need Crossplane v2 or later.

Run the CRD count before and after activation to prove the saving, and re-run it whenever you add a policy entry.

## Checked

Steps, commands, the safe-start requirement and the 200 to 3 CRD example confirmed on the guide. The guide marks MRDs and MRAPs as alpha features in Crossplane v2.0 and later.

Method: docs-checked 2026-11-09 against the raw Disabling Unused Managed Resources guide (docs repo, current content folder), read in full.
