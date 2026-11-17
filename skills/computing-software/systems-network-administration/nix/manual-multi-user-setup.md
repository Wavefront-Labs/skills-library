---
id: computing-software.systems-network-administration.nix.manual-multi-user-setup
name: manual-multi-user-setup
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, build-users, nixbld, nix-remote, daemon-socket]
level: advanced
status: docs-checked
description: "Hand-build a multi-user Nix setup: create nixbld build users and group, run nix-daemon as root, point users at it with NIX_REMOTE, restrict the socket."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/multi-user.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Multi-user mode: the store and database are owned by a privileged user (usually root); builds run under separate build accounts; unprivileged users' store operations are forwarded to a daemon running as the store owner.

Build users (`nixbld1`, `nixbld2`, ...) must belong to the `nixbld` group, which has no other members, and to no other group. On Linux:

```
groupadd -r nixbld
for n in $(seq 1 10); do useradd -c "Nix build user $n" \
    -d /var/empty -g nixbld -G nixbld -M -N -r -s "$(which nologin)" \
    nixbld$n; done
```

Concurrent builds can never exceed the number of build users; create more if you expect many.

Run the daemon as root and add it to boot scripts:

```
nix-daemon
```

Unprivileged users set `NIX_REMOTE=daemon` in login scripts:

```
export NIX_REMOTE=daemon
```

Restrict access to a group by permissions on the socket directory:

```
chgrp nix-users /nix/var/nix/daemon-socket
chmod ug=rwx,o= /nix/var/nix/daemon-socket
```

Others cannot reach `/nix/var/nix/daemon-socket/socket`.

Note: only root and trusted users in `nix.conf` can specify arbitrary binary caches.

## Checked

2026-11-04. Confirmed against the Nix manual Multi-User Mode page: the privileged store owner and daemon forwarding, the `nixbld` group and build users with the Linux commands, the build-user concurrency limit, `nix-daemon` as root, `NIX_REMOTE=daemon`, the `daemon-socket` permission commands, and the binary cache limitation. Nothing removed.

Method: documentation only; no commands were run.
