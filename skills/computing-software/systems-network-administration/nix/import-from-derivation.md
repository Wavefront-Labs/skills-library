---
id: computing-software.systems-network-administration.nix.import-from-derivation
name: import-from-derivation
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, import-from-derivation, ifd, allow-import-from-derivation, read-write-mode]
level: advanced
status: docs-checked
description: "Recognise Import From Derivation, its list of triggering builtins, why it slows evaluation, and how to forbid it with allow-import-from-derivation."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/language/import-from-derivation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
IFD: passing an expression that evaluates to a store path to a builtin that reads from the filesystem. Evaluation pauses, the store object is realised, then evaluation resumes.

Triggering builtins: `import expr`, `builtins.readFile`, `readFileType`, `readDir`, `pathExists`, `filterSource f expr`, `builtins.path { path = expr; }`, `hashFile t expr`, `scopedImport x drv`.

Cost: the evaluator is sequential, so it discovers store paths to read one at a time; realisation is parallel but cannot be batched across all required paths. IFD is much slower than otherwise.

Forbid it:

```
allow-import-from-derivation = false
```

Evaluation then completes before any realisation starts, so Nix can produce a build plan first.

Example:

```
let
  drv = derivation {
    name = "hello";
    builder = "/bin/sh";
    args = [ "-c" "echo -n hello > $out" ];
    system = builtins.currentSystem;
  };
in "${builtins.readFile drv} world"
```

```
nix-instantiate IFD.nix --eval --read-write-mode
```

prints `building '...-hello.drv'...` then `"hello world"`.

## Checked

2026-11-04. Confirmed against the Nix manual Import From Derivation page: the list of builtins, the pause, realise and resume behaviour, the sequential evaluator performance note, `allow-import-from-derivation` set to `false`, the build plan statement, and the `IFD.nix` example with its output. Removed an unsourced verify line.

Method: documentation only; no commands were run.
