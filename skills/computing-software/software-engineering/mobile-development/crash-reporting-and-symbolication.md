---
id: computing-software.software-engineering.mobile-development.crash-reporting-and-symbolication
name: crash-reporting-and-symbolication
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-platform-services, crash-reporting, symbolication, dsym, crashlytics, anr, mapping-file]
level: practitioner
status: docs-checked
description: "Set up mobile crash reporting that produces readable stacks: Crashlytics/Sentry setup, iOS dSYM uploads with sentry-cli, ANR causes and diagnosis, and triaging crashes."
sources:
  - https://firebase.google.com/docs/crashlytics/get-started
  - https://developer.android.com/topic/performance/vitals/anr
  - https://docs.sentry.io/platforms/apple/guides/ios/dsym/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crash reporting and symbolication

**Goal:** every production crash and ANR is captured with a symbolicated, deobfuscated stack trace and enough context to fix it, with stability tracked per release.

## 1. Pick and integrate a reporter
Firebase Crashlytics and Sentry are the two reporters covered by the sources here. Crashlytics has separate get-started guides for Apple platforms, Android, Flutter, Unity and Android NDK; each walks you through setup and forcing a test crash to check it. Initialise the reporter as early as you can in app startup, and avoid running two SDKs that both want to own crash handling (design advice; the sources do not cover it).

## 2. iOS symbolication (Sentry)
Sentry requires dSYMs (debug information files) to symbolicate stack traces; symbolication reveals the function, file name and line number of a crash.
- Every upload route needs a Sentry auth token (created on the Organization Tokens settings page). Uploaded dSYMs appear under the project's Settings > Debug Files.
- Three upload routes: `sentry-cli`, the Sentry Fastlane plugin, or an Xcode build phase Run Script.
- `sentry-cli debug-files upload --auth-token <token> --org <org-slug> --project <project-slug> <path-to-dsyms>` scans folders or ZIP archives recursively and skips files already uploaded. `--include-sources` also uploads source for source context.
- Source context needs the build setting `DEBUG_INFORMATION_FORMAT` set to "DWARF with dSYM File", which is the default for release builds but not for debug builds.
- Fastlane: `sentry_debug_files_upload` (`auth_token`, `org_slug`, `project_slug`, optional `include_sources: true`). Plugin 2.0.0 removed `sentry_upload_dsym` and `sentry_upload_dif` in favour of `sentry_debug_files_upload`.
- Xcode build phase: add `${DWARF_DSYM_FOLDER_PATH}/${DWARF_DSYM_FILE_NAME}/Contents/Resources/DWARF/${EXECUTABLE_NAME}` to the Run Script's Input Files and set `ENABLE_USER_SCRIPT_SANDBOXING` to `NO`. The script can emit warnings (build passes) or errors (build fails); for CI deployments Sentry suggests failing the build when symbols may be hard to recover.
- Self-hosted Sentry: export `SENTRY_URL` for sentry-cli, or pass `url:` to the Fastlane plugin.

## 3. Android ANRs
An ANR (Application Not Responding) triggers when the UI thread is blocked too long. Documented triggers:
- Input dispatching timed out: no response to an input event within 5 seconds.
- A service cannot finish `Service.onCreate` and `onStartCommand`/`onBind` within a few seconds.
- `Context.startForegroundService` used but the service does not call `startForeground` within 5 seconds.
- A `BroadcastReceiver` does not finish in time; 10 seconds if the app has a foreground activity.
- A `JobService` does not return from `onStartJob`/`onStopJob` within a few seconds. For apps targeting Android 14 and higher these ANRs are reported to the app; for Android 13 and lower they are silent.

Common causes listed: slow I/O on the main thread, long calculations on the main thread, synchronous binder calls to a slow process, waiting on a synchronized block held by a long operation on another thread, and deadlocks.

Diagnosis tools named by the guide: `ApplicationExitInfo` (Android 11, API level 30 or higher; reports exit reasons including ANRs, low memory, crashes and excessive CPU usage), `StrictMode` during development, `HealthStats`, `Debug`, and trace files. ANR traces are in `/data/anr` on the device (older releases: a single `traces.txt`; newer: multiple `anr_*` files), pulled with `adb root`, `adb shell ls /data/anr`, `adb pull /data/anr/<filename>`; a bug report via `adb bugreport` also works. Background ANR dialogs only show if "Show all ANRs" is enabled in Developer options.

Fixes: move I/O off the main thread (for example `withContext(Dispatchers.IO)` in a ViewModel, or a repository in the data layer); keep `onReceive` short and defer longer work to a ViewModel (a few seconds at most) or WorkManager (longer); use coroutine `Mutex.withLock` instead of blocking locks in Kotlin.

## 4. Context and triage
- Attach custom keys, breadcrumbs and a pseudonymous user ID; never PII or tokens.
- Report non-fatal errors (caught exceptions that indicate bugs) separately from crashes.
- Sort by users affected and trend; group duplicates; link issues to tickets. Fix the symbol-upload step first when crash groups split into many unsymbolicated issues.
- Disclose crash data collection in privacy labels and data-safety forms.

## Verify
- A deliberate test crash in a release-configured build appears symbolicated with file and line in the dashboard, on both platforms.

## Checked
Date: 2026-11-08. Confirmed against the Sentry iOS debug symbols page (upload routes, sentry-cli command and options, DEBUG_INFORMATION_FORMAT, Fastlane action names, Xcode Run Script settings, SENTRY_URL), the Android ANR guide (triggers, timeouts, causes, ApplicationExitInfo, StrictMode, /data/anr, fixes) and the Crashlytics get-started hub (platform guides, test crash). Removed unconfirmed material: Apple's debugging-information page (unreadable), Crashlytics run script paths, upload-symbols, mapping-file and NDK settings, retrace, ndk-stack, atos and dwarfdump usage, the 0.47% ANR threshold, MetricKit and watchdog codes, and the Bitcode note.
Method: documentation only; no commands were run.
