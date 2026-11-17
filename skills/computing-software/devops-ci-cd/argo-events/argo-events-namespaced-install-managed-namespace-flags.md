---
id: computing-software.devops-ci-cd.argo-events.argo-events-namespaced-install-managed-namespace-flags
name: argo-events-namespaced-install-managed-namespace-flags
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, namespaced, managed-namespace, controller-manager, rbac, install]
level: advanced
status: docs-checked
description: "Run the Argo Events controller in namespaced mode and point it at a different managed namespace with the right flags per version."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/managed-namespace.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events namespaced install managed namespace flags

Argo Events installs cluster-scoped (ClusterRole) or namespace-scoped (normal Role) for the service account `argo-events-sa`.

From v1.7, in a namespace-scoped install the `controller-manager` Deployment must run with `--namespaced`. To make it watch a separate namespace add `--managed-namespace`:

```yaml
args:
  - --namespaced
  - --managed-namespace
  - default
```

Before v1.7 there were three controller Deployments (`eventbus-controller`, `eventsource-controller`, `sensor-controller`), and `--namespaced` had to be added to each of them (and the managed namespace flag similarly to each).

## Checked

2026-11-04. Confirmed against the Managed Namespace page: cluster-scoped versus namespace-scoped setup with ClusterRole or Role for `argo-events-sa`, `--namespaced` and `--managed-namespace` on the `controller-manager` Deployment from v1.7, and the three separate controller Deployments before v1.7. Removed claims about the `namespace-install.yaml` roles being reusable across namespaces and the service account being `argo-events-sa` in both modes (the Installation page uses the `default` service account for the OpenShift namespace install), plus "runs everything", none of which this page states.
Method: documentation only; no commands were run.
