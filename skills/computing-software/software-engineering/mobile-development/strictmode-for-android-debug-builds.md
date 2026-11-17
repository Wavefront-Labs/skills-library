---
id: computing-software.software-engineering.mobile-development.strictmode-for-android-debug-builds
name: strictmode-for-android-debug-builds
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, strictmode, threadpolicy, vmpolicy, main-thread-io, leaked-closeables, debug-tooling]
level: practitioner
status: docs-checked
description: "Catch accidental main-thread disk and network access and leaked resources in Android debug builds with StrictMode ThreadPolicy and VmPolicy, and know its limits."
sources: ["https://developer.android.com/reference/android/os/StrictMode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# StrictMode for debug builds

StrictMode is a developer tool that detects things you might be doing by accident. It is most
commonly used to catch accidental disk or network access on the main thread; keeping that work
off the main thread also helps prevent ANR dialogs.

```kotlin
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        // enable only in debug builds, e.g. behind your own debug flag
        StrictMode.setThreadPolicy(
            StrictMode.ThreadPolicy.Builder().detectAll().build()
        )
        StrictMode.setVmPolicy(
            StrictMode.VmPolicy.Builder().detectAll().build()
        )
    }
}
```
Set the policies early, in `Application.onCreate()` or another early component method (the API
page's example). You choose what happens on a violation: `penaltyLog` writes it to the log, so
you can watch `adb logcat` while using the app. `StrictMode.enableDefaults()` is a wrapper
around `setVmPolicy` and `setThreadPolicy` that only logs, and covers main-thread disk and
network access plus leaked SQLite cursors and unclosed resources.

- `ThreadPolicy` applies to one thread; `VmPolicy` applies to all threads in the process.
- `noteSlowCall(name)` does nothing unless the thread policy enabled `detectCustomSlowCalls()`.
- `allowThreadDiskReads()` and `allowThreadDiskWrites()` loosen the current thread policy and
  return the old policy, so restore it at the end of the block; use them around a known,
  accepted access rather than disabling the policy.
- `penaltyListener` on the policy builders delivers violations to an
  `OnThreadViolationListener` or `OnVmViolationListener` on your executor.

## Limits
- Do not try to fix everything it reports: much disk access is normal during the activity
  lifecycle. Use it to find accidental access. Network requests on the UI thread are almost
  always a problem.
- It is not a security mechanism and is not guaranteed to find all access; it is best effort,
  and disk or network access from JNI calls may not trigger it.
- The thread policy propagates across Binder calls, so violations by a system service on your
  behalf can be caught.

## Checked
Confirmed in the StrictMode API reference page: purpose, example, `detectAll`, `penaltyLog`,
`enableDefaults`, policy scopes, `noteSlowCall`, `allowThreadDisk*`, listeners, and the
limitations. Removed as not on the cited pages: individual `detect*` method names other than
`detectAll` and `detectCustomSlowCalls`, `penaltyDeath`, the logcat tag and violation text,
`DiskReadViolation`, the API level for `penaltyListener`, and the SharedPreferences/DataStore
advice.
Method: docs-only read of cited pages, 2026-11-08
