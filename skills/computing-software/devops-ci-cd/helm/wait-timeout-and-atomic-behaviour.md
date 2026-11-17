---
id: computing-software.devops-ci-cd.helm.wait-timeout-and-atomic-behaviour
name: wait-timeout-and-atomic-behaviour
category: computing-software
field: devops-ci-cd
product: helm
tags: [wait, timeout, rollback-on-failure, wait-for-jobs, atomic, readiness, watcher]
level: advanced
status: docs-checked
description: "Helm 4 wait strategies (watcher, hookOnly, legacy), --timeout, --wait-for-jobs and --rollback-on-failure."
sources:
  - "https://helm.sh/docs/helm/helm_install/"
  - "https://helm.sh/docs/helm/helm_upgrade/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Install and upgrade can block until resources are ready.

- `--wait`: Helm 4 takes a strategy: `watcher`, `hookOnly` or `legacy`. The default is `hookOnly`, which only waits for hooks. `watcher` uses status watching of resources (the modern path); `legacy` is the older polling behaviour.
- `--wait-for-jobs`: also wait until all Jobs complete.
- `--timeout DURATION`: time to wait for any individual Kubernetes operation, such as a Job for hooks. Default `5m0s`.
- `--rollback-on-failure`: if the install or upgrade fails, roll back (upgrade) or uninstall (install). `--wait` defaults to the `watcher` strategy when it is set.
- `--cleanup-on-fail` (upgrade): delete new resources created in this upgrade when it fails.

```bash
helm upgrade --install app ./chart --wait=watcher --timeout 10m --rollback-on-failure
```

## Checked

2026-11-03. Confirmed against the helm install, upgrade and rollback reference pages on helm.sh (--wait strategies and hookOnly default, --wait-for-jobs, --timeout 5m0s, --rollback-on-failure, --cleanup-on-fail). Removed: the claim that it replaces `--atomic`, the failed-status and shorter-output remarks, and the list of resource kinds waited on (not on the pages).
Method: documentation only; no commands were run.

