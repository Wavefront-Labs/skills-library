---
id: computing-software.systems-network-administration.nix.nix-shell-shebang-scripts
name: nix-shell-shebang-scripts
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, shebang, nix-shell-interpreter, self-contained-script]
level: practitioner
status: docs-checked
description: "Write self-contained scripts whose dependencies come from Nix using a #! /usr/bin/env nix-shell line with -i and -p, pinned nixpkgs or a deps.nix file."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-shell.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A script declares its dependencies with `#! nix-shell` lines after the standard shebang.

```
#! /usr/bin/env nix-shell
#! nix-shell -i python3 --packages python3
print("hello")
```

(Interpreter and package names are illustrative.)

Rules:
- The first line is `#! /usr/bin/env nix-shell`.
- Following lines hold `nix-shell` options such as `-i <interpreter>` and `--packages <packages>`.
- Only the first line must be at the top of the file; the `#! nix-shell` lines can come later, so they can sit inside block comments in languages such as ECMAScript, Erlang or PHP.
- `-i` names the real interpreter, for example `python3`, `perl`, `bash` or `runghc`.
- Simple Nix expressions can be package arguments, such as `terraform.withPlugins (...)`; quote them with single or double quotes.
- Multiple `#! nix-shell` lines are merged, so one can pin Nixpkgs with `-I nixpkgs=...`.
- Dependencies can come from a file: `#! nix-shell deps.nix -i python`, where `deps.nix` defines the environment, for example with `runCommand`.

## Checked

2026-11-04: shebang form, merged nix-shell lines, line placement, quoting of expressions, -I pinning and the deps.nix variant confirmed against the Use as a #!-interpreter section of the nix-shell manual page. Removed the Verify line (chmod and run), which the page does not state.

Method: documentation only; no commands were run.
