---
id: computing-software.software-engineering.ruby.ruby-enumerators-lazy
name: ruby-enumerators-lazy
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-blocks, enumerators-lazy]
level: practitioner
status: docs-checked
description: "Use Enumerator, external iteration with next and Enumerator::Lazy for large or infinite sequences."
sources: ["https://docs.ruby-lang.org/en/master/Enumerator.html", "https://docs.ruby-lang.org/en/master/Enumerator/Lazy.html", "https://docs.ruby-lang.org/en/master/Kernel.html", "https://docs.ruby-lang.org/en/master/Proc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enumerators and lazy enumeration
- Iterator methods that accept a block may return an `Enumerator` when called without one (for example `each_slice`, `each_cons`, `each_with_index`).
- `Enumerator::Lazy` is for long or infinite sequences and chains calculations without building intermediate arrays; `first(n)` or `to_a` / `force` evaluate it. Example: `(1..Float::INFINITY).lazy.select(&:even?).map { _1 * 2 }.first(5)`.
- `Enumerator.new { |y| y << 1 }` creates a generator; external `next` raises `StopIteration` at the end and `Kernel#loop` rescues `StopIteration`.
- Blocks may use numbered parameters (`_1`) and `it` for the implicit parameter.
Verify: print side effects inside lazy steps to confirm they run only on demand.

## Checked
2026-11-02. Confirmed against: Enumerator, Lazy, Kernel#loop (rescues StopIteration), Proc numbered parameters / it. Removed or softened (not stated on those pages): version tags.
Method: documentation only; no commands were run.
