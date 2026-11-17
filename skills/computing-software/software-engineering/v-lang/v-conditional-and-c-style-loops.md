---
id: computing-software.software-engineering.v-lang.v-conditional-and-c-style-loops
name: v-conditional-and-c-style-loops
category: computing-software
field: software-engineering
product: v-lang
tags: [v-conditional-and-c-style-loops, loops-and-labels, while loop, infinite loop, c-style for, for cond, loop, iteration, v-lang]
level: intro
status: docs-checked
description: "Use for cond {}, for {} and for i := 0; i < n; i++ forms; V has a single for keyword and no while."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# while-style, infinite and C-style loops

Goal: pick the right loop form; V has only the `for` keyword.

- Condition ("while"): `for i <= 100 { sum += i; i++ }`; no parentheses around the condition and the braces are always required.
- Bare (infinite): `for { num += 2; if num >= 10 { break } }`.
- C-style: `for i := 0; i < 10; i += 2 { if i == 6 { continue } }`; `i` does not need `mut` because it is always mutable.
- Labelled `break` and `continue` target an outer loop: `outer: for ... { for { continue outer } }`; the label must immediately precede the outer loop.
- Do-while pattern: use a bare `for` with a conditional `break` at the end.

Gotchas:
- The condition form is easy to turn into an infinite loop if you forget to update the counter, which is why the docs call the C-style loop safer.

Verify: run a countdown loop and assert the final value.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Condition for", "Bare for", "C for", "Labelled break & continue"). Removed as not stated: the one-init/one-post limitation, the `os.get_line` EOF example, and the closure-capture remark about C-style loop variables.

Method: documentation only; no commands were run.
