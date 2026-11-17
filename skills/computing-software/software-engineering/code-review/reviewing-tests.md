---
id: computing-software.software-engineering.code-review.reviewing-tests
name: reviewing-tests
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, reviewing-a-diff, reviewing-tests, test-quality, mutation-testing, test-smells, coverage]
level: practitioner
status: docs-checked
description: "Review tests as carefully as production code: are they present, correct, do they fail when the code is wrong, and are their assertions simple and useful?"
sources: ["https://google.github.io/eng-practices/review/reviewer/looking-for.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reviewing tests

**Goal:** tests in the change would actually catch the bugs they claim to prevent, and
won't become a maintenance burden. This follows the "Tests" section of Google's guide
"What to look for in a code review".

## Questions to ask
1. **Is there a test?** Ask for unit, integration or end-to-end tests as appropriate. In general
   tests belong in the same change as the production code, unless the change is an emergency.
2. **Are the tests correct, sensible and useful?** Tests do not test themselves and we rarely
   write tests for tests, so a human must check they are valid.
3. **Will they actually fail when the code is broken?** Think about whether they would. Try
   mentally breaking the implementation: if the tests would still pass, they are decoration.
4. **Would they produce false positives if the code changes beneath them?** Brittle tests fail
   on harmless changes.
5. **Does each test make simple and useful assertions?**
6. **Are tests separated appropriately between test methods?**
7. **Is the test code maintainable?** Tests are code that has to be maintained too. Do not accept
   complexity in tests just because they are not part of the main binary.

## Verify
- [ ] Every new behaviour or bug fix has a test that would fail without the change.
- [ ] Assertions are simple and each test method has a clear purpose.

## Checked

2026-11-08. Read in full: Google eng-practices "What to look for in a code review" (Tests section). The questions restate that section. Removed: mutation testing tool names, mocking and fakes advice, determinism rules, test-level pyramid advice, smell list, the testing blog post and book chapter sources, none of which were read in this batch.

Method: documentation only; no commands were run.
