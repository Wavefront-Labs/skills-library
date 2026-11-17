---
id: computing-software.software-engineering.mobile-development.foreground-services-and-background-execution-limits
name: foreground-services-and-background-execution-limits
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, foreground-service, background-execution-limits, foreground-service-types, doze, ios-background-modes, workmanager]
level: advanced
status: docs-checked
description: "Run work when the app is not visible within platform rules: Android foreground service types and start restrictions, Doze and standby buckets, and iOS background modes."
sources: ["https://developer.android.com/develop/background-work/services/fgs", "https://developer.android.com/develop/background-work/services/fgs/service-types", "https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start", "https://developer.android.com/about/versions/oreo/background", "https://developer.android.com/training/monitoring-device-state/doze-standby"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Foreground services and background execution limits

**Goal:** pick the sanctioned mechanism for each kind of background work, so the OS does not kill
it, the store does not reject it, and users are not surprised by battery use.

## Decide the mechanism first
| Work | Android | iOS |
|---|---|---|
| deferrable, must complete (sync, upload) | WorkManager | BGTaskScheduler (BGProcessingTask) |
| user-initiated, long, user aware (navigation, workout, call, media playback) | foreground service of the matching type | background mode (audio, location, VoIP) |
| user-initiated data transfer | WorkManager expedited work | URLSession background session |
| exact time event | AlarmManager | local notification |
| server-triggered | FCM high-priority message -> WorkManager | push + background fetch |

## Android foreground services
- A foreground service shows an ongoing notification and must call `startForeground()` promptly after `startForegroundService()`.
- **Types are mandatory** (targetSdk 34+): declare in the manifest and pass to `startForeground`,
  with the matching permission:
```xml
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_LOCATION" />
<service android:name=".TrackingService" android:foregroundServiceType="location" android:exported="false" />
```
```kotlin
ServiceCompat.startForeground(this, NOTIF_ID, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_LOCATION)
```
  Types: `camera`, `connectedDevice`, `dataSync`, `health`, `location`, `mediaPlayback`,
  `mediaProjection`, `microphone`, `mediaProcessing`, `phoneCall`, `remoteMessaging`, `shortService`, `specialUse`,
  `systemExempted`. For `specialUse`, declare the use case in a manifest `<property>`; it is reviewed in Play Console.
- **Start restrictions** (API 31+): apps cannot start foreground services from the background except
  for listed exemptions (high-priority FCM, exact alarms, user interaction with a notification/widget,
  and others listed on the restrictions page). Otherwise `ForegroundServiceStartNotAllowedException`. Use
  WorkManager expedited work instead.
- `shortService` can run for about 3 minutes; the system then calls `onTimeout()` and the service must stop, or the app gets an ANR. `onTimeout()` does not exist on Android 13 and lower.

## Android background limits
- Background services (non-foreground) are stopped after a window of several minutes once the app leaves the foreground
  (API 26+). Apps cannot register for implicit broadcasts in the manifest, with limited exceptions (API 26+).
- **Doze**: when the device is idle, network, jobs, syncs and alarms are deferred to maintenance windows.
  `setExactAndAllowWhileIdle` for critical alarms.
- `setAndAllowWhileIdle()` and `setExactAndAllowWhileIdle()` cannot fire more than once per nine minutes per app.
- Test Doze: `adb shell dumpsys deviceidle force-idle`.

## iOS
- Apps are suspended shortly after backgrounding. Use the sanctioned mechanism from the table above and check Apple's background-execution documentation for current rules; this skill was not checked against it.

## Verify
- [ ] Each foreground service has a declared type, permission and Play declaration.
- [ ] Background starts tested on API 34+ with the app in background (no exceptions).
- [ ] Behaviour verified under forced Doze (`adb shell dumpsys deviceidle force-idle`).

## Checked
2026-11-01. Confirmed against developer.android.com: foreground service types list and `specialUse` property, `shortService` timeout (about 3 minutes, `onTimeout()` absent on Android 13 and lower), background-start restriction on API 31+ with `ForegroundServiceStartNotAllowedException`, Oreo background-service window and implicit broadcast limit, Doze maintenance windows, `setExactAndAllowWhileIdle` nine-minute limit, `dumpsys deviceidle force-idle`. Removed: five-second startForeground timeout, notification-hiding claim, standby-bucket command, OEM list, and the iOS specifics.
Method: documentation only; no commands were run.
