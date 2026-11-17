---
id: computing-software.qa-testing-engineering.exploratory-testing.mobile-log-collection-adb-xcode
name: mobile-log-collection-adb-xcode
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [adb-logcat, mobile-logs, bug-investigation, android]
level: practitioner
status: docs-checked
description: "Collect Android logs for bug investigation: adb logcat filters, formats and buffers, and adb bugreport contents."
sources:
  - https://developer.android.com/tools/logcat
  - https://developer.android.com/studio/debug/bug-report
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collecting Android logs (logcat, bug reports)

**Goal:** attach the device-side evidence developers need to every mobile bug.

## logcat
Logcat dumps system messages including those an app writes with the Log class. The Android logging system is a set of circular buffers kept by logd. Run `[adb] shell logcat [<option>] [<filter-spec>]`; `adb logcat` is shorthand for `adb shell logcat`. Available options depend on the device OS version; `adb logcat --help` lists them, and many are root only.

- **Filter by tag and priority** with `tag:priority`, whitespace separated; priorities in order are V, D, I, W, E, F, S.
  - `adb logcat ActivityManager:I MyApp:D *:S` shows only those tags (`*:S` silences the rest, making the filters an allowlist).
  - `adb logcat *:W` shows warning and above for all tags.
  - Quote the expression if your shell treats `*` specially.
- **Format** with `-v`: brief, long, process, raw, tag, thread, threadtime (default), time. Modifiers include color, epoch, monotonic, uid, usec, UTC, year, zone, for example `adb logcat -b all -v color -d`.
- **Buffers** with `-b`: main (default, excludes system and crash), system, crash, radio, events, all, default (main, system and crash). Combine with several `-b` flags or one comma list: `logcat -b main,radio,events`.
- Logs pass four filters before you see them: compile-time (for example ProGuard can strip `Log.d`), system property (`log.tag.<TAG>`), application minimum priority (default INFO) and display filters. A missing log line may be filtered before logcat.

## Bug report
A bug report contains device logs, stack traces and other diagnostics. Capture it with Developer options > Take bug report, the Android Emulator extended controls Bug report screen, or `adb bugreport [path]`. With several devices connected, pick one with `adb -s <serial> bugreport`.
- The zip is named `bugreport-BUILD_ID-DATE.zip`; the main file `bugreport-BUILD_ID-DATE.txt` holds dumpsys output, dumpstate error logs and system message logs including stack traces. It also holds `version.txt` and the `FS` folder with copied device files.
- Older reports are in `/bugreports` on the device: `adb shell ls /bugreports/` then `adb pull`.
- For real users, the page points to Google Play Console crash and ANR data (previous six months) and Firebase Crashlytics.

## Attach well
Note the device model, OS version, app version and build, and the reproduction time so log lines can be matched; trim to the relevant minute and attach the full file too.

## Verify
Each mobile bug report includes logs covering the reproduction time with the app's errors or crash trace visible, plus device, OS and build details.

## Checked
2026-11-09: checked against the Android logcat page and the Capture and read bug reports page, both read in full. iOS coverage dropped: the Apple logging page returned a stub, so the Console.app, Xcode device log, sysdiagnose and `xcrun simctl` bullets were removed. Also removed because the pages do not state them: `adb logcat -c`, `--pid` and `pidof` usage, `FATAL EXCEPTION` and `ANR in` search strings, `dumpsys activity` and `dumpsys meminfo` commands, and the Android Studio filter syntax. Tags `xcode-console` and `ios` trimmed. The name keeps xcode for id stability.

Method: documentation only; no commands were run.
