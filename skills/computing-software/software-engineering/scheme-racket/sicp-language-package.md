---
id: computing-software.software-engineering.scheme-racket.sicp-language-package
name: sicp-language-package
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-language-package]
level: intro
status: draft
description: "Use the sicp package (#lang sicp) with SICP's cons-stream, true/false and nil conventions and the picture-language support."
sources:
  - https://docs.racket-lang.org/guide/languages.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The sicp language package
**Goal:** follow the book exactly.
```bash
raco pkg install sicp
```
```racket
#lang sicp
(define s (cons-stream 1 (cons-stream 2 '())))
```
- Provides `cons-stream`, `stream-car`, `stream-cdr`, `inc`, `dec`, `nil`, `true`, `false`.
- Uses mutable pairs semantics aligned with the book; behaviour versus `#lang racket` differs (confirm in the package docs).
## Self-check
Evaluate `(stream-car (stream-cdr s))` giving `2`.
