---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-token-bootstrap-commands
name: k3s-token-bootstrap-commands
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, token-create, token-rotate, bootstrap-token]
level: practitioner
status: docs-checked
description: "Create, list, delete and rotate K3s tokens with the k3s token subcommands."
sources:
  - https://docs.k3s.io/cli/token
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Subcommands: create, delete, generate, list, rotate.

`k3s token create [token]` makes a bootstrap token; with no argument one is generated. A secure-format token including the cluster CA hash is printed once; save it because the secret part cannot be shown again. Flags:

- --description: human-friendly note
- --groups: extra groups (default system:bootstrappers:k3s:default-node-token)
- --ttl: lifetime such as 1s, 2m, 3h; 0 never expires (default 24h0m0s)
- --usages: default signing,authentication
- --data-dir (default /var/lib/rancher/k3s, or ${HOME}/.rancher/k3s if not root) and --kubeconfig

`k3s token generate` prints a random bootstrap token without creating it. You can make your own in the form `[a-z0-9]{6}.[a-z0-9]{16}` (token ID, then secret).

`k3s token list` shows ID, description and remaining TTL; `--output` is text (default) or json.

`k3s token delete` takes the full token or just the ID.

`k3s token rotate` replaces the original server token. Flags: --server (default https://127.0.0.1:6443, $K3S_URL), --token (existing, $K3S_TOKEN), --new-token. With no new token one is generated. After rotation, all servers and all agents that joined with the old token must be restarted with the new one.

Warning: snapshots taken before the rotation need the old server token to restore.

The bootstrap token lifecycle uses the same code as `kubeadm token`.

## Checked

2026-11-03: read docs.k3s.io cli/token. Confirmed: the create, delete, generate, list and rotate subcommands, the --ttl (default 24h0m0s), --usages (signing,authentication), --groups and --data-dir defaults, the [a-z0-9]{6}.[a-z0-9]{16} format, and the rotate flags.

Method: documentation only; no commands were run.
