---
id: computing-software.qa-testing-engineering.exploratory-testing.mobile-interrupt-testing
name: mobile-interrupt-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [interrupt-testing, mobile-testing, app-lifecycle, backgrounding]
level: practitioner
status: docs-checked
description: "Test Android apps under interruptions (calls, dialogs, app switching, multi-window, process kill) using the activity lifecycle as the expected behaviour."
sources:
  - https://developer.android.com/guide/components/activities/activity-lifecycle
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mobile interrupt testing (Android)

**Goal:** the app behaves correctly when the OS or user interrupts it. The activity lifecycle page names the failures to prevent: crashing when the user receives a phone call or switches apps, consuming resources when not in use, losing progress when the user leaves and returns, and crashing or losing progress on rotation.

## Interruptions to apply (at critical points: mid-form, mid-payment, during upload, during playback)
- Incoming phone call, or anything that takes focus: the Resumed activity stays resumed until something such as a phone call, navigating to another activity or the screen turning off takes focus; it then enters Paused.
- A semi-transparent activity such as a dialog over your screen (the covered activity stays paused while partially visible).
- Multi-window: only one app has focus, so the other app's activity is Paused even while fully visible. Tap the other window and check the app still works and does not hold shared resources such as the camera needlessly.
- Switching away to another app (the activity is Stopped and may be killed), screen off, and returning.
- Rotation, multi-window entry and other configuration changes, which destroy and recreate the activity.
- Killing the app from Settings (Application Manager), which the page says the user can do.

## Expected (from the lifecycle page)
- The activity releases or adjusts resources not needed while invisible in `onStop` (for example pausing animations, coarser location updates); using `onStop` rather than `onPause` keeps UI work running in multi-window.
- Transient UI state survives configuration change and system-initiated process death when saved with ViewModel, `rememberSaveable` or local storage; instance state is only suitable for a trivial amount of data.
- The system never kills an activity directly; it kills the process. Kill likelihood rises from Resumed (lowest) to Started/Paused, to Stopped, to Destroyed (highest), so a long-backgrounded app is the likely candidate for process death.

## Verify
An interrupt checklist executed at each critical point of key journeys, with results per device and OS version, and state checked on return.

## Checked
2026-11-09: checked against the Android activity lifecycle page (overview, onResume, onPause, onStop, onDestroy, process kill table and saving-state sections; the activity navigation and callback-order sections at the end were skimmed only). Removed because not confirmed: all iOS content and the Apple and ISTQB sources, low battery, battery saver, alarms, Siri and notification-shade cases, `adb` commands for simulating calls and key events, the emulator `gsm call` command, the "Don't keep activities" option, duplicate-payment and audio-focus expectations. Tags `notifications` and `istqb-mobile` trimmed.

Method: documentation only; no commands were run.
