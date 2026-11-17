---
id: computing-software.systems-network-administration.nix.nix-env-query-packages
name: nix-env-query-packages
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-env-query, available-packages, compare-versions, status-flags]
level: intro
status: docs-checked
description: "List installed or available packages with nix-env --query, find attribute paths, show status, compare installed against available and emit JSON."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-env/query.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nix-env --query` shows installed store paths in the current profile generation (default) or, with `--available` (`-a`), derivations in the active Nix expression. Results are sorted by `name`; name patterns filter them.

```
nix-env --query
nix-env --query --available --attr-path
nix-env --query --available --status
nix-env --query --available --compare-versions
nix-env --query --available --json '.*zip.*'
```

Output options:
- `--xml`, `--json`: machine-readable.
- `--prebuilt-only` (`-b`): only packages with a substitute.
- `--status` (`-s`): three characters: installed, present on the system, substitute exists; a dash means no.
- `--attr-path` (`-P`): attribute path usable with `--attr`; only with `--available`.
- `--compare-versions` (`-c`): `<` newer available, `=` same or older available, `>` only older exist, `- ?` none available.
- `--no-name`, `--system`, `--drv-path`, `--out-path`, `--description` (one line of `meta.description`).
- `--meta`: all meta-attributes, only with `--xml` or `--json`.

Use `--file` to query a specific Nix expression, for example a Nixpkgs archive URL.

## Checked

2026-11-04: source selection, output flags, status characters, compare-versions symbols and the --file example confirmed against the nix-env --query manual page. Removed the Verify line, which the page does not state.

Method: documentation only; no commands were run.
