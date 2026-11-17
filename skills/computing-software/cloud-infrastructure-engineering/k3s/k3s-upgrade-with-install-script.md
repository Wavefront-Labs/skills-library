---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-upgrade-with-install-script
name: k3s-upgrade-with-install-script
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, upgrade, install-k3s-version, install-k3s-skip-start]
level: practitioner
status: docs-checked
description: "Upgrade K3s by re-running the install script with the same configuration, servers first one at a time."
sources:
  - https://docs.k3s.io/upgrades/manual
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Order: upgrade server nodes first, one at a time, then agents.

Re-run the script with the same options you originally used:

```
curl -sfL https://get.k3s.io | <EXISTING_K3S_ENV> sh -s - <EXISTING_K3S_ARGS>
```

Pick a channel or version:

```
curl -sfL https://get.k3s.io | INSTALL_K3S_CHANNEL=latest <EXISTING_K3S_ENV> sh -s - <EXISTING_K3S_ARGS>
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=vX.Y.Z+k3s1 <EXISTING_K3S_ENV> sh -s - <EXISTING_K3S_ARGS>
```

The script downloads the new binary, updates the systemd unit or openrc init script to reflect the arguments passed, and restarts the service. To download without starting, set INSTALL_K3S_SKIP_START=true.

Failure mode: INSTALL_K3S_EXEC, K3S_ variables and trailing shell arguments generate the unit and env file. If you set configuration originally but not on the re-run, the original values are lost. The config file (/etc/rancher/k3s/config.yaml) is not managed by the script, so prefer it for independence.

The script does not drain or cordon the node. Pod containers keep running while K3s restarts, but if workloads are sensitive to brief API server outages, drain and cordon first and uncordon afterwards.

Do not skip minor versions: the Kubernetes version skew policy applies.

## Checked

2026-11-03: read docs.k3s.io upgrades/manual. Confirmed: re-running the install script with INSTALL_K3S_CHANNEL or INSTALL_K3S_VERSION, the unit/init-script update, INSTALL_K3S_SKIP_START and the version skew policy.

Method: documentation only; no commands were run.
