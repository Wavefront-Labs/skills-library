---
id: computing-software.firmware-embedded-development.bare-metal-programming.embedded-assert-and-error-strategy
name: embedded-assert-and-error-strategy
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [embedded-assert, superloop, assert-handler, fail-fast, error-handling, builtin-return-address, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Choose a firmware assert that stays in release builds cheaply (record PC/LR, not file strings) and separate bugs from expected runtime errors."
sources:
  - https://interrupt.memfault.com/blog/asserts-in-embedded-systems
  - https://gcc.gnu.org/onlinedocs/gcc/Return-Address.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assertion and error handling strategy

## Two kinds of failure
| | Programming error (bug) | Expected runtime error |
|---|---|---|
| Examples | NULL handle, index out of range, impossible state | sensor NACK, CRC mismatch, timeout |
| Response | assert: stop, record, reset or halt | return an error code, retry, degrade |

Using asserts for runtime errors makes devices reset on a loose cable; using error codes for bugs
hides them. Assert on internal preconditions; validate external input and return errors.

## Assert implementations compared (Memfault, "Asserts in Embedded Systems")
1. **Standard library `assert(expr)`**: you supply `__assert_func(const char *file, int line,
   const char *func, const char *failedexpr)`. File path, line, function and expression text are
   all passed in, which costs code space. The article's FreeRTOS test grew the `-Os` image by 25766
   bytes versus no asserts; it advises against this if code space matters.
2. **Message string per assert**: every message is stored in the binary (about 32 bytes each in the
   article's example).
3. **`__FILE__` and `__LINE__`**: works well, but `__FILE__` holds the full path (77 bytes in the
   article's example). The string is shared by asserts in the same file, so cost scales with the
   number of files containing asserts. Normalising paths to the project root helps.
4. **`__FILENAME__`** defined by the build system from the file name only: smaller than option 3.
5. **Record PC and LR only**: each assert costs a fixed number of bytes regardless of path or
   file count, and the LR gives an extra frame of backtrace. The author's measured `-Os` deltas
   over no asserts were +1693 (option 3), +1134 (option 4) and +808 bytes (option 5), versus
   +25766 for the default library assert. Resolve the addresses off-target with `addr2line`
   against the ELF of the build.

Compiler optimisation such as inlining can merge different asserts and give confusing results;
the article suggests also passing `__LINE__` to make each call unique.

## Getting the caller address with GCC
`__builtin_return_address(0)` returns the return address of the current function; `level` must be
a constant integer. When a function is inlined it returns the address of the function that is
returned to, so use the `noinline` attribute on the handler. Non-zero levels can have unpredictable
effects, including crashing, and should be used only when debugging.
```c
#define ASSERT(expr) do { if (!(expr)) assert_failed(); } while (0)

__attribute__((noinline, noreturn))
void assert_failed(void) {
    void *caller = __builtin_return_address(0);   /* identifies the failing site */
    record_crash(caller);      /* store in RAM that survives reset: your own code */
    halt_or_reset();           /* halt if a debugger is attached, else reset */
}
```
Keep the ELF for every released build so addresses can be mapped back to source lines.

## On the next boot
Read the stored record, validate it, log or upload it, then clear it. Count consecutive assert
resets and enter a safe mode after a limit you choose, rather than reset-looping.

## Where to assert
- Function preconditions on internal APIs.
- The `default:` of a state-machine switch and other unreachable code.
- Compile-time facts belong in `_Static_assert` instead.

## Verify
- [ ] A forced assert is recorded and the next boot's address maps to the right line with `addr2line`.
- [ ] The release map file shows the per-assert cost you expect.
- [ ] With a debugger attached, the assert halts instead of resetting.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the Memfault article: the five assert approaches, `__assert_func` signature, per-string and `__FILE__` sizes, code-size table, inlining caveat, addr2line use. Confirmed on the GCC Return-Address page: `__builtin_return_address` behaviour, constant level, inlining and noinline note, non-zero level warning.
Removed because the readable pages do not state them: the CMSIS and CoreDebug register names, NVIC reset call, no-init RAM details, and the QP/C qassert page (404).
