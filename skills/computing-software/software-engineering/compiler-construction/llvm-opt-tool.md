---
id: computing-software.software-engineering.compiler-construction.llvm-opt-tool
name: llvm-opt-tool
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, opt-passes, new-pass-manager, llc-codegen, compilers, interpreters, language-implementation]
level: practitioner
status: docs-checked
description: "Running passes"
sources:
  - https://llvm.org/docs/CommandGuide/opt.html
  - https://llvm.org/docs/CommandGuide/llc.html
  - https://llvm.org/docs/NewPassManager.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# opt, llc and pass pipelines

Goal: run and inspect passes.
- `opt -passes='pass1,pass2' in.ll -S -o out.ll` runs a textual pipeline; `-S` writes textual IR instead of bitcode; `-p` is an alias for `-passes`.
- Nest by IR unit when needed: `-passes='function(no-op-function),no-op-module'`; `-debug-pass-manager` traces the run and `opt --print-passes` lists the available passes.
- `-verify-each` adds a verify pass after every pass, which finds the pass that broke the module; `-time-passes` and `-stats` report cost.
- `llc -O2 -march=x86-64 out.ll -o out.s` compiles IR to assembly; `-filetype=asm|obj|null` picks the output kind and `--print-after-isel` prints machine code after instruction selection.
- `llc --regalloc=<basic|fast|greedy|pbqp>` picks the register allocator.
Verify: IR diff shows the intended transformation.

## Checked
2026-11-08. Confirmed in the LLVM opt and llc command guides and the New Pass Manager page: `-passes`, `-S`, `-o`, `-verify-each`, `-time-passes`, `-stats`, `--print-passes`, `-p` alias, `-debug-pass-manager`, nested `function(...)` pipelines, llc `-O`, `-march`, `-filetype`, `--print-after-isel`, `--regalloc` values. Removed: the `default<O2>` pipeline string, `mem2reg,instcombine,simplifycfg` example list, `print<domtree>` and `-print-after-all` (not on these pages). The specific -march value is an example only.
Method: documentation only; no commands were run.
