---
id: computing-software.software-engineering.cpp.cppcheck-clang-static-analyzer-and-msvc-analyze
name: cppcheck-clang-static-analyzer-and-msvc-analyze
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, cppcheck, clang-static-analyzer, scan-build, msvc-analyze, static-analysis, codechecker, sarif]
level: practitioner
status: docs-checked
description: "Run C/C++ static analyzers beyond clang-tidy: cppcheck, the Clang Static Analyzer (scan-build, CodeChecker), MSVC /analyze, and GCC -fanalyzer, with suppressions and CI."
sources: ["https://cppcheck.sourceforge.io/manual.html", "https://clang.llvm.org/docs/analyzer/user-docs/CommandLineUsage.html", "https://codechecker.readthedocs.io/", "https://learn.microsoft.com/en-us/cpp/build/reference/analyze-code-analysis", "https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cppcheck, Clang Static Analyzer and MSVC /analyze

**Goal:** catch null dereferences, leaks, uninitialised reads and API misuse at build time with
analyzers that complement clang-tidy's lint-style checks.

## Feed them the real build
All of these need the exact compile flags. Generate `compile_commands.json`
(`-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`) and point tools at it.

## cppcheck
```bash
cppcheck --project=build/compile_commands.json \
         --enable=warning,performance,portability,style \
         --inline-suppr --suppressions-list=cppcheck-suppress.txt \
         --cppcheck-build-dir=.cppcheck-cache \
         --xml 2> cppcheck.xml
```
- Check categories enabled by `--enable` include warning, performance, portability and style.
- Inline suppression: `// cppcheck-suppress nullPointer` on the line above.
- `--library=<lib>` loads a library `.cfg` shipped with cppcheck; `--check-level=exhaustive` for deeper runs.
- `--cppcheck-build-dir` lets unchanged files reuse results; `cppcheck-htmlreport` for HTML; `--template=gcc` for GCC-style output; a MISRA addon exists (rule texts are downloaded separately).

## Clang Static Analyzer (path-sensitive symbolic execution)
```bash
scan-build -o scan-results cmake --build build    # wraps the compiler
scan-view scan-results/<date>
# clang-tidy can run it too:
clang-tidy -checks='-*,clang-analyzer-*' -p build src/*.cpp
```
- Finds bugs along specific paths (leak only on an error branch, use-after-free, division by zero,
  null deref after a check), with a step-by-step HTML explanation.
- **CodeChecker** (Ericsson) runs the Clang Static Analyzer (`clangsa`) and clang-tidy over
  compile_commands.json, with cross-translation-unit analysis (`--ctu`), HTML export and a baseline export format:
```bash
CodeChecker log -b "cmake --build build" -o compile_commands.json
CodeChecker analyze compile_commands.json -o reports --analyzers clangsa clang-tidy
CodeChecker parse reports -e html -o reports_html
```

## MSVC /analyze
- Project setting "Enable Code Analysis on Build" or `cl /analyze`; rulesets select checks
  (`/analyze:ruleset <file>`). Extensions such as `CppCoreCheck.dll` provide the C++ Core Guidelines checks.
- Output SARIF with `/analyze:log:format:sarif`.

## GCC -fanalyzer
`gcc -fanalyzer` does interprocedural path analysis and warns about problems such as double-free, leaks and
file-descriptor misuse. The GCC manual says it is only suitable for C code in the release it documents, and that it is
much more expensive than other warnings; run it in a dedicated CI job on C sources.

## Adopting on an existing codebase
1. Run once, record a baseline (for cppcheck, an XML baseline with `--suppress-xml`; for CodeChecker, the baseline export format).
2. Fail CI only on **new** findings in changed files.
3. Burn down the baseline by category, starting with high-severity checkers.
4. Triage false positives with targeted suppressions and a comment explaining why.

## Verify
- [ ] Analyzer job runs in CI on every PR with compile_commands.json from the real build.
- [ ] New findings fail the build; baseline count trends down.
- [ ] SARIF results visible in the code-review UI.

## Checked

Date: 2026-10-25. Documentation: cppcheck manual (danmar/cppcheck man/manual.md), Clang Static Analyzer user docs (llvm/llvm-project, head 2026-10-25), CodeChecker user guide (Ericsson/codechecker docs), Microsoft C++ docs (MicrosoftDocs/cpp-docs), GCC manual invoke.texi.

Confirmed: cppcheck `--project=compile_commands.json`, `--enable` categories, `--inline-suppr`, `// cppcheck-suppress`, `--suppressions-list`, `--cppcheck-build-dir`, `--check-level=exhaustive`, `--library`, `--template=gcc`, `cppcheck-htmlreport`, XML baselines; scan-build with `-o`, `scan-view`, `clang-tidy -checks=-*,clang-analyzer-*`; CodeChecker `log`, `analyze --analyzers clangsa clang-tidy`, `--ctu`, `parse`, baseline export; MSVC `/analyze`, `/analyze:ruleset`, `/analyze:log:format:sarif`, CppCoreCheck.dll; GCC `-fanalyzer` limitations.
Removed as unconfirmed: `--error-exitcode` and `-j` flags, cppcheck as a CodeChecker analyzer (the current guide lists clangsa and clang-tidy), `--status-bugs`, the named MSVC ruleset file, SAL annotation names, and GCC 10 and C++ support versions (the manual says C only).

Method: documentation only; no commands were run.
