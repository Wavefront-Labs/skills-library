---
id: computing-software.systems-network-administration.nix.nix-channel-management
name: nix-channel-management
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-channel, channels, channel-rollback, tarball-ttl]
level: practitioner
status: docs-checked
description: "Subscribe to, update, list, roll back and remove Nix channels with nix-channel, including the nixexprs.tar.gz requirement and the reproducibility caveat."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-channel.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Channels reference remote Nix expressions and fetch their latest versions. Official channels are listed at channels.nixos.org.

```
nix-channel --add https://channels.nixos.org/nixpkgs-unstable
nix-channel --list
nix-channel --update
nix-channel --rollback
nix-channel --remove nixpkgs
```

Operations:
- `--add url [name]`: name defaults to the URL's last component with `-stable` or `-unstable` removed. It does not update. The URL must point to a directory containing `nixexprs.tar.gz` whose top level has one directory with a `default.nix`.
- `--update [names]`: downloads and creates a new generation; all channels if no names. Downloads are cached; `--tarball-ttl` or the `tarball-ttl` option sets how long.
- `--list-generations`: generations of the channel profile.
- `--rollback [generation]`: back to before the last update, or a given generation.

Caveat: channel state lives outside the expressions that use it, limiting reproducibility. For explicit dependencies use `fetchurl`, `fetchTarball` or `fetchGit`, or `-I` on the command line.

The page's rollback example runs `nix-instantiate --eval '<nixpkgs>' --attr lib.version` before and after `--rollback` to show the version change.

## Checked

2026-11-04: operations, name default, nixexprs.tar.gz requirement, tarball-ttl note, reproducibility note and examples confirmed against the nix-channel manual page. Removed nothing.

Method: documentation only; no commands were run.
