---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-install-script-flags-vs-config
name: k3s-install-script-flags-vs-config
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, install-k3s-exec, flags, reinstall]
level: practitioner
status: docs-checked
description: "Pass K3s flags through the install script five equivalent ways and avoid losing settings when re-running it."
sources:
  - https://docs.k3s.io/installation/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand how the install script persists configuration.

INSTALL_K3S_EXEC, K3S_ environment variables and trailing shell arguments are persisted into the service configuration. After install, you can edit the env file, edit the service configuration, or re-run the installer with new options.

These all register a server with no flannel and a token:

```
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server" sh -s - --flannel-backend none --token 12345
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --flannel-backend none" K3S_TOKEN=12345 sh -s -
curl -sfL https://get.k3s.io | K3S_TOKEN=12345 sh -s - server --flannel-backend none
curl -sfL https://get.k3s.io | sh -s - --flannel-backend none --token 12345
```

The agent equivalents include `K3S_URL=https://k3s.example.com K3S_TOKEN=mypassword sh -s -` (agent assumed because of K3S_URL) and `INSTALL_K3S_EXEC="agent --server https://k3s.example.com --token mypassword"`.

Failure mode: if you set configuration on first run but not on a re-run, the original values are lost. The config file is not managed by the install script, so use /etc/rancher/k3s/config.yaml if you want configuration independent of the installer.

Binary and image: the plain binary takes the same settings (`K3S_KUBECONFIG_MODE="644" k3s server` or `k3s server --write-kubeconfig-mode=644`), and the docker.io/rancher/k3s image supports the same methods. Use `--help` to see options and matching environment variables.

## Checked

2026-11-03: read docs.k3s.io installation/configuration. Confirmed: the four equivalent server install variants, the agent variants, the persisted-configuration failure mode and the binary and image usage.

Method: documentation only; no commands were run.
