---
id: computing-software.software-engineering.cpp.warning-suppression-and-pragmas
name: warning-suppression-and-pragmas
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-tooling, cpp-tl-warning-suppression, pragmas, diagnostics, gcc, clang, msvc, system-headers, warning-suppression]
level: practitioner
status: docs-checked
description: "Suppress C++ compiler warnings narrowly and portably: pragma push/pop for GCC, Clang and MSVC, system headers, and per-warning error control."
sources: ["https://gcc.gnu.org/onlinedocs/gcc/Diagnostic-Pragmas.html", "https://clang.llvm.org/docs/UsersManual.html#controlling-diagnostics-via-pragmas", "https://learn.microsoft.com/en-us/cpp/preprocessor/warning"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Warning suppression and pragmas

Prefer fixing the code. When a warning is a false positive or comes from code you do not own, suppress it as narrowly as possible, with a comment saying why.

## Per-compiler pragmas
```cpp
// GCC and Clang (Clang treats "GCC diagnostic" and "clang diagnostic" as synonyms)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wformat"      // option name is a double-quoted string
/* code that triggers the warning */
#pragma GCC diagnostic pop

// MSVC
#pragma warning(push)
#pragma warning(disable : 4507 4034)           // warning numbers
/* code */
#pragma warning(pop)
```
- GCC: `#pragma GCC diagnostic kind "-Woption"` where kind is `error`, `warning` (even if `-Werror` is in effect) or `ignored`. Only warnings can be controlled, and not all of them (use `-fdiagnostics-show-option` to see which option controls a diagnostic). These pragmas override command-line options, and only affect diagnostics at or after the pragma's position in the file.
- `push` remembers the diagnostic state and `pop` restores it. In GCC a `pop` with no matching `push` restores the command-line options; Clang does not yet support that behaviour, so a bare `ignored` not guarded by `push`/`pop` differs between compilers. Always pair them.
- GCC ignores `#pragma clang diagnostic`, so use the `GCC` spelling when GCC must also honour the pragma.
- MSVC `#pragma warning(disable : N, justification : "reason")` records a reason (the `justification` property works with `disable` and `suppress`); `#pragma warning(suppress : N)` disables the warning for the next line only and then restores the state.

## Other tools
- System headers: Clang suppresses warnings that occur in system headers; by default an included file is a system header if it was found through a path given with `-isystem`.
- Keep `-Werror` on but exempt one class with `-Wno-error=<warning>` (Clang manual) instead of disabling the warning entirely.

## Gotchas
- A suppression pragma hides real bugs when the surrounding code changes; review each one like code and keep the reason comment next to it.
- Not every GCC diagnostic can be modified by `#pragma GCC diagnostic`; if a pragma has no effect, check with `-fdiagnostics-show-option` that the diagnostic is controllable.

## Verify
- [ ] Build with `-Werror` on each compiler you support: no warnings escape from the suppressed region and none leak after the `pop`.

## Checked
2026-11-09. Confirmed on the GCC Diagnostic Pragmas page (kinds, string option, override of command line, position rule, push/pop and unmatched pop, -fdiagnostics-show-option and not all diagnostics modifiable), the Clang User's Manual section on controlling diagnostics via pragmas (GCC/clang spelling synonyms, GCC ignores clang spelling, unpaired pop difference, system headers and -isystem, -Wno-error=foo) and the MSVC warning pragma page (push, pop, disable, suppress, justification). Removed as not on those pages: the macro wrappers and warning 4996, [[maybe_unused]], fallthrough and std::ignore advice, MSVC /external options, CMake SYSTEM and COMPILE_OPTIONS tips, clang-tidy NOLINT, GCC middle-end pragma caveats, __has_warning and -Wunknown-pragmas notes.
Method: documentation only; no commands were run.
