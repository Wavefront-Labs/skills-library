---
id: computing-software.messaging-and-integration.apache-camel.loop
name: loop
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, loop, dowhile, camelloopindex]
level: intro
status: docs-checked
description: "Camel Loop EIP: count, copy and doWhile modes, CamelLoopIndex and CamelLoopSize, breakOnShutdown and body flow between iterations."
sources:
  - https://camel.apache.org/components/next/eips/loop-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loop

Runs the steps repeatedly. `expression` (required) gives the count, converted to an integer; a non-integer throws `RuntimeCamelException`.

Modes:
- Default: the same Exchange is reused, so each iteration starts from the previous result.
- `copy` (default false): each iteration uses a copy of the original.
- `doWhile` (default false): loops until the expression is `false` or `null`.

Other options: `breakOnShutdown` (default false), `onPrepare`, `disabled` (default false).

Properties: `CamelLoopIndex` (from 0) and `CamelLoopSize` (not available in while mode).

Bodies: the first iteration sees the original body; later ones see the previous output, or the original again in copy mode. Output is the last iteration's result.

Examples: `loop(8)` sends to `mock:result` eight times; the count can be `header("loop")` or `xpath("/hello/@times")`. With copy mode and three loops, appending "B" to "A" gives "AB" each time; without it "AB", "ABB", "ABBB". `loopDoWhile(simple("${body.length} <= 5"))` loops while the body is 5 chars or fewer.

Keep counts at about 10,000 or fewer.

Verify: `loop(3)` yields `CamelLoopIndex` values 0, 1, 2.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full Loop EIP page source (loop-eip.adoc) and the Loop model definition (loop.json) from the apache/camel repository, which generate the cited page. Confirmed the three modes, the option defaults (copy, doWhile, breakOnShutdown, disabled all false), onPrepare, the integer requirement and RuntimeCamelException, CamelLoopIndex (0 based) and CamelLoopSize (not in while mode), body flow, the 10000 guidance and all examples. Nothing was removed. No commands were run.
