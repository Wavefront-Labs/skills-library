---
id: computing-software.software-engineering.objective-c.oslog-logging
name: oslog-logging
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-debugging, oslog-logging]
level: practitioner
status: draft
description: "Log with os_log, subsystems and categories and privacy specifiers, read logs with the log command, and avoid NSLog in hot paths."
sources:
  - https://developer.apple.com/documentation/os/logging
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logging
**Goal:** structured, filterable, privacy-aware logs.

```objc
#import <os/log.h>
static os_log_t ABCLog(void) { static os_log_t l; static dispatch_once_t o; dispatch_once(&o, ^{ l = os_log_create("com.example.app", "network"); }); return l; }
os_log(ABCLog(), "fetched %{public}@ in %.2f s", url.absoluteString, elapsed);
os_log_error(ABCLog(), "failed: %{public}@", error.localizedDescription);
os_log_debug(ABCLog(), "details %@", obj);          // not persisted by default
```
```bash
log stream --predicate 'subsystem == "com.example.app"' --level debug
log show --last 10m --predicate 'subsystem == "com.example.app" AND category == "network"'
xcrun simctl spawn booted log stream --predicate 'process == "App"'
```
- Dynamic strings and objects are redacted (shown as `<private>`) in logs captured without a debugger unless marked `%{public}`; scalars are public by default.
- Levels: default, info, debug, error, fault.
- `NSLog` is simple and always persists; it writes through the same logging system but is heavier and has no categories; avoid in loops and never log secrets.
- Use `#if DEBUG` macros for verbose tracing.
- Sign-posts (`os_signpost`) mark intervals visible in Instruments.

## Gotchas
- `%{public}@` logs user data in the clear; check what you expose.
- Debug-level messages are not stored unless enabled.

## Self-check
Run `log stream` with your subsystem predicate and confirm lines appear.
