---
id: computing-software.software-engineering.assembly.nasm-macros
name: nasm-macros
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, nasm-macros, asm-nasm]
level: practitioner
status: docs-checked
description: "NASM preprocessor macros: single-line and multi-line macros, parameters, defaults, local labels with %%, conditionals and repetition."
sources:
  - https://www.nasm.us/doc/nasm05.html
  - https://www.nasm.us/doc/nasm02.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NASM macros and conditionals
**Goal:** remove repetition without hiding control flow.

```nasm
%define ARG0 rdi                      ; single-line text macro

%macro FN_ENTER 1                     ; one parameter
    push rbp
    mov  rbp, rsp
    sub  rsp, %1
%endmacro

%macro FN_LEAVE 0
    leave
    ret
%endmacro

%macro MAXU 2                         ; %1 = max(%1, %2), unsigned
    cmp  %1, %2
    jae  %%done                       ; %% label is unique per expansion
    mov  %1, %2
%%done:
%endmacro

%macro SAVE 1-3 rbx, r12              ; 1 to 3 params, defaults for missing
    %rep %0
        push %1
        %rotate 1
    %endrep
%endmacro

%ifdef WIN64
    %define SHADOW 32
%else
    %define SHADOW 0
%endif
%include "common.inc"
```
- `%1`, `%2` are parameters; `%0` is the count. In `%macro name min-max defaults`, the minimum number of parameters is required and the defaults fill the optional ones in order; `*` as the maximum means no upper limit.
- `%%name` labels get a unique name (of the form `..@2345.name`) on each expansion; a plain label inside a macro would be defined twice on the second use.
- Conditionals are `%if`, `%ifdef`, `%ifmacro`, `%ifidn` and others, each with `%elif`, `%else`, `%endif` and `%ifn` inverse forms; `%if` takes a critical expression. `%ifdef` pairs with `-dNAME` on the command line.
- `%rep count` repeats a block; a maximum count is always required, and `%exitrep` leaves early. `%assign i i+1` is the usual loop counter. `TIMES` cannot repeat a macro because it runs after macro expansion.
- `%rotate n` rotates the parameter list left (negative: right) without losing any, which makes the `%rep %0` push loop above work.
- Run `nasm -E file.asm` to see the preprocessed output (comments and directives removed) when debugging macros.

## Gotchas
- Naming a macro after an instruction overloads that instruction: with `%macro push 2`, `push ebx` still assembles but gives a warning (silenced with `-w-macro-params`). Prefer a distinct name such as `FN_ENTER`, not `ENTER`.
- A macro that clobbers flags or registers should say so in a comment; the caller cannot tell.
- `%macro` and `%define` are case-sensitive; `%imacro` and `%idefine` make them case-insensitive, which the manual recommends avoiding unless needed.
- Multi-line macros can be overloaded by parameter count, but a single-line `%define foo bar` without parameters blocks any parameterised `foo`.

## Self-check
Expand your macro with `nasm -E` twice in a row and verify both `%%done` labels differ.

## Checked
2026-11-08. Checked against the NASM 3.02 manual: chapter 5 (single-line macros and overloading, %assign, multi-line macros, macro-local labels, default parameters, %0, %rotate, conditional assembly, %ifdef and -d, %rep and %exitrep, %imacro) and chapter 2 (the -E preprocess-only option). Changed: the macro `ENTER` was renamed because naming a macro after an instruction overloads it. Removed: the "define a macro before using it (single pass)" claim, which the manual does not state.

Method: documentation only; no commands were run.
