---
id: computing-software.devops-ci-cd.helm.resource-policy-keep
name: resource-policy-keep
category: computing-software
field: devops-ci-cd
product: helm
tags: [resource-policy, keep, annotation, uninstall, pvc, orphan]
level: practitioner
status: docs-checked
description: "Use the helm.sh/resource-policy: keep annotation so a resource survives helm uninstall, and what it costs."
sources:
  - https://helm.sh/docs/howto/charts_tips_and_tricks/
  - https://helm.sh/docs/helm/helm_uninstall/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Chart developers add an annotation to a resource so Helm skips deleting it:

```yaml
kind: Secret
metadata:
  annotations:
    helm.sh/resource-policy: keep
```

The annotation tells Helm to skip deleting the resource when a Helm operation (such as `helm uninstall`, `helm upgrade` or `helm rollback`) would result in its deletion. The resource is then orphaned: Helm no longer manages it in any way. Consequences from the docs:

- It can cause problems with `helm install --replace` on a release that was already uninstalled but kept resources.
- Because Helm no longer tracks the kept resource, removing it later is up to you (for example with `kubectl delete`).
- `helm uninstall --keep-history` is a different feature: it removes all associated resources, marks the release as deleted and retains the release history. By default `helm uninstall` removes the resources of the last release and the release history.

Typical use (judgement, not from the docs): PersistentVolumeClaims, generated Secrets and similar data you do not want lost by a mistaken uninstall.

## Checked

2026-11-08. Checked against the Helm tips-and-tricks page (helm.sh/resource-policy: keep) and the uninstall command page. Removed unsourced claims.

Method: documentation only; no commands were run.
