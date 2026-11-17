---
id: computing-software.qa-testing-engineering.test-automation.test-sizes-small-medium-large
name: test-sizes-small-medium-large
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [test-sizes, small-medium-large-tests, test-classification, hermetic-tests, test-strategy]
level: practitioner
status: docs-checked
description: "Classify tests as Google-style small, medium or large by what they may touch (process, network, disk, sleep) and map sizes to Bazel timeouts; size differs from scope."
sources:
  - https://testing.googleblog.com/2010/12/test-sizes.html
  - https://abseil.io/resources/swe-book/html/ch11.html
  - https://bazel.build/reference/test-encyclopedia
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test sizes (small/medium/large)

**Goal:** classify tests by what they are allowed to do, because that predicts speed and flakiness better than arguments over "unit" versus "integration".

## Definitions
Google Testing Blog (2010) table:

| | Small | Medium | Large |
|---|---|---|---|
| Network | no | localhost only | yes |
| Database | no | yes | yes |
| File system | no | yes | yes |
| External systems | no | discouraged | yes |
| Multiple threads | no | yes | yes |
| Sleep statements | no | yes | yes |
| Time limit (s) | 60 | 300 | 900+ |

*Software Engineering at Google* ch. 11 adds the process view:
- Small: must run in a single process (often a single thread); no sleeping, I/O or other blocking calls, so no network or disk (test doubles replace heavy dependencies; a hermetic in-memory file system is allowed).
- Medium: may span processes, use threads and make blocking calls, including to localhost, but not to other systems; contained in one machine.
- Large: removes the localhost restriction; test and system may span machines.
- Size and scope are separate properties: for example a narrow-scoped test of a method can still need to be medium size. The book's rough guide is about 80% narrow unit tests, 15% medium-scoped integration tests and 5% end-to-end tests (scope, not size).
- The book says Google encourages small tests wherever possible, and that rerunning flaky tests trades CPU for engineering time but only delays fixing the root cause. All tests should aim to be hermetic.

## Bazel
Test encyclopedia: `timeout` values are short 60 s, moderate 300 s, long 900 s, eternal 3600 s. A test with no explicit timeout gets one implied by size: small is short, medium is moderate, large is long, enormous is eternal. Size also sets assumed peak resource usage. Set timeouts as tight as possible without flakiness.

## Enforcement (from the blog)
The blog describes marking size with a Java annotation (no annotation means Small) and installing a security manager per size to disallow activities, so tests police the limits; it also requires tests to run in any order and so be isolated.

## Verify
Every test has a size, small tests mechanically fail when they open sockets or touch disk, and timeouts follow size.

## Checked
2026-11-08. Confirmed against the three pages above. Removed (not stated in them): pytest, JUnit 5 and Jest enforcement recipes, `pytest-socket`, the claim that Bazel `size` is orthogonal to scope in the rules sense, CI scheduling by size (small on save, medium on PR, large nightly), and the flaky-rate-by-size advice. Corrected the 80/15/5 ratio, which is about scope, not size.
Method: documentation only; no commands were run.
