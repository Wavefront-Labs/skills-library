---
id: computing-software.software-engineering.ocaml.migrating-from-ocaml-4-to-5
name: migrating-from-ocaml-4-to-5
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, ocaml5-migration, ocaml-versions, ocaml-5, migration, multicore, 4-14]
level: advanced
status: docs-checked
description: "Move code to OCaml 5: check library support, thread/domain changes, removed Stdlib modules, GC/stack differences and Obj usage."
sources: ["https://ocaml.org/releases", "https://ocaml.org/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating 4.14 to 5.x

## Checklist
1. Create a 5.x switch: `opam switch create <5.x version>` (see the opam usage guide) and reinstall dependencies.
2. Fix compile errors from removed or changed APIs (read the release notes for each version between yours and the target on ocaml.org/releases).
3. Audit global mutable state (reference cells, arrays, mutable record fields, `Hashtbl`): once you use domains, avoid data races. Immutable values can be shared freely between domains; mutable structures need a mutex or atomics.
4. Threads: systhreads created on a domain stay pinned to that domain, and only one systhread at a time runs OCaml code on a given domain.
5. Stack: the `l` (stack_limit, in words) OCAMLRUNPARAM option sets the stack limit for both bytecode and native code; check deep recursion on the new runtime.
6. Data-race-free programs have sequentially consistent semantics; check the memory model chapter before relying on racy code.

## Notes
- OCaml 5.0.0 introduced a new runtime with shared-memory parallelism (domains) and effect handlers.
- Each domain maps 1:1 to an OS thread and has its own runtime state, so domains are relatively expensive to create; do not spawn them casually.
- Benchmark before and after.
- Version specifics: read the release notes for each release for what you use.

## Self-check
- [ ] The test suite passes on both 4.14 and 5.x in CI.

## Checked

2026-11-02. Checked against ocaml.org/releases (5.0.0 introduced the new runtime with shared memory parallelism and effect handlers) and the OCaml 5.5 manual chapter on parallelism with domains (domains map 1:1 to OS threads with their own runtime state, immutable values shared freely, data-race-free programs are sequentially consistent, systhreads pinned to a domain with one running at a time) and the runtime chapter (l = stack_limit in words). Removed (not stated there): the pinned 5.2.0 version and --deps-only command, C stub and caml_modify advice, Random and Str as racy state, the master lock wording, Unix.fork failing after domains spawn, TSan version and package, stop-the-world minor GC, and the claim that sequential programs need no changes.

Method: documentation only; no commands were run.
