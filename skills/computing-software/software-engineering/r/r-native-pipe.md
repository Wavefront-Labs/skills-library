---
id: computing-software.software-engineering.r.r-native-pipe
name: r-native-pipe
category: computing-software
field: software-engineering
product: r
tags: [r, r-pipes, native-pipe]
level: practitioner
status: docs-checked
description: "Use"
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/pipeOp.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native pipe versus magrittr
- `|>` arrived in R 4.1.0 and is a syntax transform: `x |> f(y)` is parsed as `f(x, y)`.
- The right-hand side must be a call; syntactically special functions such as `+` or `if` are not allowed.
- A `_` placeholder can name the argument that receives the left-hand side, once, e.g. `df |> lm(y ~ x, data = _)`; `_` can also head an extraction chain such as `_$coef[[2]]`. The page gives no version for these; check R NEWS for the release.
- `\(x) x + 1` is the lambda shorthand used in the pipe examples.
Verify: `quote(x |> f())` shows the transformed call.

## Checked

Date: 2026-11-02. Confirmed on ?pipeOp (introduced in R 4.1.0, syntax transformation, call-only right-hand side, `_` placeholder rules, lambda shorthand in examples). Removed as not confirmed: the 4.2.0 and 4.3.0 version claims and the magrittr comparison.

Method: documentation only; no commands were run.
