---
id: computing-software.systems-network-administration.nix.builders-configuration
name: builders-configuration
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, builders, cross-platform-build, machines-file]
level: practitioner
status: docs-checked
description: "Dispatch Nix builds to remote machines with the builders option, on the command line or in nix.conf or an /etc/nix/machines file, including a cross-platform test build."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/advanced-topics/distributed-builds.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Test a cross-platform build from the command line (an `aarch64-darwin` derivation built from Linux):

```
nix build --impure \
 --expr '(with import <nixpkgs> { system = "aarch64-darwin"; }; runCommand "foo" {} "uname > $out")' \
 --builders 'ssh://mac aarch64-darwin'
```

Progress looks like `[1/0/1 built, 0.0 MiB DL] building foo on ssh://mac`. Check `cat ./result`; it should print `Darwin`.

Several builders are separated by a semicolon or newline:

```
--builders 'ssh://mac aarch64-darwin ; ssh://beastie x86_64-freebsd'
```

Persist in `nix.conf`:

```
builders = ssh://mac aarch64-darwin ; ssh://beastie x86_64-freebsd
```

Restart the Nix daemon after changing `nix.conf`.

Or keep the list in its own file, referenced with `@`:

```
builders = @/etc/nix/machines
```

That is the default, so `/etc/nix/machines` is included automatically.

Prerequisites for the remote side are in the remote-builder-prerequisites skill.

## Checked

2026-11-04. Confirmed against the Nix manual Remote Builds page: the `nix build --impure --expr ... --builders` example and its output, semicolon or newline separation, the `nix.conf` form, daemon restart, and `builders = @/etc/nix/machines` being the default. Nothing removed.

Method: documentation only; no commands were run.
