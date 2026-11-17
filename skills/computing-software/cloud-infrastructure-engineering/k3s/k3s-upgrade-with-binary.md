---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-upgrade-with-binary
name: k3s-upgrade-with-binary
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, binary-upgrade, usr-local-bin-k3s, drain-cordon]
level: practitioner
status: docs-checked
description: "Upgrade K3s by replacing the binary and restarting the k3s or k3s-agent service."
sources:
  - https://docs.k3s.io/upgrades/manual
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manual upgrade without the install script.

Steps:

1. Download the desired K3s binary from the GitHub releases page.
2. Copy it to /usr/local/bin/k3s (or wherever your binary lives).
3. Restart the k3s or k3s-agent service, or restart the k3s process if you run the binary directly.

Upgrade servers first, one at a time, then agents.

Note: pod containers keep running while K3s is stopped, so it is generally safe to restart K3s without draining pods and cordoning the node. If your workload is sensitive to brief API server outages, drain and cordon the node with kubectl before restarting K3s, and uncordon it afterwards.


Do not skip minor versions of Kubernetes when upgrading: the Kubernetes version skew policy applies.

## Checked

2026-11-08. Read the full K3s Manual Upgrades page (docs/upgrades/manual.md in the k3s-io/docs repo). Confirmed: the three binary upgrade steps, servers first one at a time then agents, containers continuing while K3s is stopped, drain and cordon advice, and the version skew policy. Removed the stop/start command line and the rollback snapshot advice (not on the page).

Method: documentation only; no commands were run.
