---
id: computing-software.software-engineering.fsharp.release-optimisation-flags
name: release-optimisation-flags
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, release-optimisation-flags, fsharp-compiler, optimize-flag, deterministic-build]
level: advanced
status: docs-checked
description: "What the F# compiler flags --optimize, --tailcalls, --crossoptimize, --checked, --deterministic and --pathmap do, per the F# compiler options reference."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/compiler-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimisation and determinism
**Goal:** know what the compiler flags do when you build for release.

Flags documented on the F# compiler options page (each takes `+` or `-` unless noted):
- `--optimize[+|-] [list]` (`-O`): enables or disables optimisations. Selective sub-options: `nojitoptimize`, `nojittracking`, `nolocaloptimize`, `nocrossoptimize`, `notailcalls`.
- `--tailcalls[+|-]`: enables or disables the `tail` IL instruction, which reuses the stack frame for tail-recursive functions. **Enabled by default.**
- `--crossoptimize[+|-]`: cross-module optimisations.
- `--checked[+|-]`: generates overflow checks; equivalent to the C# option of the same name.
- `--deterministic[+|-]`: produces a deterministic assembly (including module version GUID and timestamp). It cannot be used with wildcard version numbers and supports only embedded and portable debugging types.
- `--pathmap:path=sourcePath,...`: maps physical paths to the source path names the compiler outputs (same as the C# `/pathmap`); useful so builds on different machines embed the same paths.
- `--debug[+|-]` / `--debug:[full|pdbonly]`: debug information; the default is `full`. `--pdb:file` names the PDB and only applies when `--debug` is on.

Pass them through your build system's compiler-flag mechanism; the cited page does not document MSBuild property names, so check your SDK documentation for how `Optimize`, `Tailcalls`, `DeterministicSourcePaths` and similar map onto these flags.

## Gotchas
- With tailcalls on, tail-recursive calls reuse the stack frame, so a call that is a tail call leaves no frame behind: expect different stack traces from a build with `--tailcalls-`.
- `--deterministic` is about the compiler output only; also keep inputs (sources, package versions, `--pathmap`) identical.

## Self-check
Build twice from clean with the same flags and compare file hashes.

## Checked
Confirmed on the F# compiler options page: flag names, `+/-` forms, optimisation sub-options, tailcalls default, deterministic restrictions, pathmap, debug default.
Removed: the MSBuild property block, claims that optimize is on by default in Release, `ContinuousIntegrationBuild`, and `dotnet fsc --help`, none stated on the cited page.
Method: docs-only read of cited pages, 2026-11-08
