---
id: computing-software.software-engineering.c.hardening-flags-fortify-stack-protector-relro
name: hardening-flags-fortify-stack-protector-relro
category: computing-software
field: software-engineering
product: c
tags: [c, hardening-flags, fortify-source, stack-protector, relro, pie]
level: advanced
status: docs-checked
description: "Build C binaries with stack protector, FORTIFY_SOURCE, PIE and RELRO hardening and verify them."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://wiki.sei.cmu.edu/confluence/display/c/", "https://gcc.gnu.org/onlinedocs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardening flags fortify stack protector relro

Goal: raise the cost of exploiting any remaining memory bug.

- Typical GCC/Clang flags: `-O2 -D_FORTIFY_SOURCE=2` (`=3` needs gcc 12 or later or clang 9 or later per feature_test_macros(7); fortification needs compiler optimisation), `-fstack-protector-strong`, `-fPIE` with link `-pie`, `-Wl,-z,relro,-z,now`, `-fstack-clash-protection`; x86 `-fcf-protection`; arm64 `-mbranch-protection=<features>` (see GCC AArch64 Options).
- Distribution defaults vary; check your toolchain instead of assuming.
- Verify the result on the finished binary with `readelf` (program headers and dynamic section) or a checker such as `checksec`; confirm the output format on your platform.
- Hardening does not fix bugs and can fail silently if flags are not passed at link time too (pass `CFLAGS` and `LDFLAGS` consistently).
- Also consider `-ftrivial-auto-var-init=zero` (GCC; check your compiler version) to zero locals and a hardened allocator for deployments.

Verify: run the checker on the release artifact in CI and fail on missing PIE/RELRO/canary.

## Checked

2026-11-02. Confirmed in GCC Instrumentation Options (`-fhardened` list: `-D_FORTIFY_SOURCE`, `-fstack-protector-strong`, `-fstack-clash-protection`, `-fPIE -pie -Wl,-z,relro,-z,now`, `-ftrivial-auto-var-init=zero`, `-fcf-protection`), feature_test_macros(7) for the `=3` gate, AArch64 Options for `-mbranch-protection`. Removed: `noexecstack`, the `standard` keyword, the full-RELRO label, distro names, `file`/`BIND_NOW` output details and the Clang version claim.

Method: documentation only; no commands were run.
