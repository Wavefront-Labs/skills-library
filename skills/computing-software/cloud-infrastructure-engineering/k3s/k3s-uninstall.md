---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-uninstall
name: k3s-uninstall
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, k3s-uninstall-sh, k3s-agent-uninstall-sh]
level: intro
status: docs-checked
description: "Remove K3s from server or agent nodes with the generated uninstall scripts and understand what data is deleted."
sources:
  - https://docs.k3s.io/installation/uninstall
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: remove K3s from a host that was installed with the install script.

Warning from the docs: uninstalling K3s may cause data loss.

Server node:

```
/usr/local/bin/k3s-uninstall.sh
```

Agent node:

```
/usr/local/bin/k3s-agent-uninstall.sh
```

These scripts are generated during installation. Running one:

- stops K3s and all running pods;
- deletes the local cluster datastore, Local Storage persistent volume data, node configuration, and all of the scripts and CLI tools.

It does not remove data from external datastores, or data created by pods that use external Kubernetes persistent volumes.

Rejoining: if you plan to rejoin the node to an existing cluster after uninstalling and reinstalling, delete the node from the cluster first so the node password secret is removed (see the Node Registration documentation).

## Checked

2026-11-08. Read the full K3s Uninstalling K3s page (docs/installation/uninstall.md in the k3s-io/docs repo). Confirmed: the data-loss warning, both script paths, what the scripts stop and delete, external datastores and external persistent volumes untouched, and deleting the node first to remove the node password secret. Removed the INSTALL_K3S_BIN_DIR sentence and the k3s-killall.sh contrast (neither is on the page).

Method: documentation only; no commands were run.
