---
id: computing-software.systems-network-administration.nix.remote-builder-prerequisites
name: remote-builder-prerequisites
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, remote-builds, remote-builder, trusted-users, nix-store-info]
level: practitioner
status: docs-checked
description: "Prepare a machine as a Nix remote builder: SSH access, authorized key, trusted-users, passphrase-free daemon key and a nix store info connection test."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/advanced-topics/distributed-builds.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each remote machine needs:
- Nix installed.
- An SSH server (such as `sshd`) running and reachable.
- The local machine's public key in `/etc/ssh/authorized_keys.d/<username>`.
- The SSH user listed in `trusted-users` in `nix.conf`.

Test the connection:

```
nix store info --store ssh://username@mac
```

With a specific identity file:

```
nix store info --store ssh://username@mac?ssh-key=/path/to/my-key
```

Key notes:
- Builds are non-interactive, so use a key without a passphrase, or preload keys into `ssh-agent` or `gpg-agent`.
- In the default multi-user install the daemon runs builds and cannot prompt, so its key must have no passphrase.
- The daemon's user (usually root) needs SSH access. Check with `sudo su` then `ssh mac`. Root's keys are typically in `/root/.ssh/` on Linux or `/var/root/.ssh/` on macOS.

Troubleshooting: `bash: nix: command not found` then `error: cannot connect to 'mac'` means the `PATH` of non-interactive login shells lacks Nix; fix that `PATH`.

## Checked

2026-11-04: requirements list, nix store info test, ssh-key query parameter, passphrase and daemon-user notes and the PATH error confirmed against the Remote Builds manual page. Removed nothing.

Method: documentation only; no commands were run.
