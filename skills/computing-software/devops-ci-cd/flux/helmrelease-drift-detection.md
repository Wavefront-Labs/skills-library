---
id: computing-software.devops-ci-cd.flux.helmrelease-drift-detection
name: helmrelease-drift-detection
category: computing-software
field: devops-ci-cd
product: flux
tags: [helmrelease, driftdetection, drift-correction, ignore-rules, hpa]
level: advanced
status: docs-checked
description: "Detect or correct cluster drift from the Helm storage manifest with spec.driftDetection mode warn or enabled and ignore rules."
sources:
  - https://fluxcd.io/flux/components/helm/helmreleases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Drift detection is a field on the HelmRelease, `.spec.driftDetection.mode`. When the release is in sync with Helm storage and the mode is `warn` or `enabled`, helm-controller compares the stored manifest to the cluster with a server-side dry-run apply. On drift it emits a Kubernetes Event with a short summary; a fuller JSON Patch summary goes to the logs at `--log-level=debug`.

With `enabled`, it also corrects drift by creating and patching resources from the dry-run result, then emits an Event summarising changes and failures. After a failed attempt it keeps trying until the desired state is reached or a new Helm action starts, such as after a spec change.

Ignore fields another controller owns, for example replicas under an HPA or fields mutated by chart hooks:

```yaml
spec:
  driftDetection:
    mode: enabled
    ignore:
      - paths: ["/spec/replicas"]
        target:
          kind: Deployment
```

`paths` are JSON Pointers. Without `target` the rule applies to all resources of the release. A pointer to the whole document (`""`) ignores a resource entirely, equivalent to the ignore annotation.

Start with `warn` to see what would change before turning correction on, because correction can overwrite changes made by operators or other tools.

Check Events with `kubectl events --for helmrelease/NAME` and watch for the summary lines.

## Checked

2026-11-03. Read the HelmRelease reference (fluxcd.io/flux/components/helm/helmreleases/): `.spec.driftDetection` modes warn and enabled, server-side dry-run comparison, Event summary and JSON Patch at `--log-level=debug`, ignore paths as JSON Pointers; `kubectl events --for` checked on the Kubernetes kubectl events reference. Removed the Flux v2.2.0 version claim, which the page does not state.

Method: documentation only; no commands were run.
