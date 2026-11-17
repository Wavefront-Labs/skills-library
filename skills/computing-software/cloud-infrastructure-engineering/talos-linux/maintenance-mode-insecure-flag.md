---
id: computing-software.cloud-infrastructure-engineering.talos-linux.maintenance-mode-insecure-flag
name: maintenance-mode-insecure-flag
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [maintenance-mode, insecure, mtls, cert-fingerprint, apply-config, sidero-link, talosctl]
level: practitioner
status: docs-checked
description: "Using talosctl --insecure in maintenance mode: why the API is unauthenticated, verifying the node by console cert fingerprint, and which commands and resources work insecurely."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/system-configuration/insecure.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos normally uses mutual TLS. A node in maintenance mode (no machine config yet) serves the API with a self-signed certificate and the client presents none, so `--insecure` tells `talosctl` to skip server verification. Once a config is applied, stop using `--insecure`; later commands authenticate with the certificates in your talosconfig. (`talosctl image cache-create --insecure` is unrelated: it allows insecure registries.)

**Verify identity.** The node prints its temporary certificate fingerprint on the console at boot (physical, VM, serial or IPMI). Pass it:

```bash
talosctl apply-config
--insecure
--cert-fingerprint <fingerprint>
--nodes <node_ip>
--file machine.yaml
```

(The docs show the flags on separate lines; add line continuations when running it.)

**Commands that accept `--insecure`:** `apply-config`, `version`, `get`, `meta`, `reset`, `wipe disk`. For `get`, list the resources available insecurely (non-sensitive ones):

```bash
talosctl get rd --insecure --nodes $NODE_IP -o json \
| jq -r 'select(.spec.sensitivity == null) | .spec.aliases[0]'
```

Use `!= null` to list the ones that are not available.

```bash
talosctl apply-config --insecure --nodes 192.168.1.100 --file controlplane.yaml
talosctl get disks --nodes 192.168.1.100 --talosconfig=./talosconfig
```

In Omni-managed clusters, unjoined nodes listen only over the SideroLink tunnel, so no one else on the network can push a config to them.

## Checked

2026-11-04. Insecure flag page confirms the TLS behaviour, fingerprint procedure, supported command list and jq queries.

Method: documentation only; no commands were run.
