---
id: computing-software.qa-testing-engineering.exploratory-testing.mobile-permission-and-lifecycle-testing
name: mobile-permission-and-lifecycle-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [app-permissions-testing, mobile-testing, runtime-permissions, app-lifecycle, process-death]
level: practitioner
status: docs-checked
description: "Test Android runtime permissions (grant, deny, deny twice, one-time, revoke) and UI-state survival across rotation, process death and user dismissal."
sources:
  - https://developer.android.com/training/permissions/requesting
  - https://developer.android.com/topic/libraries/architecture/saving-states
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Permission and lifecycle testing (Android)

**Goal:** the app handles every permission state and lifecycle transition without crashing or losing data.

## Permissions
For each permission-gated feature:
- Grant on the prompt; deny; deny twice. The page says that if the user taps Deny for a permission more than once the system dialog no longer appears when the app requests it again, and this is treated as permanent denial.
- Rationale: when `ContextCompat.checkSelfPermission()` returns `PERMISSION_DENIED`, the app calls `shouldShowRequestPermissionRationale()`; if true it shows an educational UI before requesting.
- Android 11 and later: for location, microphone and camera the dialog has **Only this time**, granting a temporary one-time permission. If the user revokes it (for example in system settings) the app process terminates and the user is prompted again at the next request.
- Permissions can be denied or granted automatically, so each feature must re-check the permission before use.
- On Android 11+ targets, permissions of apps unused for a few months are reset automatically. On Android 13+ an app can drop permissions with `revokeSelfPermissionOnKill()`.
- Expected on denial (page guidance): minimal loss of functionality, a specific message where the feature's data would appear, no blocking full-screen warning, no persistent nagging.

Inspect and reset state:
- `adb shell dumpsys package PACKAGE_NAME`: under `runtime permissions`, `USER_SET` marks a permission denied once and `USER_FIXED` marks denied permanently.
- `adb shell pm clear-permission-flags PACKAGE_NAME PERMISSION_NAME user-set user-fixed` resets the flags so testers see the dialog again.
- `adb shell install -g PATH_TO_APK_FILE` grants all runtime permissions at install on an emulator or test device.

## Lifecycle and UI state
- Users expect a clean state after swiping the app off Recents, force-quitting from Settings, rebooting, or finishing the activity.
- Users expect state kept across configuration changes such as rotation or multi-window. By default the system destroys the host activity on those, wiping UI state stored in it.
- The system may destroy the app process while it is in the background; on return the screen is clean unless state was saved. Per the page: a ViewModel survives configuration change but not system-initiated process death; saved state (`SavedStateHandle`, `rememberSaveable`) survives both.
- Test: change state mid-task, rotate, background the app long enough for the system to kill it, return, and check the state is restored. Saved state is for small transient UI state; larger data must come from local storage.

## Verify
A permission matrix (feature by state) and a lifecycle checklist executed on the minimum and latest supported OS versions.

## Checked
2026-11-09: checked against the Android Request runtime permissions page (read denial, one-time, reset and testing sections) and the Save UI states page (read the dismissal, ViewModel and saved-state sections; the code samples were not checked). Removed because not confirmed: all iOS content and the Apple source (not fetched), `adb shell pm grant|revoke|reset-permissions`, `adb shell am kill` and `am force-stop`, the `POST_NOTIFICATIONS` Android 13 claim, the approximate-versus-precise location and limited photo library cases, and the upgrade, fresh-install and cold-start items. Tag `istqb-mobile` trimmed.

Method: documentation only; no commands were run.
