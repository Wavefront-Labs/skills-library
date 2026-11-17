---
id: computing-software.software-engineering.mobile-development.android-in-app-updates
name: android-in-app-updates
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, in-app-updates, play-core, appupdatemanager, flexible-update, immediate-update, forced-update]
level: practitioner
status: docs-checked
description: "Prompt Android users to update with the Play In-App Updates API: flexible versus immediate flows, staleness and priority checks, and update result handling."
sources: ["https://developer.android.com/guide/playcore/in-app-updates", "https://developer.android.com/guide/playcore/in-app-updates/kotlin-java"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# In-app updates (Google Play)

Two flows: **flexible** (downloads in the background, you trigger install when convenient) and **immediate** (full-screen blocking update for critical fixes).

```kotlin
val manager = AppUpdateManagerFactory.create(context)
val launcher = registerForActivityResult(ActivityResultContracts.StartIntentSenderForResult()) { r ->
    if (r.resultCode != RESULT_OK) { /* user declined or failed; do not nag every launch */ }
}

manager.appUpdateInfo.addOnSuccessListener { info ->
    val available = info.updateAvailability() == UpdateAvailability.UPDATE_AVAILABLE
    val stale = (info.clientVersionStalenessDays() ?: 0) >= 3
    if (available && stale && info.isUpdateTypeAllowed(AppUpdateType.FLEXIBLE)) {
        manager.startUpdateFlowForResult(info, launcher, AppUpdateOptions.newBuilder(AppUpdateType.FLEXIBLE).build())
    }
}

// flexible: finish when downloaded
manager.registerListener { state ->
    if (state.installStatus() == InstallStatus.DOWNLOADED) manager.completeUpdate()  // restart UI; ask the user first (snackbar)
}
```
Google Play does not restart the app for a flexible update, so show a notification or snackbar when the state is `DOWNLOADED` and call `completeUpdate()` after confirmation. Called in the foreground it shows a full-screen restart UI; called in the background it installs silently. On every return to the foreground, check `installStatus() == DOWNLOADED` again, otherwise the downloaded update keeps occupying storage.

For critical updates use `AppUpdateType.IMMEDIATE` (Google Play shows progress over your UI and handles install and restart). In `onResume`, if `updateAvailability() == DEVELOPER_TRIGGERED_UPDATE_IN_PROGRESS`, call `startUpdateFlowForResult` again to resume a stalled update.

## Gotchas
- Supported on Android 5.0 (API 21) or higher, on phones, tablets and ChromeOS; not compatible with apps that use APK expansion (.obb) files.
- Dependencies: `com.google.android.play:app-update` plus `app-update-ktx` for Kotlin (version 2.1.0 in the current guide; recheck).
- Priority: `updatePriority()` returns an integer 0 to 5 (default 0) set per release with `inAppUpdatePriority` in the Play Developer API (`Edits.tracks`); it can only be set when rolling out the release. It covers every version code between the installed and latest version, across tracks. Typical strategy: low priority update only when idle, medium flexible, high (for example 4 and above) immediate.
- Always call `isUpdateTypeAllowed(type)` before starting; each `AppUpdateInfo` can start an update only once, so after a failure request a fresh one and recheck.
- Result codes: `RESULT_OK` (accepted; may not arrive for immediate updates), `RESULT_CANCELED` (declined), `ActivityResult.RESULT_IN_APP_UPDATE_FAILED` (other error). If the user declines, let them continue and prompt later, unless the app cannot work without the update.
- Request updates only for changes important to core functionality, to avoid tiring users.

Verify: the older build detects the update (`UPDATE_AVAILABLE`), the update flow starts, a flexible update reaches `DOWNLOADED` and `completeUpdate()` installs it, and the new `versionCode` is present afterwards. See the Play guide on testing in-app updates (not covered by this skill's checked sources).

## Checked
Date: 2026-11-08. Confirmed against the Android Developers In-app updates overview and the Kotlin/Java guide: flows, API 21 and device types, .obb incompatibility, app-update 2.1.0 artifacts, staleness and priority APIs (0 to 5, inAppUpdatePriority), result codes, flexible install and completeUpdate behaviour, immediate resume check. Removed the unsupported Play-install-only, emulator, low-storage, staged-rollout and internal-app-sharing claims.
Method: documentation only; no commands were run.
