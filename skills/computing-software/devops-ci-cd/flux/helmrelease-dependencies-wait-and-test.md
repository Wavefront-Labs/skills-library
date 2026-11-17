---
id: computing-software.devops-ci-cd.flux.helmrelease-dependencies-wait-and-test
name: helmrelease-dependencies-wait-and-test
category: computing-software
field: devops-ci-cd
product: flux
tags: [helmrelease, dependson, waitstrategy, helm-test, kstatus]
level: sme
status: docs-checked
description: "Order HelmReleases, choose the poller or legacy wait strategy, and run Helm tests after install or upgrade."
sources:
  - https://fluxcd.io/flux/components/helm/helmreleases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Ordering: `.spec.dependsOn` lists other HelmReleases that must be Ready (condition `Ready` is `True`) before this one proceeds, for example CRDs and their controller before dependent workloads.

```yaml
spec:
  dependsOn:
    - name: backend
      namespace: default
```

Waiting: `.spec.waitStrategy.name` is `poller` (kstatus polling of resource statuses, the default) or `legacy` (Helm v3 wait logic, the default when the `UseHelm3Defaults` feature gate is on). Install and upgrade offer `disableWait` and `disableWaitForJobs` to skip waiting. Custom resources without kstatus support can be covered with `.spec.healthCheckExprs` using CEL.

Tests: set `.spec.test.enable: true` to run the chart Helm tests after a successful install or upgrade. Results appear in `.status.history` and as Events. Test failures count as release failures and trigger remediation unless `.spec.test.ignoreFailures: true`, which can be overridden per install or upgrade action.

```yaml
spec:
  test:
    enable: true
    ignoreFailures: false
```

Release identity: `.spec.releaseName` defaults to `[<targetNamespace>-]<name>` and is shortened with a SHA-256 hash past 53 characters. Changing release name, target namespace or storage namespace on an installed release uninstalls it and installs a new one, it does not rename or move it.

## Checked

2026-11-03. Read the HelmRelease reference (fluxcd.io/flux/components/helm/helmreleases/): `dependsOn` Ready semantics, `waitStrategy.name` poller/legacy and the `UseHelm3Defaults` gate, `disableWaitForJobs`, `healthCheckExprs`, `.spec.test.enable` and `ignoreFailures`, `releaseName` default and 53-character SHA-256 shortening, and the uninstall-and-reinstall warnings. Nothing removed.

Method: documentation only; no commands were run.
