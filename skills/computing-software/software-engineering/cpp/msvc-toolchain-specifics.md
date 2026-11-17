---
id: computing-software.software-engineering.cpp.msvc-toolchain-specifics
name: msvc-toolchain-specifics
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, msvc, visual-studio, permissive-minus, runtime-library, vcvars, windows, cl-exe, dllexport]
level: practitioner
status: docs-checked
description: "Build C++ correctly with MSVC: vcvars developer environments, /permissive- and /Zc conformance flags, runtime library (/MD vs /MT) mismatches, warnings, PDBs and DLL exports."
sources: ["https://learn.microsoft.com/en-us/cpp/build/reference/compiler-options-listed-by-category", "https://learn.microsoft.com/en-us/cpp/build/reference/permissive-standards-conformance", "https://learn.microsoft.com/en-us/cpp/build/reference/md-mt-ld-use-run-time-library", "https://learn.microsoft.com/en-us/cpp/build/building-on-the-command-line", "https://cmake.org/cmake/help/latest/prop_tgt/MSVC_RUNTIME_LIBRARY.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MSVC toolchain specifics

**Goal:** portable C++ that builds cleanly with MSVC, without the classic Windows-only failures:
missing environment, conformance differences, runtime mismatches and DLL symbol problems.

## Developer environment
`cl.exe` needs `INCLUDE`, `LIB` and `PATH` set by `vcvarsall.bat`:
```bat
"%ProgramFiles%\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
```
- `vcvarsall.bat` takes host and target architecture parameters; Microsoft warns that the command files vary
  from machine to machine, so do not copy them between computers.
- With CMake's Visual Studio generators the environment is not needed; with Ninja run from a developer
  command prompt so `cl.exe` is found.

## Conformance flags (set them all)
```
/permissive-     standards mode: two-phase lookup, no non-const ref binding to temporaries, etc.
/Zc:__cplusplus  report the real standard in __cplusplus (otherwise always 199711L)
/Zc:preprocessor enable the conforming preprocessor
/std:c++20       or /std:c++latest
/utf-8           source and execution charset UTF-8
/EHsc            standard C++ exception handling
```
`/permissive-` is set by default in new projects from Visual Studio 2017 15.5, and implied by
`/std:c++latest` (VS 2019 16.8+) and `/std:c++20` (16.11+); set it explicitly in other build systems.

## Warnings
`/W4`, `/WX` warnings as errors, `/external:anglebrackets /external:W0` to silence third-party
headers, `/w1NNNN` (for example `/w14265`) to raise a specific warning to level 1-4.

## Runtime library: /MD vs /MT
| Flag | Runtime |
|---|---|
| `/MD` / `/MDd` | DLL CRT (release / debug) |
| `/MT` / `/MTd` | static CRT (release / debug) |
Every object and static library in one link **must use the same** runtime and debug/release flavour,
otherwise the linker reports runtime-library or `_ITERATOR_DEBUG_LEVEL` mismatches.
Memory allocated in a module with one CRT must not be freed by another.
CMake (3.15+, takes effect when policy CMP0091 is NEW):
```cmake
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
```

## Debug info and PDBs
`/Zi` writes a separate PDB, `/Z7` embeds debug information in the object files (see the /Z7, /Zi, /ZI
reference). `/FS` forces synchronous PDB writes when several cl processes share one PDB. Keep release PDBs for crash dumps.

## DLL exports
Symbols are hidden by default on Windows. Use an export macro:
```cpp
#if defined(MYLIB_BUILD)
#  define MYLIB_API __declspec(dllexport)
#else
#  define MYLIB_API __declspec(dllimport)
#endif
class MYLIB_API Widget { ... };
```
CMake's `GenerateExportHeader` creates it; `WINDOWS_EXPORT_ALL_SYMBOLS` is a blunt shortcut.
Do not pass STL types across DLL boundaries built with different toolsets/flags.

## Other gotchas
- `/O2` for speed; `/GL` + `/LTCG` for whole-program optimisation; `/Ob3` (VS 2019 and later) for more inlining.
- `/sdl` adds security checks; `/guard:cf` Control Flow Guard; `/Qspectre` mitigations.
- clang-cl (`-T ClangCL` with the Visual Studio generators) can serve as a second compiler;
  MSVC supports `/fsanitize=address`.

## Verify
- [ ] CI builds with `/permissive- /Zc:__cplusplus /W4 /WX` on MSVC.
- [ ] No LNK2038 runtime mismatch; all deps built with the same CRT.
- [ ] Release PDBs archived.

## Checked

Date: 2026-10-25. Documentation: Microsoft C++ docs (MicrosoftDocs/cpp-docs build/reference pages for /Zc:__cplusplus, /permissive-, /std, /MD, /Z7, /FS, /WX and /external, building-on-the-command-line, exporting-from-a-dll; head fetched 2026-10-25) and CMake (Kitware/CMake, head 2026-10-25).

Confirmed: `vcvarsall.bat` architecture parameters and its path under `VC\Auxiliary\Build`; `__cplusplus` stays 199711L without `/Zc:__cplusplus`; `/permissive-` defaults and implication by `/std:c++latest` and `/std:c++20`; `/MD`, `/MT` and their debug forms; `CMAKE_MSVC_RUNTIME_LIBRARY` (3.15, needs CMP0091 NEW) and the generator-expression form; `/Z7`, `/Zi`, `/FS`; `/O2`, `/GL`, `/LTCG`, `/Ob3` (VS 2019+), `/sdl`, `/guard:cf`, `/Qspectre`; `/fsanitize=address`; `/external:W0`; GenerateExportHeader and WINDOWS_EXPORT_ALL_SYMBOLS.
Removed as unconfirmed: vswhere, Enter-VsDevShell and GitHub Action names, toolset version mapping, the LNK2038 message, vcpkg triplet-to-runtime mapping, `/DEBUG:FULL`, NOMINMAX note, runtime DLL names and the "CMake does not add /permissive-" claim.

Method: documentation only; no commands were run.
