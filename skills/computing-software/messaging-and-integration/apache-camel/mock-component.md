---
id: computing-software.messaging-and-integration.apache-camel.mock-component
name: mock-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, mock, testing, assertions]
level: intro
status: docs-checked
description: "Camel mock component: expectedMessageCount and body expectations, assertIsSatisfied wait of 10 seconds, assertPeriod for zero-message tests, retainFirst and retainLast limits."
sources:
  - https://camel.apache.org/components/next/mock-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mock:

Expectations (set before sending):
- `expectedMessageCount(int)`, `expectedMinimumMessageCount(int)`
- `expectedBodiesReceived(...)` in order
- `expectedHeaderReceived(...)`
- `expectsAscending(Expression)`, `expectsDescending(Expression)`
- `expectsNoDuplicates(Expression)`

`assertIsSatisfied()` waits for messages up to the result wait time, default 10 seconds (`setResultWaitTime(millis)`). `setAssertPeriod(millis)` keeps checking after expectations are met to confirm no more messages arrive.

Endpoint options (defaults): `expectedCount` -1, `failFast` true (fail at the first mismatch), `copyOnExchange` true (deep copy), `retainFirst` -1, `retainLast` -1, `browseLimit` 100 (0 unlimited), `log` false, `lazyStartProducer` false. Others: `resultWaitTime`, `resultMinimumWaitTime`, `reportGroup`, `sleepForEmptyTest`.

Gotchas:
- An expected count of 0 matches immediately; set `assertPeriod` so the test waits long enough to confirm nothing arrives.
- Mocks hold every received Exchange until reset or JVM restart. For high volume use `retainFirst` and `retainLast`; expectations then apply to retained messages only, while `getReceivedCounter()` still reports the true total.

Verify: with `expectedMessageCount(2)`, `assertIsSatisfied()` waits (10 seconds by default) for the expectation to be met, and with `assertPeriod` set it keeps checking afterwards that nothing extra arrives.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel mock component page: the expectation methods, the 10 second assertIsSatisfied wait, setAssertPeriod, the zero-count warning, endpoint option defaults (expectedCount -1, failFast true, copyOnExchange true, retainFirst -1, retainLast -1, browseLimit 100, log false, lazyStartProducer false), the other listed options and the retention behaviour (getReceivedCounter still reports the real total) match. The old verify line claimed a failure outcome the page does not state; it was reworded. No commands were run.
