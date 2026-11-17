---
id: computing-software.firmware-embedded-development.bare-metal-programming.embedded-c-warning-flags
name: embedded-c-warning-flags
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [compiler-warnings, arm-none-eabi-gcc, wconversion, werror, static-checking, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Pick a GCC warning set for firmware (-Wall -Wextra -Wconversion -Wdouble-promotion -Wshadow...), apply it to your code but not vendor code, and ratchet to -Werror."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html
  - https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html
  - https://gcc.gnu.org/onlinedocs/gcc/Diagnostic-Pragmas.html
  - https://gcc.gnu.org/onlinedocs/cpp/System-Headers.html
  - https://cmake.org/cmake/help/latest/command/target_include_directories.html
  - https://cmake.org/cmake/help/latest/prop_tgt/COMPILE_WARNING_AS_ERROR.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Warning flags for embedded C

Warnings are the cheapest static analysis you have. On firmware the important ones are about
integer width, implicit float promotion and silent truncation.

## Example set
```cmake
set(FW_WARNINGS
  -Wall -Wextra
  -Wconversion -Wsign-conversion     # implicit narrowing: uint32_t -> uint16_t, int -> unsigned
  -Wdouble-promotion                  # float silently promoted to double (soft-double on M4F!)
  -Wshadow -Wundef                    # shadowed locals; #if on an undefined macro
  -Wcast-align -Wcast-qual
  -Wformat=2 -Wformat-truncation
  -Wimplicit-fallthrough
  -Wnull-dereference -Wduplicated-cond -Wlogical-op
  -Wstrict-prototypes -Wmissing-prototypes   # C only: catches non-static helpers and void f() declarations
  -Wstack-usage=512                   # example budget in bytes: pick one that fits your stacks
)
target_compile_options(app PRIVATE ${FW_WARNINGS})
```
Most valuable for MCU code:
- `-Wdouble-promotion`: `float y = x * 1.5;` computes in double (software emulated on
  single-precision FPUs); write `1.5f`.
- `-Wconversion`: `uint8_t len = strlen(s);` truncation; `TIM->ARR = period_us * 2;` overflow paths.
- `-Wstack-usage=N`: warns when a function's conservatively computed stack use might exceed N bytes;
  `alloca` and variable-length arrays count towards it.
- `-Wundef`: `#if STM32F4` when the macro is spelled `STM32F4xx` silently evaluates to 0.

## Vendor code
HAL, CMSIS and middleware will drown you in warnings. Mark their include paths as system (GCC suppresses warnings in
system headers, and `-isystem` or `-idirafter` directories count as system) so their headers don't
warn, and compile their sources in a separate target without the strict set:
```cmake
target_include_directories(app SYSTEM PRIVATE ${CMSIS_INC} ${HAL_INC})
add_library(vendor STATIC ${HAL_SRCS})
target_compile_options(vendor PRIVATE -w)     # -w inhibits all warnings; or use a relaxed set
```

## Ratchet to -Werror
1. Turn on the set, count warnings per category.
2. Fix or suppress narrowly (`#pragma GCC diagnostic push/ignored/pop` around one line, with a
   comment).
3. Enable `-Werror` in CI (`set_property(TARGET app PROPERTY COMPILE_WARNING_AS_ERROR ON)`, CMake
   3.24+) so new warnings fail the build; developers can override locally with
   `cmake --compile-no-warning-as-error`.
Pin the compiler version: new GCC releases add warnings and break `-Werror` builds.

## Complement with
`-fanalyzer`: much more expensive than other GCC warnings, neither sound nor complete, and only
suitable for C code in the release the page documents. Warnings catch the cheap things; they don't
replace a dedicated static analyser.

## Verify
- [ ] A clean build prints zero warnings for project code.
- [ ] CI fails when a warning is introduced (test with a deliberate `float f = 1.0 * x;`).

## Checked
2026-11-08. Confirmed in the GCC manual (Warning Options for each listed flag, `-w`, `-Werror`; Static Analyzer
Options; Diagnostic Pragmas), the GCC preprocessor manual (System Headers), and the CMake manual
(`COMPILE_WARNING_AS_ERROR` added in 3.24 and ignored under `--compile-no-warning-as-error`;
`target_include_directories` SYSTEM). Removed: the "GCC 12+" and "GCC 10+" version claims, the blog source
(not read in full), and the MISRA remark. The `-Wstack-usage=512` value is an example, not a recommendation.
Method: documentation only; no commands were run.
