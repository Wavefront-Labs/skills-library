---
id: computing-software.database-administration.dragonfly.operator-install-and-scale
name: operator-install-and-scale
category: computing-software
field: database-administration
product: dragonfly
tags: [kubernetes-operator, operator-install, replicas, dragonfly-resource]
level: practitioner
status: docs-checked
description: "Install the Dragonfly Kubernetes operator and create a Dragonfly resource with replicas, args and resources."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/operator/installation.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/operator/dragonfly-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install the operator:

```bash
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
```

It runs in the `dragonfly-operator-system` namespace.

Create instances with a `Dragonfly` resource. Key spec fields:

- `replicas`: total instances including the primary; `1` is a primary only, `2` is a primary plus one replica, and there is always one primary.
- `args`: extra Dragonfly server flags.
- `resources`: CPU and memory requests/limits.
- `authentication.passwordFromSecret`: password from a Secret.
- `tlsSecretRef`: Secret for TLS connections, in the same namespace.
- `snapshot.cron`, `snapshot.persistentVolumeClaimSpec`: snapshot schedule and PVC.
- `serviceAccountName`, `aclFromSecret` (since v1.1.1), `skipFSGroup` (since v1.1.2), `memcachedPort` (since v1.1.2).

Scale with `kubectl patch dragonfly <name> --type merge -p '{"spec":{"replicas":5}}'` or by editing `spec.replicas` and re-applying.

## Checked

2026-11-04. Confirmed in the Operator installation and Dragonfly Configuration pages: install manifest URL, namespace, replicas semantics, field names and since-versions. Removed `snapshot.dir` and the Secret key names `tls.crt`/`tls.key`, which neither page states.

Method: documentation only; no commands were run.
