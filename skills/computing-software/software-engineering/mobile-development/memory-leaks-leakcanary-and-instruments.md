---
id: computing-software.software-engineering.mobile-development.memory-leaks-leakcanary-and-instruments
name: memory-leaks-leakcanary-and-instruments
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-performance, leakcanary, memory-leaks, instruments-leaks, memory-graph-debugger, retain-cycles, android, ios, weak-self]
level: practitioner
status: docs-checked
description: "Find and fix Android memory leaks: LeakCanary detection and leak traces, Android Studio heap dumps, and the classic leak patterns."
sources: ["https://square.github.io/leakcanary/fundamentals-how-leakcanary-works/", "https://developer.android.com/studio/profile/capture-heap-dump"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory leaks: LeakCanary and heap dumps

**Goal:** catch leaked screens and objects during development, before they show up as
out-of-memory kills and slowness.

## Android: LeakCanary
Once installed (as a debug-only dependency) it needs no code. It hooks into the Android lifecycle and passes these
objects to an `ObjectWatcher`, which holds weak references to them:
- destroyed `Activity` instances
- destroyed `Fragment` instances
- destroyed fragment `View` instances
- cleared `ViewModel` instances

Watch anything else with `AppWatcher.objectWatcher.watch(myDetachedView, "View was detached")`.

If the weak reference is not cleared after 5 seconds and a garbage collection, the object is retained and possibly
leaking. LeakCanary waits for a threshold of retained objects before dumping the heap: 5 while the app is visible,
1 when it is not (so pressing Home triggers a dump within 5 seconds). Tapping the notification dumps immediately.
Dumping freezes the app briefly. The `.hprof` is parsed with Shark, which computes each retained object's **leak
trace**, the reference path that prevents collection.

- Suspect references are underlined (`~~~` in the text form); the signature of a leak is a hash of those suspect
  references, and leaks with the same signature are grouped as one bug.
- Leaks are split into Application Leaks and Library Leaks (known bugs in third-party or SDK code, matched by reference
  names against a built-in database). Library leaks may not be fixable by you; consider reporting the bug.

## Android Studio heap dump
Capture with the Analyze Memory Usage (Heap Dump) task; call `dumpHprofData()` to dump at a precise point. In the class
drop-down choose **Show activity/fragment leaks**. In single-activity Compose apps, Activity leaks are the critical
ones because they retain the whole Compose hierarchy. Studio Quail 2 and later integrates LeakCanary as a Profiler task.
Look in the class and instance lists for large Retained Size and for these causes:
- Long-lived references to an Activity or Context (including from state holders or lambdas that capture Context).
- Listeners or observers not cleaned up in the `onDispose` block of a `DisposableEffect`.
- Non-static inner classes such as a `Runnable` holding an Activity.
- Caches that hold objects longer than necessary.

To provoke leaks for testing, rotate the device between portrait and landscape repeatedly and switch between your app
and others (for example Home, then back) in different activity states.

## Verify
- [ ] LeakCanary reports no leaks in a debug run through main flows.
- [ ] Repeated navigation into and out of a screen does not grow the heap dump instance count.

## Checked
2026-11-08. Confirmed against the LeakCanary page How LeakCanary works and the Android Developers page Capture a heap dump: watched object types, 5-second wait, thresholds 5 and 1, Shark, leak signature, application vs library leaks, heap dump filters, leak causes, rotation test. Removed: iOS Memory Graph, Instruments and retain-cycle sections (Apple pages not readable), the Gradle coordinates and version, the Services watch claim, `leakcanary-android-instrumentation`, the Fragment `_binding` and global-scope coroutine items, the repeat-ten-times habit (page gives no count). Page URL for heap dumps is the redirect target of the old memory-profiler link.
Method: documentation only; no commands were run.
