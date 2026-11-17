---
id: computing-software.cloud-infrastructure-engineering.crossplane.provider-deletion-protection
name: provider-deletion-protection
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [provider, deletion-protection, clusterusage, feature-flag]
level: advanced
status: docs-checked
description: "Enable provider deletion protection so a Provider with live managed resources cannot be deleted."
sources:
  - https://docs.crossplane.io/latest/packages/providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An alpha feature. Enable it with `--enable-provider-deletion-protection`; it also needs Usages (on by default).

```shell
helm upgrade --install crossplane crossplane-stable/crossplane \
  --namespace crossplane-system \
  --set args='{"--enable-provider-deletion-protection"}'
```

Crossplane watches the managed resources of each Provider. While any of a type exist it creates a `ClusterUsage` blocking deletion of the Provider, with a reason such as `Provider has active managed resources of type VPC.ec2.aws.upbound.io`. When the last of that type goes, it removes the ClusterUsage.

Find them by label:

```shell
kubectl get clusterusages -l crossplane.io/provider-protection=true
```

Names are a hash of the MRD name. Labels `pkg.crossplane.io/package` and `apiextensions.crossplane.io/mrd` identify the Provider and the type.

Deleting a protected Provider fails at the admission webhook `nousages.protection.crossplane.io` with an "in-use by N usage(s)" error.

To delete the Provider, first remove all its managed resources, or manually delete the protecting `ClusterUsage`.

The feature needs Usages enabled (on by default). Crossplane removes a ClusterUsage automatically when no managed resources of its type remain.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Providers page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the --enable-usages=false flag claim.

Method: documentation only; no commands were run.
