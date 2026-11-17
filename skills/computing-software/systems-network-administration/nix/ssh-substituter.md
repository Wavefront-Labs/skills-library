---
id: computing-software.systems-network-administration.nix.ssh-substituter
name: ssh-substituter
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, ssh-substituter, nix-copy-closure, ssh-agent]
level: practitioner
status: docs-checked
description: "Fetch store paths from another machine's Nix store over SSH with --substituters ssh://, copy a closure without installing, and avoid the passphrase trap."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/package-management/ssh-substituter.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install Firefox and pull any closure paths the remote server has:

```
nix-env --install --attr nixpkgs.firefox --substituters ssh://alice@avalon
```

(`alice@avalon` is the manual's example.) It works like the binary cache substituter but over SSH. For each needed path Nix checks the remote store first, then the binary cache, then builds from source.

Note: the SSH substituter cannot prompt for an SSH passphrase. Load the decrypted private key into `ssh-agent` with `ssh-add` first.

Copy a closure without adding it to your profile:

```
nix-store --realise /nix/store/m85bxg...-firefox-34.0.5 --substituters ssh://alice@avalon
```

This is essentially the same as:

```
nix-copy-closure --from alice@avalon /nix/store/m85bxg...-firefox-34.0.5
```

## Checked

2026-11-04: substituter lookup order, the ssh-agent note, the nix-store --realise example and the nix-copy-closure equivalence confirmed against the Serving a Nix store via SSH manual page. Removed the Verify line, which the page does not state.

Method: documentation only; no commands were run.
