---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-config-file-yaml
name: k3s-config-file-yaml
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, config-yaml, config-yaml-d, k3s-config-file]
level: practitioner
status: docs-checked
description: "Configure K3s with /etc/rancher/k3s/config.yaml, how CLI flags map to keys, and precedence against flags."
sources:
  - https://docs.k3s.io/installation/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep K3s configuration in a file independent of the installer.

The config file is loaded however K3s is installed or run. Defaults:

- /etc/rancher/k3s/config.yaml
- drop-ins in /etc/rancher/k3s/config.yaml.d/*.yaml, loaded alphabetically

Both are configurable via the --config flag or K3S_CONFIG_FILE variable; overriding the file name also changes the drop-in directory path.

Example:

```
write-kubeconfig-mode: "0644"
tls-san:
  - "foo.local"
node-label:
  - "foo=bar"
  - "something=amazing"
cluster-init: true
```

This equals `k3s server --write-kubeconfig-mode "0644" --tls-san "foo.local" --node-label "foo=bar" --node-label "something=amazing" --cluster-init`.

Mapping rules: a CLI argument maps to the YAML key of the same name; repeatable arguments become YAML lists; booleans are true or false.

Precedence: values are loaded from both file and CLI, and CLI arguments win. For repeatable arguments such as --node-label, the CLI values overwrite all values in the list.

Combined example: a config.yaml with `token: "secret"` and `debug: true`, plus `K3S_KUBECONFIG_MODE="644" INSTALL_K3S_EXEC="server" sh -s - --flannel-backend none`, yields a server with kubeconfig mode 644, flannel backend none, the secret token and debug logging.

## Checked

2026-11-03: read docs.k3s.io installation/configuration. Confirmed: the default config path and config.yaml.d drop-ins, --config/K3S_CONFIG_FILE, the YAML-to-CLI mapping rules, CLI-over-file precedence and the combined example.

Method: documentation only; no commands were run.
