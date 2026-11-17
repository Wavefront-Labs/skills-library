---
id: computing-software.systems-network-administration.nix.derivation-output-checks
name: derivation-output-checks
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, allowed-references, disallowed-references, output-checks, structured-attrs]
level: advanced
status: docs-checked
description: "Constrain a derivation's runtime references and closure with allowedReferences, disallowedRequisites and outputChecks, and the __structuredAttrs interaction."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/language/advanced-attributes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Output checks fail a build whose output has unwanted references.

- `allowedReferences`: restricts an output's runtime references. An empty list forbids references to any inputs. Include `"out"` to allow a self-reference.
- `allowedRequisites`: restricts the full runtime closure to the listed items, which must also not add other dependencies.
- `disallowedReferences`: forbids direct runtime references to the listed items.
- `disallowedRequisites`: forbids runtime dependence on the listed items, including anything depending on them recursively.

With `__structuredAttrs = true`, the derivation's other attributes are serialised to a JSON file, and the four attributes above have no effect. Use `outputChecks` instead, defined per output, supporting those four plus `maxSize`, `maxClosureSize` and `ignoreSelfRefs`.

`unsafeDiscardReferences`: with structured attributes, a per-output boolean attribute set that enables unsafe discarding of references.

Related: `exportReferencesGraph` writes the references graph of each listed path to a named file in the build's temporary directory; `passAsFile` passes an attribute through a temporary file and gives the builder `<attr>Path`.

Gotcha: with `__structuredAttrs = true`, a top-level `allowedReferences` has no effect; move it into `outputChecks`.

## Checked

2026-11-04. Confirmed against the Nix manual Advanced Attributes page: the four reference and requisite checks, the `"out"` self-reference, the `__structuredAttrs` warning, `outputChecks` with `maxSize`, `maxClosureSize` and `ignoreSelfRefs`, `unsafeDiscardReferences`, `exportReferencesGraph` and `passAsFile`. Reworded the gotcha to the page's wording (no effect).

Method: documentation only; no commands were run.
