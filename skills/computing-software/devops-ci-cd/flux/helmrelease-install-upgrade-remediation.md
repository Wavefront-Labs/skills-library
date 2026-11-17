---
id: computing-software.devops-ci-cd.flux.helmrelease-install-upgrade-remediation
name: helmrelease-install-upgrade-remediation
category: computing-software
field: devops-ci-cd
product: flux
tags: [helmrelease, remediation, retries, rollback, uninstall]
level: advanced
status: docs-checked
description: "Configure automatic rollback or uninstall with retries for failed Helm installs and upgrades, plus retry strategies."
sources:
  - https://fluxcd.io/flux/components/helm/helmreleases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a failed install, upgrade or Helm test leaves the release failed. Set remediation to act automatically.

```yaml
spec:
  install:
    remediation:
      retries: 3
  upgrade:
    remediation:
      retries: 3
      strategy: rollback
      remediateLastFailure: true
```

How it works: on failure the controller remediates (rollback or uninstall), then retries, until `retries` are exhausted or the action succeeds. Then it stops and the release stays failed, unless `remediateLastFailure: true` restores the last good state or uninstalls. For upgrades that defaults to `true` when retries is above 0.

Upgrade `strategy` is `rollback` (default) or `uninstall`, which reinstalls afterwards. `retries` defaults to 0; a negative value retries forever. `ignoreTestFailures` skips remediation on Helm test failures.

Install and upgrade also accept `strategy.name`: `RemediateOnFailure` (default) or `RetryOnFailure`, which retries a failed install as an upgrade after `retryInterval` (default 5m, not allowed with RemediateOnFailure). The `DefaultToRetryOnFailure` feature gate flips the default.

Tuning blocks: `.spec.rollback` (timeout, cleanupOnFail, disableHooks, disableWait, force) applies to rollback remediation; `.spec.uninstall` (timeout, deletionPropagation, keepHistory) applies to uninstall remediation.

A new chart version or changed config resets failure counters. To restart exhausted retries, use the reset annotation.

## Checked

2026-11-03. Read the HelmRelease reference (fluxcd.io/flux/components/helm/helmreleases/): install and upgrade `remediation` fields (retries, strategy, remediateLastFailure defaults, ignoreTestFailures), `strategy.name` RemediateOnFailure/RetryOnFailure with `retryInterval` 5m and the `DefaultToRetryOnFailure` gate, the rollback and uninstall blocks, and the counter reset on new chart or config. Nothing removed.

Method: documentation only; no commands were run.
