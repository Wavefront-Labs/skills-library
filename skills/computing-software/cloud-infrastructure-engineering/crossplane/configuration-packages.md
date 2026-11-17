---
id: computing-software.cloud-infrastructure-engineering.crossplane.configuration-packages
name: configuration-packages
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [configuration, package, xpkg, revision, dependencies]
level: practitioner
status: docs-checked
description: "Install and manage Configuration packages that bundle Compositions, XRDs and dependencies."
sources:
  - https://docs.crossplane.io/latest/packages/configurations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Configuration is an OCI image holding Compositions, XRDs and the Providers and Functions they need, making a platform portable.

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Configuration
metadata:
  name: configuration-quickstart
spec:
  package: xpkg.crossplane.io/crossplane-contrib/configuration-quickstart:v0.1.0
```

At Helm install: `--set configuration.packages='{xpkg.crossplane.io/crossplane-contrib/configuration-quickstart:v0.1.0}'`.

Crossplane installs the contents plus dependencies. It supports digests, and the same options as providers:

- `packagePullPolicy`: `IfNotPresent` (default), `Always`, `Never`.
- `revisionActivationPolicy`: `Automatic` (default) or `Manual`.
- `revisionHistoryLimit`: default `1`.
- `packagePullSecrets`: for private registries.
- `skipDependencyResolution: true`: you must then install required Providers yourself.

Installing a newer version creates a `ConfigurationRevision`. List them with `kubectl get configurationrevisions`; columns show HEALTHY, REVISION, STATE and dependency counts. Only the Active revision supplies the Compositions and XRDs.

Installs come only from a container registry, not Kubernetes volumes.

A Configuration is the unit to version and ship a platform: build it with `crossplane xpkg build`, push it to a registry, and install the tag in each cluster. Dependencies declared in the package are installed automatically unless you skip resolution.

## Checked

Checked against the Configurations page, read in full: install manifest, Helm flag, digests, pull policy, activation policy, revision history, pull secrets, skipDependencyResolution, revisions listing, registry-only installs, xpkg build.

Method: docs-checked 2026-11-09 against the packages/configurations page (docs repo raw markdown).
