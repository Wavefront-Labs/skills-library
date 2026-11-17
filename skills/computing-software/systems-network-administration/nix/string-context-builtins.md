---
id: computing-software.systems-network-administration.nix.string-context-builtins
name: string-context-builtins
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, string-context, get-context, discard-string-context, append-context]
level: sme
status: docs-checked
description: "Inspect and manipulate Nix string context with hasContext, getContext, unsafeDiscardStringContext and appendContext, and know the context element types."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/language/string-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Nix string is a character sequence plus a string context: an unordered set of elements tracking non-string dependencies such as store paths and derivations. Concatenation and interpolation carry context, and Nix uses it to ensure each referenced store path is valid. You rarely handle it directly.

Element types:
- Deriving path, constant: from `builtins.storePath`; shows `path = true`.
- Deriving path, output: from `builtins.outputOf` (experimental); shows `outputs = [ "out" ];`.
- Derivation deep: used with `exportReferencesGraph`; `builtins.addDrvOutputDependencies` converts a constant element into one, giving `allOutputs = true;`.

Builtins:
- `builtins.hasContext s`: non-empty context?
- `builtins.getContext s`: context as an attribute set.
- `builtins.unsafeDiscardStringContext s`: copy with empty context, needed for operators requiring an empty context. "Unsafe" because dependency tracking is lost.
- `builtins.appendContext s ctx`: copy with extra elements in the `getContext` format.

To build an arbitrary context: make a string carrying the desired elements, extract it with `getContext`, then apply to a base string with `appendContext`.

Example:

```
builtins.getContext (builtins.storePath "/nix/store/<hash>-hello-2.10")
```

The page notes that the string returned by `unsafeDiscardStringContext` has lost the dependency tracking Nix normally guarantees.

## Checked

2026-11-04: string context definition, the three element types with their getContext shapes, the four builtins and the arbitrary-context recipe confirmed against the String context manual page. Replaced an unconfirmed claim about unrealised or collectable paths with what the page says.

Method: documentation only; no commands were run.
