---
id: computing-software.web-development.webassembly.proposal-process-and-status
name: proposal-process-and-status
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-phases, wasm-proposals, wasm-features, wasm]
level: practitioner
status: docs-checked
description: "How WebAssembly proposals move through phases 0-5, which features are in the 2.0 and 3.0 spec, and where to check engine support."
sources:
  - https://github.com/WebAssembly/meetings/blob/main/process/phases.md
  - https://github.com/WebAssembly/proposals/blob/main/README.md
  - https://github.com/WebAssembly/proposals/blob/main/finished-proposals.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The proposal process

Goal: track what is safe to use.

Phases (from the W3C process document):
- 0 Pre-Proposal: an idea; no CG vote needed; an issue on the design repository.
- 1 Feature Proposal (Community Group): general CG interest, a repository forked from the spec, an overview document.
- 2 Feature Description Available: precise overview document, test suite started.
- 3 Implementation Phase: engines and toolchains implement it; spec text and reference interpreter updated.
- 4 Standardize the Feature (Working Group): needs two or more Web VMs passing the test suite, at least one toolchain, and a fully updated spec and reference interpreter.
- 5 The Feature is Standardized: editors merge it into the main branch of the spec repo.
Advancing needs a CG vote, added to a meeting agenda through a pull request.

Finished proposals (phase 4, in the latest spec draft) by spec version:
- 1.0: MVP, import/export of mutable globals.
- 2.0: non-trapping float-to-int conversions, sign-extension operators, multi-value, JS BigInt to i64 integration, reference types, bulk memory operations, fixed-width SIMD.
- 3.0: tail call, extended constant expressions, typed function references, garbage collection, multiple memories, relaxed SIMD, custom annotation syntax, branch hinting, exception handling, JS string builtins, memory64.

Not yet merged at the time of reading: for example JS Promise Integration (phase 5), Threads (phase 4), Stack Switching (phase 3), Component Model (phase 1). Re-read the proposals list, it changes.

Check implementation status per engine in the feature status table at webassembly.org/features. Gate use on target engine support.

Verify: target browsers and runtimes are listed per feature used.

## Checked
Read the whole process document (WebAssembly/meetings process/phases.md), the active proposals README and finished-proposals.md (WebAssembly/proposals) on 2026-11-08. Confirmed the phases and entry requirements, the finished-proposals spec versions, and the pointer to webassembly.org/features. Removed: the claim that mutable globals are a 2.0 feature (the table puts it in 1.0), the "Phase 4 merges to the spec" wording (phase 5 merges), and the unchecked "confirm" caveat. The webassembly.org/features page itself is script-rendered and was not read, so no per-engine support claims are made.
Method: docs-only read of cited pages, 2026-11-08
