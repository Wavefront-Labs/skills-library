---
id: computing-software.cloud-infrastructure-engineering.crossplane.provider-install-options
name: provider-install-options
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [provider, package, pull-policy, digest, pull-secrets]
level: practitioner
status: docs-checked
description: "Install a Provider and set its package options: digest, pull policy, activation, history, pull secrets and dependencies."
sources:
  - https://docs.crossplane.io/latest/packages/providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install:

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: crossplane-contrib-provider-aws-s3
spec:
  package: xpkg.crossplane.io/crossplane-contrib/provider-aws-s3:v2.0.0
```

Or at Helm install: `--set provider.packages='{xpkg.crossplane.io/crossplane-contrib/provider-aws-s3:v2.0.0}'`.

Options under `spec`:

- Use `@sha256:...` instead of a tag for repeatable installs.
- `packagePullPolicy`: `IfNotPresent` (default), `Always` (checks every minute), `Never`.
- `revisionActivationPolicy`: `Automatic` (default) or `Manual`.
- `revisionHistoryLimit`: integer, default `1`.
- `packagePullSecrets`: list of secrets in the Crossplane namespace. They are not passed to dependencies.
- `skipDependencyResolution: true` ignores package dependencies.
- `ignoreCrossplaneConstraints: true` installs despite a Crossplane version requirement.

Offline installs need a container registry such as Harbor; volumes are not supported.

Check status with `kubectl get providers` (INSTALLED, HEALTHY). If HEALTHY is False, run `kubectl describe providerrevisions` and read the events, such as an incompatible Crossplane version.

Delete a Provider with `kubectl delete provider` only after its managed resources are gone, or they may be abandoned.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Providers page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the ImageConfig rewrite and pin-in-production advice.

Method: documentation only; no commands were run.
