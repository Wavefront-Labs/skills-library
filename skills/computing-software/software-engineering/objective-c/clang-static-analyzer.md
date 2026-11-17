---
id: computing-software.software-engineering.objective-c.clang-static-analyzer
name: clang-static-analyzer
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-static-analysis, clang-static-analyzer]
level: practitioner
status: docs-checked
description: "Run the analyzer via Xcode Analyze, clang --analyze or scan-build, and read the common Cocoa memory, nullability and API-misuse reports."
sources:
  - https://clang.llvm.org/docs/analyzer/user-docs/CommandLineUsage.html
  - https://clang.llvm.org/docs/analyzer/user-docs/Annotations.html
  - https://clang.llvm.org/docs/analyzer/checkers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clang Static Analyzer
**Goal:** find leaks, nil dereferences and API misuse without running code.

```bash
clang --analyze --analyzer-output text -fobjc-arc Foo.m
scan-build -o build/analysis xcodebuild -configuration Debug
scan-build -k -V make
```
- `clang --analyze` analyzes one translation unit. `--analyzer-output` selects the format: html, plist, plist-multi-file, plist-html, sarif, sarif-html or text (default plist); sarif writes to the path given by `-o`.
- `scan-build <build command>` runs your normal build with a fake compiler (by overriding CC and CXX) and writes HTML reports plus `index.html`. `-o` sets the report directory (default a directory in /tmp), `-V` opens the results, `-k` keeps going after errors (supports make and xcodebuild), `-v` is verbose. It does not support cross-translation-unit analysis; CodeChecker (out of tree) does, on Linux.
- Xcode's Analyze menu command (Build and Analyze) is the easiest route for iOS projects. With scan-build and xcodebuild, analyze the Debug configuration against the simulator SDK with code signing off.
- Cocoa-aware checkers include `osx.cocoa.RetainCount` (leaks and improper reference counting), `osx.cocoa.NilArg` (prohibited nil arguments), `osx.cocoa.SelfInit` (self initialised in initializers), `osx.cocoa.Loops`, `osx.cocoa.IncompatibleMethodTypes`, `osx.cocoa.ClassRelease` (retain, release or autorelease sent to a Class), `osx.coreFoundation.CFRetainRelease` (null passed to CFRetain/CFRelease), and the `nullability.*` family (for example `nullability.NullPassedToNonnull`). `optin.osx.cocoa.localizability.NonLocalizedStringChecker` is an opt-in checker.
- Teach it ownership with annotations: `NS_RETURNS_RETAINED` (`ns_returns_retained`), `CF_RETURNS_RETAINED` (`cf_returns_retained`), `CF_RETURNS_NOT_RETAINED`, and `NS_CONSUMED`/`NS_RELEASES_ARGUMENT` (`ns_consumed`: the callee releases the parameter).
- Build in a Debug configuration: assertions let the analyzer prune infeasible paths and cut false positives (`--force-analyze-debug-code` on scan-build enables them). Custom assertion handlers must be annotated or the analyzer assumes they return.
- If the project uses an autoconf `configure` script, run `scan-build ./configure` first so generated makefiles use the analyzer's compiler.

## Self-check
Write a CF leak (CFStringCreate without release) and confirm the report.

## Checked

2026-11-08. Confirmed against the Clang analyzer Command Line Usage (scan-build and CodeChecker), Annotations and Available Checkers pages. Removed `RUN_CLANG_STATIC_ANALYZER`, `xcodebuild analyze`, `-analyzer-checker-help`, the `__clang_analyzer__` suppression idiom, the CI-failure advice and the ARC-leak remark, which none of those pages state.
Method: documentation only; no commands were run.
