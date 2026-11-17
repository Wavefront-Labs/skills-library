---
id: computing-software.software-engineering.objective-c.code-coverage
name: code-coverage
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-testing, code-coverage]
level: practitioner
status: draft
description: "Collect and read coverage with xcodebuild -enableCodeCoverage and xccov, and set coverage targets sensibly."
sources:
  - https://developer.apple.com/documentation/xctest
  - https://developer.apple.com/documentation/xcode
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Code coverage
**Goal:** measure which Objective-C lines tests execute.

```bash
xcodebuild test -scheme App -destination '...' -enableCodeCoverage YES -resultBundlePath build/R.xcresult
xcrun xccov view --report build/R.xcresult              # per-target and per-file percentages
xcrun xccov view --report --json build/R.xcresult > cov.json
xcrun xccov view --file Sources/ABCCart.m build/R.xcresult   # line-level view
```
- Xcode: scheme > Test > Options > Gather coverage for selected targets.
- Instrumentation uses clang's `-fprofile-instr-generate -fcoverage-mapping` under the hood (set by Xcode's coverage option).
- On Linux/GNUstep use `--coverage` with gcov/llvm-cov (`llvm-cov report`).
- Set thresholds in CI by parsing the JSON (`lineCoverage` field).
- Exclude generated code and vendored sources from the coverage targets.

## Gotchas
- Coverage counts executed lines, not assertion quality.
- Unit-test hosts that crash produce no coverage.

## Self-check
Add a test for a previously uncovered branch and see the percentage rise.
