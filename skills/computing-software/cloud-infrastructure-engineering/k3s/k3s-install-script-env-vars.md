---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-install-script-env-vars
name: k3s-install-script-env-vars
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, install-k3s-exec, install-k3s-version, install-k3s-channel]
level: practitioner
status: docs-checked
description: "Reference of the INSTALL_K3S_* environment variables that control the get.k3s.io installer."
sources:
  - https://docs.k3s.io/reference/env-variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune the install script without editing it. Place variables after the pipe:

```
curl -sfL https://get.k3s.io | INSTALL_K3S_CHANNEL=latest sh -
```

Variables from the docs:

- INSTALL_K3S_SKIP_DOWNLOAD: true means do not download the K3s hash or binary.
- INSTALL_K3S_SYMLINK: by default creates symlinks for kubectl, crictl and ctr if they are not already in the path; `skip` creates none, `force` overwrites.
- INSTALL_K3S_SKIP_ENABLE: true means do not enable or start the service.
- INSTALL_K3S_SKIP_START: true means do not start the service.
- INSTALL_K3S_VERSION: version to download from GitHub; if unset it uses the stable channel.
- INSTALL_K3S_BIN_DIR: where to put the binary, links and uninstall script; default /usr/local/bin.
- INSTALL_K3S_BIN_DIR_READ_ONLY: true writes no files to the bin dir and forces INSTALL_K3S_SKIP_DOWNLOAD=true.
- INSTALL_K3S_SYSTEMD_DIR: default /etc/systemd/system.
- INSTALL_K3S_EXEC: command and flags for the service. With K3S_URL set it defaults to agent, otherwise server.
- INSTALL_K3S_NAME: systemd service name; default k3s (server) or k3s-agent (agent); a custom name is prefixed with k3s-.
- INSTALL_K3S_TYPE: systemd service type.
- INSTALL_K3S_SELINUX_WARN: true continues if the k3s-selinux policy is not found.
- INSTALL_K3S_SKIP_SELINUX_RPM: true skips automatic k3s RPM install.
- INSTALL_K3S_CHANNEL_URL: default https://update.k3s.io/v1-release/channels.
- INSTALL_K3S_CHANNEL: stable (default), latest or testing.

## Checked

2026-11-03: read docs.k3s.io reference/env-variables. Confirmed: the INSTALL_K3S_* variable list, the defaults for BIN_DIR, SYSTEMD_DIR, CHANNEL (stable) and CHANNEL_URL, the INSTALL_K3S_EXEC and INSTALL_K3S_NAME default rules, and the SYMLINK skip/force values.

Method: documentation only; no commands were run.
