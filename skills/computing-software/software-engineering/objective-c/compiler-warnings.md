---
id: computing-software.software-engineering.objective-c.compiler-warnings
name: compiler-warnings
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-build, compiler-warnings]
level: practitioner
status: docs-checked
description: "Enable a strong clang warning set (-Wall, -Wextra, -Wshadow, -Wformat-security, -Wunguarded-availability) and treat selected ones as errors."
sources:
  - https://clang.llvm.org/docs/DiagnosticsReference.html
  - https://clang.llvm.org/docs/UsersManual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compiler warning flags
**Goal:** catch bugs at compile time.

```
-Wall -Wextra
-Wshadow -Wconversion -Wformat -Wformat-security
-Wundeclared-selector -Wselector -Wstrict-selector-match
-Warc-repeated-use-of-weak -Warc-retain-cycles -Wimplicit-retain-self
-Wunguarded-availability-new -Wobjc-designated-initializers
-Wnullability-completeness -Wdeprecated-implementations
-Werror=return-type -Werror=objc-method-access
```
- `-Wcompletion-handler` reports a completion handler that is called twice or never called on some paths.
- `-Wimplicit-retain-self` reports a block that implicitly retains `self` ("explicitly mention 'self' to indicate this is intended behavior"); `-Warc-retain-cycles` reports a block that captures a variable strongly in a way likely to cause a retain cycle.
- `-Weverything` enables all diagnostics (including those from `-pedantic`); because some contradict each other, users typically disable many with `-Wno-...`.
- `-Wno-error=foo` keeps warning `foo` from being an error under `-Werror`, for example `-Wno-error=deprecated-declarations` while you migrate.
- Warnings are suppressed in system headers; by default a file is a system header if found via a path given with `-isystem`, so third-party headers can be added that way.
- Pragmas for local suppression:
```objc
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wundeclared-selector"
/* code */
#pragma clang diagnostic pop
```

## Gotchas
- An unknown warning flag only produces a warning (`-Wunknown-warning-option`, on by default).
- Prefer `-Werror=<name>` for chosen categories over a blanket `-Werror`.

## Self-check
Add the flags to a scratch target and fix or consciously suppress every new warning.

## Checked

2026-11-08. Every flag in the list has an entry in the Clang Diagnostic flags reference (`-Wall`, `-Wextra`, `-Wshadow`, `-Wconversion`, `-Wformat`, `-Wformat-security`, `-Wundeclared-selector`, `-Wselector`, `-Wstrict-selector-match`, `-Warc-repeated-use-of-weak`, `-Warc-retain-cycles`, `-Wimplicit-retain-self`, `-Wunguarded-availability-new`, `-Wobjc-designated-initializers`, `-Wnullability-completeness`, `-Wdeprecated-implementations`, `-Wreturn-type`, `-Wobjc-method-access`, `-Wcompletion-handler`, `-Wunknown-warning-option`, `-Wdeprecated-declarations`, `-Wpedantic`). The Clang User's Manual confirms `-Weverything`, `-Wno-error=foo`, system-header suppression via `-isystem`, and `#pragma clang diagnostic`. Removed as unconfirmed: that `-Wpedantic` is noisy with Cocoa, Xcode system-header search paths, version-dependence of flags, and SDK-update breakage. Per-flag behaviour beyond the quoted diagnostic text is not asserted.
Method: documentation only; no commands were run.
