---
id: computing-software.game-programming.unity.assembly-definitions-and-compile-times
name: assembly-definitions-and-compile-times
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-build, assembly-definition, asmdef, compile-times, asmref, version-defines, game-programming]
level: practitioner
status: docs-checked
description: "Split Unity scripts into assembly definitions to cut recompiles: asmdef and asmref, references, Auto Referenced, Editor and test assemblies, define constraints, version defines."
sources: ["https://docs.unity3d.com/Manual/ScriptCompilationAssemblyDefinitionFiles.html", "https://docs.unity3d.com/Manual/assembly-definition-files.html", "https://docs.unity.com/en-us/engine/6000.6/manual/programming-environment/script-compilation/assembly-definition-files/assembly-definitions-intro", "https://docs.unity.com/en-us/engine/6000.6/manual/programming-environment/script-compilation/assembly-definition-files/assembly-definitions-creating", "https://docs.unity.com/en-us/engine/6000.6/manual/programming-environment/script-compilation/assembly-definition-files/assembly-definitions-referencing", "https://docs.unity.com/en-us/engine/6000.6/manual/programming-environment/script-compilation/assembly-definition-files/includes", "https://docs.unity.com/en-us/engine/6000.6/manual/programming-environment/script-compilation/assembly-definition-files/class-assembly-definition-importer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assembly definitions and compile times

**Goal:** organize scripts into assemblies so a change recompiles less code and dependencies are
explicit.

## Why
By default Unity compiles almost all game scripts into the predefined `Assembly-CSharp.dll`, plus a
few smaller predefined assemblies. The manual lists the drawbacks as projects grow: every script
change recompiles all other scripts, any script can access any other script's types, and all scripts
are compiled for all platforms. Scripts in assemblies you define leave the default assemblies and can
only access scripts in your other custom assemblies. You cannot specify compilation order; Unity
orders by dependencies.

## Creating assemblies
- Assembly Definition (`.asmdef`): placed in the root of a script folder; menu Assets > Create >
  Scripting > Assembly Definition. It includes scripts in the folder and subfolders that do not have
  their own Assembly Definition or Reference.
- Assembly Definition Reference (`.asmref`): placed in a folder to add its scripts to an existing
  assembly; menu Assets > Create > Scripting > Assembly Definition Reference, then set its Assembly
  Definition property and click Apply.
- Select a script in the Project window to see its assembly in the Inspector's Assembly Information
  section.
- Platform-specific: in Platforms, check Any Platform and exclude platforms, or uncheck it and include
  platforms.
- Editor code anywhere: create a platform-specific assembly including only the Editor platform in a
  folder of Editor scripts, and use `.asmref` assets in other folders. Without this, scripts in folders
  named `Editor` normally go to `Assembly-CSharp-Editor`; an Assembly Definition in a folder with an
  `Editor` folder beneath it takes those scripts into its own assembly instead.
- Test assemblies: Unity identifies an assembly as a test assembly if it references
  `nunit.framework.dll` and has assembly definition references to `UnityEngine.TestRunner` and
  `UnityEditor.TestRunner`. Test assemblies are not compiled in the regular build pipeline; their code
  is in a Player build only when you run Play Mode tests in a Player.

## References
- An assembly using types from another must reference it. Add references in the Assembly Definition
  Inspector (Assembly Definition References, + button).
- By default predefined assemblies reference all other assemblies; custom assemblies automatically
  reference all precompiled assemblies.
- **Auto Referenced** off on an Assembly Definition: predefined assemblies do not recompile when it
  changes, and cannot use its code directly. It does not affect whether the assembly is in the build.
- Not allowed: references from custom assemblies to the predefined assemblies, explicit references
  from predefined assemblies, and cyclical references (refactor, or put mutually referencing classes in
  one assembly).
- **Use GUIDs** saves references as GUIDs so renaming an Assembly Definition asset does not break
  references; the manual calls it good practice. Referencing by name breaks on rename.
- **Override References** (General Options) lets you reference only the precompiled assemblies you
  list; otherwise Unity recompiles all your assemblies when any precompiled assembly updates.
- Other General Options: Allow 'unsafe' Code (passes `/unsafe`), No Engine References (no
  `UnityEditor`/`UnityEngine` references), Root Namespace.

## Conditional inclusion
- **Define Constraints**: all listed symbols must be defined for the assembly to compile; they work
  like `#if` at assembly level; prefix `!` to negate (`!ENABLE_IL2CPP`).
- **Version Defines**: rules with If resource (Unity or a package/module), version is, set define. The
  symbol is in scope only for scripts in that assembly, and can be used as a Define Constraint.
  Expressions use interval notation, no spaces, no wildcards: `[1.3,3.4.1]`, `(1.3.0,3.4)`, `[2.4.5]`
  (exact). Example: `[6000.0,6000.2)` covers 6000.0 and 6000.1 versions of Unity.

## Checked
Date: 2026-11-07

The two cited docs.unity3d.com pages are the same short overview (a table of links). I additionally
fetched and read, in full as text, the Introduction to assemblies, Creating assembly assets,
Referencing assemblies, Conditionally including assemblies and Assembly Definition Inspector reference
pages (Unity 6000.6 docs) and added them to `sources`. The Assembly Definition Reference Inspector
page was fetched but not read, and the file-format reference was not fetched.

Removed because none of those pages confirm it: the example layout (Game.Core etc.), advice on
ordering the dependency graph by edit frequency, `Editor Iteration Profiler` / Preferences >
Diagnostics measuring tips, the domain-reload comparison, third-party asset advice, the
`InternalsVisibleTo` gotcha, `com.unity.inputsystem [1.7,)` example, and the invented Verify list.

Method: documentation only; no commands were run.
