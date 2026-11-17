---
id: computing-software.systems-network-administration.nix.ssh-forced-command-store
name: ssh-forced-command-store
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, forced-command, sshd-config, nix-store-serve]
level: advanced
status: docs-checked
description: "Create a restricted nix-ssh account whose sshd ForceCommand is nix-store --serve, giving read-only access to the local Nix store and nothing else."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/package-management/ssh-substituter.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To give clients read-only access to the local store over SSH and nothing else, restrict a dedicated user in `sshd_config`:

```
Match User nix-ssh
  AllowAgentForwarding no
  AllowTcpForwarding no
  PermitTTY no
  PermitTunnel no
  X11Forwarding no
  ForceCommand nix-store --serve
Match All
```

On NixOS use `configuration.nix` instead:

```nix
nix.sshServe.enable = true;
nix.sshServe.keys = [ "ssh-dss AAAAB3NzaC1k... bob@example.org" ];
```

`keys` takes the public keys of users allowed to connect.

This account is meant for SSH substituter access (an `ssh://` substituter URL, as in the ssh-substituter skill).

## Checked

2026-11-04: the sshd_config block, forced command, NixOS sshServe options and the keys description confirmed against the Serving a Nix store via SSH manual page. Removed the Match All explanation, the client URL form and the Verify line, which the page does not state.

Method: documentation only; no commands were run.
