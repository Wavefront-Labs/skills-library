---
id: computing-software.software-engineering.dart.dart-zones-error-handling
name: dart-zones-error-handling
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-zones, zones-error-handling]
level: advanced
status: docs-checked
description: "Catch uncaught async errors with runZonedGuarded and pass context via zone values."
sources: ["https://dart.dev/libraries/async/zones"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# runZonedGuarded, zone values and error handling
- `runZonedGuarded(() { main2(); }, (error, stack) { log(error, stack); });` makes the new zone's `onError` the uncaught-error handler, so errors from unawaited futures and timers created inside (for example a `Timer.run` callback that throws) reach it instead of crashing the program. By default an uncaught error crashes the program.
- Unlike `try`/`catch`, the zone keeps running after an uncaught error, so the handler can run more than once.
- Errors on Future chains never cross error-zone boundaries, in either direction: an error cannot enter an error zone, and a future chain created inside cannot propagate its error out (a `catchError` outside never fires).
- `runZoned(body, zoneValues: {#reqId: 42})` and `Zone.current[#reqId]` carry request context across async gaps. Values are inherited by nested zones and can be shadowed; you cannot change what a key maps to, but you can mutate the object. Use unique key objects (typically symbol literals) to avoid clashes with other libraries.
- `ZoneSpecification` can override forking, callback registration and running (`run`, `registerCallback`...), `scheduleMicrotask`, timers, uncaught-error handling and `print`.
- Zone rules: a callback runs in the zone where it was scheduled; stream callbacks run in the zone where the stream is listened to, not where `map()` was called.
- Handling uncaught errors does not require zones: `Isolate.run()` also listens for uncaught errors.

Verify: throw inside an unawaited future or a `Timer.run` callback within `runZonedGuarded` and see the handler run.

## Checked

Checked 2026-11-08 against the Dart "Zones" page (https://dart.dev/libraries/async/zones), read in full. Confirmed: runZonedGuarded onError semantics, default crash, error-zone boundary rules, zoneValues semantics and inheritance, ZoneSpecification override list, stream zone rule, Isolate.run note. Removed: the unsupported claim about ensureInitialized-style frameworks, the claim that test fakes use ZoneSpecification, and the placeholder second source entry.

Method: documentation only; no commands were run.
