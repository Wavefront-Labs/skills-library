---
id: computing-software.software-engineering.compiler-construction.mlir-dialects-and-lowering
name: mlir-dialects-and-lowering
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, mlir-dialect, mlir-opt, conversion-passes, mlir, mlir-dialects, mlir-lowering, compilers, interpreters, language-implementation]
level: practitioner
status: docs-checked
description: "Multi-level IR"
sources:
  - https://mlir.llvm.org/docs/LangRef/
  - https://mlir.llvm.org/docs/DialectConversion/
  - https://mlir.llvm.org/docs/Tutorials/Toy/Ch-6/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dialects and lowering

Goal: understand MLIR structure.
- The language reference describes dialects, operations, blocks, regions and attributes as the core building blocks.
- Dialect conversion uses a `ConversionTarget` (what is legal at the end), conversion patterns, and a `TypeConverter` for block-argument and region signature changes.
- Lowering can be transitive: the framework may apply several patterns to legalize one operation, so you need not emit LLVM-dialect operations directly.
- The Toy tutorial lowers to the LLVM dialect by populating patterns for affine, scf-to-cf, arith, memref, cf and func (`populateSCFToControlFlowConversionPatterns`, `populateFuncToLLVMConversionPatterns`, and similar), with `LLVMConversionTarget` and `LLVMTypeConverter`.
Verify: after full conversion only operations marked legal on the target remain.

## Checked
2026-11-08. Confirmed in the MLIR Language Reference (Dialects, Operations, Blocks, Regions, Attributes), the Dialect Conversion page and Toy tutorial chapter 6. Removed: the `mlir-opt` pass flags, `mlir-translate --mlir-to-llvmir`, ODS/TableGen remark and the named dialect list (not on these pages).
Method: documentation only; no commands were run.
