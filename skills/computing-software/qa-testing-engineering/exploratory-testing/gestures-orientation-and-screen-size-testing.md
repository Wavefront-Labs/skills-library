---
id: computing-software.qa-testing-engineering.exploratory-testing.gestures-orientation-and-screen-size-testing
name: gestures-orientation-and-screen-size-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [orientation-testing, screen-size-testing, mobile-testing, configuration-changes]
level: practitioner
status: docs-checked
description: "Test Android configuration changes: rotation, multi-window, folding, display size, theme, font and locale changes, and UI state preservation."
sources:
  - https://developer.android.com/guide/topics/resources/runtime-changes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Orientation, screen-size and configuration-change testing (Android)

**Goal:** the app keeps working, keeps the user's state and looks right when the device configuration changes while it runs.

## Why it matters
Configuration changes include display size, screen density, orientation, font size and weight, locale, dark versus light theme and keyboard availability. By default the system recreates the Activity: it calls `onDestroy`, creates a new instance and clears any state kept as Activity fields. The page says there is no way to prevent configuration changes and that it is impossible to entirely disable Activity recreation.

## Actions to run (foreground and background)
The page lists these as ways to verify state is preserved, both while the app is in the foreground and while it is in the background:
- Rotate the device.
- Enter multi-window mode, or resize the app in multi-window or a free-form window.
- Fold a foldable device with multiple displays.
- Change display size or display scaling in system settings.
- Move the app between displays with different pixel densities (external monitor, foldable).
- Change the system theme (dark or light).
- Change the font size.
- Change the system or app language.
- Connect or disconnect a hardware keyboard or a dock.

Use mid-task states: a half-filled form, scroll position, selected tab, open dialog. The page's example of a bad outcome is a user returning to a cleared form after referencing another app in multi-window.

## What to expect
- State survives: the page recommends ViewModel for in-memory UI data, `rememberSaveable` for transient UI state across configuration change and process death, and local persistence (databases, DataStore) for complex or large data.
- Apps that opt out of recreation with `android:configChanges` must handle the change themselves, and embedded views such as `AndroidView` must be updated manually. The page warns against opting out as a quick fix and against restricting orientation, aspect ratio or resizability to avoid changes. On Android 12L (API 32) and higher, an app with such restrictions enters compatibility mode when it does not directly support the current device state; test with restrictions unlocked.
- Android 17 (API 37) no longer restarts activities by default for keyboard, keyboard hidden, navigation, touchscreen, colour mode and some UI mode changes; they arrive via `onConfigurationChanged()` unless the app opts in with `android:recreateOnConfigChanges`. Test on a device or emulator at that level if you target it.
- Size changes are more likely on large screens where users enter multi-window.

## Verify
Each screen passes every configuration action above mid-task, in the foreground and background, without state loss or layout breakage, on the smallest, largest and foldable devices you support.

## Checked
2026-11-09: checked against the Android Handle configuration changes page (read in full). Removed because it does not state them: the whole gestures section (tap, swipe, pinch, 48 dp and 44 pt targets, back-gesture conflicts), iOS safe areas, Dynamic Island, notch coverage, keyboard-over-input in landscape, picture-in-picture, the "Don't keep activities" developer option, and the ISTQB and Apple HIG sources. Tags `gesture-testing` and `istqb-mat` trimmed. The name keeps gestures for id stability.

Method: documentation only; no commands were run.
