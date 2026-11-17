---
id: computing-software.cloud-infrastructure-engineering.linkerd.install-extensions
name: install-extensions
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, extensions, viz, multicluster]
level: practitioner
status: docs-checked
description: "Install built-in and third-party Linkerd extensions in their own namespaces after validating the control plane."
sources:
  - https://linkerd.io/2.19/tasks/extensions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Extensions add functionality to a Linkerd installation. The built-in ones are viz (metrics and visibility) and multicluster (cross-cluster routing).

Before installing, install Linkerd and validate with `linkerd check`. Then run the extension's install command:

```bash
linkerd viz install | kubectl apply -f -
```

Built-in extensions can also be installed with their Helm charts. Once installed, an extension is included in the standard `linkerd check` output.

Rules:

- Extensions get their own namespace, which is the recommended practice. Installing extensions in the `linkerd` namespace is not supported.
- Third-party extensions need one more step: download the extension's CLI and put it on your path, so that you can invoke the extension through the Linkerd CLI, as in `linkerd foo`.

To list extensions, run `kubectl get ns -l linkerd.io/extension`. To remove one, every extension has an `uninstall` command, for example `linkerd foo uninstall | kubectl delete -f -`.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/extensions/.

Removed or reworded: Removal/upgrade ordering and per-extension check claims.

Method: documentation only; no commands were run.
