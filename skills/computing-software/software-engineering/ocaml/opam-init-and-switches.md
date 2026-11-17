---
id: computing-software.software-engineering.ocaml.opam-init-and-switches
name: opam-init-and-switches
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, opam-switches, ocaml-opam, opam-switch, opam-init, opam-env, local-switch]
level: practitioner
status: docs-checked
description: "Install opam, create global and local switches, choose compiler versions, and load the environment with opam env."
sources: ["https://opam.ocaml.org/doc/Usage.html", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# opam switches

```bash
opam init                                  # first time; --disable-sandboxing for a default config without sandboxing
opam switch create <name> <version>        # a switch for a compiler version (name optional)
eval $(opam env)                           # update the shell environment; opam env --switch=SWITCH --set-switch
opam update && opam upgrade                # refresh the package database, then upgrade installed packages
```

## Notes
- Use `opam switch create [name] <package-or-version>` to switch to a different compiler, then run the advertised `eval $(opam env)` to update PATH.
- `opam init` can add a line to your shell init files (`--shell-setup`, `--no-setup` to skip) and can register a shell hook (`--enable-shell-hook`) that keeps the environment current at every prompt.
- `opam upgrade` should be run after `opam update`; use `opam pin` to keep specific packages from being upgraded.

## Self-check
- [ ] `which ocaml` points inside the intended switch.

## Checked

2026-11-02. Checked against opam.ocaml.org/doc/Usage.html (update, upgrade, switch create [name] <package-or-version>, eval $(opam env), pin) and the opam init man page (--disable-sandboxing, --shell-setup, --no-setup, --enable-shell-hook, shell hook behaviour, opam env --switch with --set-switch). Replaced the source link /doc/ (a stub page) with the Usage page. Removed (not on those pages): local project switches and the _opam directory, switch list and remove, the install line of tools, --yes, opam clean, the log directory and the Windows note.

Method: documentation only; no commands were run.
