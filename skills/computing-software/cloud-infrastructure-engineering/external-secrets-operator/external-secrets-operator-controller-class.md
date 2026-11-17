---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-controller-class
name: external-secrets-operator-controller-class
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [controllerclass, multi-controller, secretstore, helm]
level: advanced
status: docs-checked
description: "Run several ESO controllers side by side by assigning controller classes to SecretStores (experimental)."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/controller-class.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Experimental and not highly tested. A controller class lets multiple controllers share a cluster by splitting which stores each handles. Install with a class and mark stores:

```bash
helm install custom-external-secrets external-secrets/external-secrets --set controllerClass=custom
```

and set `spec.controller` on the `SecretStore` to the same value. ExternalSecrets bound to that store are then processed by that controller. If an ExternalSecret references several stores (including `sourceRef` overrides in `data[]` or `dataFrom[]`), a controller skips it when any referenced store belongs to another class.

A store with no `spec.controller` is valid for every controller, and the same applies to ClusterSecretStores. Skipped ExternalSecrets are retried after the controller's requeue interval (one hour if unset), even with a refresh interval of zero, so class changes are picked up.

## Checked

2026-11-03. Claims were read against guides/controller-class.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
