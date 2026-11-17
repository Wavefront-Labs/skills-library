---
id: computing-software.software-engineering.javascript.js-atomics-wait-notify
name: js-atomics-wait-notify
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, atomics-wait, js-atomics]
level: advanced
status: docs-checked
description: "Use the Atomics namespace (load, store, add, compareExchange, wait, notify) on shared memory; know return values and main-thread limits."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atomics operations, wait and notify

- `Atomics` is a non-constructor namespace of static methods for atomic operations on `SharedArrayBuffer` and `ArrayBuffer` typed arrays.
- `Atomics.add()`, `sub()`, `and()`, `or()`, `xor()` and `exchange()` return the old value at the index; `store()` returns the stored value; `load()` reads the value; `compareExchange()` stores a value only if the current one equals the expected value and returns the old value.
- `Atomics.wait()` verifies the index still holds the expected value and sleeps until notified or timed out, returning `"ok"`, `"not-equal"` or `"timed-out"`. If waiting is not allowed in the calling agent it throws; most browsers do not allow it on the main thread. `Atomics.waitAsync()` waits without blocking and returns an object representing the result.
- `Atomics.notify()` wakes agents waiting on an index and returns the number notified.
- `Atomics.pause()` hints to the CPU that the caller is spinning while waiting on a shared resource.
- `SharedArrayBuffer` is not defined unless its security requirements are met, so examples cannot run on an arbitrary page.

Self-check: with `ta[0] = 5` on a shared typed array, `Atomics.add(ta, 0, 12)` returns 5 and `Atomics.load(ta, 0)` then returns 17 (MDN example).

## Checked

Date: 2026-11-03. Confirmed on MDN Global_Objects/Atomics: method descriptions and return values, wait results and main-thread note, waitAsync, notify, pause, SharedArrayBuffer security note, add/load example. Removed as not stated there: the exact `wait`/`notify` argument lists, the mutex recipe, the Int32Array/BigInt64Array restriction, racy plain read advice, and the two-worker counter self-check.

Method: documentation only; no commands were run.
