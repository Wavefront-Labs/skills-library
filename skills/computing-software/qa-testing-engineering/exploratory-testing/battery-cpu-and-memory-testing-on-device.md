---
id: computing-software.qa-testing-engineering.exploratory-testing.battery-cpu-and-memory-testing-on-device
name: battery-cpu-and-memory-testing-on-device
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [battery-testing, cpu-usage, memory-usage, mobile-performance, android-profiler]
level: practitioner
status: docs-checked
description: "Profile Android app performance in Android Studio: profileable versus debuggable builds, starting profiler tasks, recordings and comparing scenarios."
sources:
  - https://developer.android.com/studio/profile
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiling CPU, memory and power on Android

**Goal:** find resource drains, leaks and hot loops before users do, using the same scenarios on each release.

## Build choice
- A **profileable** app is based on the release build variant with the `profileable` manifest configuration (`<profileable android:shell="true" />`, true by default); it supports most profiling tasks without the debug build's overhead. In Android Studio use Profile 'app' with low overhead.
- Use a **debuggable** app (the debug variant, with performance cost) to record Java/Kotlin allocations, capture a heap dump, or see the Interaction timeline of user interaction and lifecycle events (API 26 or higher). Use Profile 'app' with complete data.
- Requirements stated: test device or virtual device on API level 29 or higher with Google Play, and Android Gradle Plugin 7.3 or higher.

## Running a profiling task
1. Select the app process on the Profiler Home tab (usually the top process).
2. Choose a task from Tasks; not every task is available for every process.
3. Choose whether to start from startup (needed for startup time) or attach to the running process.
4. Start, interact with the app to trigger the scenario, stop the recording, and wait for parsing.
5. Recordings are saved in Past Recordings for the Studio session; export to keep them, import to reopen. Compare recordings across scenarios.
6. Recording settings: sample interval (shorter fills the file size limit sooner) and file size limit; on API 26 or higher devices the limit is ignored but large traces are still hard to parse.

## Scenarios (test design, not from the page)
- Run the same scripted flow on the same device and charge level for the previous and new release, then compare recordings.
- Repeat a screen open and close many times and check memory plateaus rather than climbs.
- Idle in the background and confirm resource use stays near zero unless a feature justifies it.

## Verify
A release comparison shows CPU and memory for the standard scenarios within an agreed tolerance of the previous release, recorded with the same build type.

## Checked
2026-11-09: checked against the Android Profile your app performance page (read in full). The page does not cover power or the individual task pages, so battery coverage is limited to the general statement that profiling covers CPU, memory, graphics and battery. Removed because not confirmed: Battery Historian and `dumpsys batterystats`, `dumpsys meminfo`, LeakCanary, Doze `deviceidle` commands, all iOS content (Xcode, Instruments, MetricKit) and the Apple and ISTQB sources, and the 30-minute, one-hour and 50-repeat figures. Tag `xcode-instruments` trimmed.

Method: documentation only; no commands were run.
