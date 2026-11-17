---
id: computing-software.software-engineering.compiler-construction.mlir-pattern-rewrites
name: mlir-pattern-rewrites
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, rewrite-patterns, dag-rewriter, canonicalization, compilers, interpreters, language-implementation]
level: practitioner
status: docs-checked
description: "Transformations"
sources:
  - https://mlir.llvm.org/docs/PatternRewriter/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pattern rewriting

Goal: write transformations.
- Patterns inherit from `RewritePattern`; the match-and-rewrite logic lives in `matchAndRewrite(Operation *op, PatternRewriter &rewriter)`, and no IR mutation may happen before the match is deemed successful.
- All IR mutation, including creation and erasure, goes through the `PatternRewriter` (for example `eraseOp`, never `op->erase()`), including changes to nested ops, regions and blocks.
- Each pattern has a `PatternBenefit`; register patterns in a `RewritePatternSet` (`patterns.add<MyPattern>(/*benefit=*/1, ctx)`).
- The same framework backs canonicalization, dialect conversion and general transformation.
Verify: the transformed IR matches the expected output.

## Checked
2026-11-08. Confirmed in the MLIR Pattern Rewriting page (pattern structure, benefit, `matchAndRewrite`, rewriter rules, `RewritePatternSet`). Removed: DRR, greedy canonicalization driver, pass manager composition and FileCheck lit-test advice (not on this page).
Method: documentation only; no commands were run.
