---
id: computing-software.systems-network-administration.nix.nix-copy-closure-ssh
name: nix-copy-closure-ssh
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-copy-closure, closure-copy, nix-sshopts]
level: practitioner
status: docs-checked
description: "Copy a store path and its dependency closure to or from a remote machine over SSH with nix-copy-closure, using --use-substitutes and NIX_SSHOPTS."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-copy-closure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Synopsis: `nix-copy-closure [--to | --from] [--gzip] [--include-outputs] [--use-substitutes | -s] [-v] [user@]machine[:port] paths`

It computes the closure of the paths and skips anything the other machine already has.

```
nix-copy-closure --to alice@avalon $(nix-build '<nixpkgs>' --attr hello)
nix-copy-closure --from alice@avalon /nix/store/<hash>-hello
```

(`alice@avalon` is illustrative.)

Options:
- `--to` (default): local store to remote.
- `--from`: remote store to local.
- `--gzip`: compress the SSH connection.
- `--include-outputs`: also copy outputs of store derivations in the closure.
- `--use-substitutes` / `-s`: target tries its substituters first; the rest is copied from the source. Useful when the link between machines is slow but the target reaches a cache such as cache.nixos.org quickly.

`NIX_SSHOPTS` passes extra options to `ssh`.

Notes:
- The local store can be set with `--store`; the remote store is configured only on the remote machine.
- You may be prompted twice (one connection to check missing paths, another to send them). Use public-key auth with `ssh-agent`.

## Checked

2026-11-04: synopsis, options, NIX_SSHOPTS, the --store note and the double-connection note confirmed against the nix-copy-closure manual page. Removed nothing.

Method: documentation only; no commands were run.
