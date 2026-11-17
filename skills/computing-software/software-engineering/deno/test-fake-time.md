---
id: computing-software.software-engineering.deno.test-fake-time
name: test-fake-time
category: computing-software
field: software-engineering
product: deno
tags: [test, fake-time, timers, date, tick, std-testing]
level: practitioner
status: docs-checked
description: "Control Date, setTimeout and setInterval in tests with FakeTime from @std/testing/time, advancing the clock with tick() instead of waiting."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/mocking.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`FakeTime` from `jsr:@std/testing/time` replaces `Date`, `setTimeout`, `setInterval` and friends with controllable versions. Pin the date and advance instantly with `tick()`. It is disposable, so `using` restores the real clock at test end.

```ts
import { assertEquals } from "jsr:@std/assert";
import { FakeTime } from "jsr:@std/testing/time";

function isWeekend(): boolean {
  const day = new Date().getDay();
  return day === 0 || day === 6; // 0 is Sunday, 6 is Saturday
}

function delayedGreeting(callback: (message: string) => void): void {
  setTimeout(() => callback("Hello after delay"), 1000);
}

Deno.test("time-dependent tests", () => {
  using time = new FakeTime(new Date("2023-05-01T12:00:00Z"));

  assertEquals(isWeekend(), false);

  // Advance 5 days to Saturday
  time.tick(5 * 24 * 60 * 60 * 1000);
  assertEquals(isWeekend(), true);

  let greeting = "";
  delayedGreeting((message) => {
    greeting = message;
  });
  time.tick(1000);
  assertEquals(greeting, "Hello after delay");
});
```

Timers fire as soon as the fake clock passes them. Use it for scheduling and expiry features, polling and debouncing, or anything where the real clock makes tests slow or flaky, rather than stubbing `Date` by hand.

## Checked

2026-11-04. Confirmed against docs runtime/test/mocking.md: FakeTime from @std/testing/time, tick(), using restore, example behaviour.

Method: documentation only; no commands were run.
