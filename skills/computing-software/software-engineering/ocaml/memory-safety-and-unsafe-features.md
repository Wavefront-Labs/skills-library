---
id: computing-software.software-engineering.ocaml.memory-safety-and-unsafe-features
name: memory-safety-and-unsafe-features
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, memory-safety-unsafe, ocaml-security, obj-magic, unsafe-get, memory-safety, audit]
level: advanced
status: docs-checked
description: "Know where OCaml loses memory safety (Obj.magic, -unsafe, C stubs, Marshal) and how to audit for them."
sources: ["https://ocaml.org/manual/api/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory safety in OCaml

## Safe by default
Bounds checks, no pointer arithmetic, GC-managed memory, abstract types enforced by the module system.

## Escape hatches to audit
```bash
grep -rn "Obj\.\|unsafe_\|Marshal\.from\|external " src/
```
- `Obj.magic`, `Obj.repr`, `Obj.field`: type confusion, crashes, possible exploits.
- Compiler flag `-unsafe`, which turns off bounds checks on array and string accesses (and the zero-divisor check).
- `Marshal.from_*` on untrusted data.
- C stubs and ctypes: ordinary C vulnerabilities (overflows, use-after-free).
- Integer operations are taken modulo 2^Sys.int_size and do not fail on overflow; check sizes before allocating (`Bytes.create n` raises `Invalid_argument` for n above `Sys.max_string_length`).

## Mitigations
- Forbid `Obj` in review (a grep CI check) and keep `-unsafe` off.

## Self-check
- [ ] The grep above returns only justified, reviewed hits.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the ocamlopt page (-unsafe removes bounds and zero-divisor checks), the Stdlib page (integers wrap modulo 2^Sys.int_size), the Obj page (repr, magic, field), the Marshal page (not type-safe) and the String/Bytes pages (Invalid_argument above Sys.max_string_length).

Removed or corrected: unsafe_get/unsafe_set function names (not in the fetched API pages), the OCaml 5 data-race remark, and the fuzzing and parser-library recommendations.

Method: documentation only; no commands were run.
