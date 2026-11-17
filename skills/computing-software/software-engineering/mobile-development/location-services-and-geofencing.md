---
id: computing-software.software-engineering.mobile-development.location-services-and-geofencing
name: location-services-and-geofencing
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, location-services, geofencing, fused-location-provider, core-location, background-location, location-permissions, battery]
level: practitioner
status: draft
description: "Use device location responsibly: Fused Location Provider and Core Location, permission tiers and approximate location, background updates, geofences and battery trade-offs."
sources: ["https://developer.android.com/develop/sensors-and-location/location", "https://developer.android.com/develop/sensors-and-location/location/geofencing", "https://developer.apple.com/documentation/corelocation", "https://developer.apple.com/documentation/corelocation/monitoring-the-user-s-proximity-to-geographic-regions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Location services and geofencing

**Goal:** get location at the accuracy and frequency the feature needs, with the least permission
and battery cost, and pass store review for background location.

## Permission tiers
| | Android | iOS |
|---|---|---|
| approximate | `ACCESS_COARSE_LOCATION` (user can choose it, API 31+) | Precise Location toggle off (`accuracyAuthorization == .reducedAccuracy`) |
| precise, in use | `ACCESS_FINE_LOCATION` | When In Use |
| background | `ACCESS_BACKGROUND_LOCATION`, requested **separately after** foreground grant (API 30+ sends the user to Settings) | Always (provisional flow: request When In Use first, then Always) |
- Request in context ("Show stores near me"), explain value first; handle denial gracefully (manual
  postcode entry).
- Background location requires Play Console declaration with a video and justification; App Review
  scrutinises "Always" usage and the `NSLocationAlwaysAndWhenInUseUsageDescription` text. Many features
  (geofence reminders) can use system geofencing or significant-change APIs instead.
- iOS Info.plist strings: `NSLocationWhenInUseUsageDescription` (required) and the Always key if used.

## Android: Fused Location Provider
```kotlin
val client = LocationServices.getFusedLocationProviderClient(context)
val last = client.lastLocation.await()                    // may be null or stale
val current = client.getCurrentLocation(Priority.PRIORITY_BALANCED_POWER_ACCURACY, cts.token).await()

val request = LocationRequest.Builder(Priority.PRIORITY_HIGH_ACCURACY, 10_000L)
    .setMinUpdateDistanceMeters(20f)
    .setMinUpdateIntervalMillis(5_000L)
    .build()
client.requestLocationUpdates(request, callback, Looper.getMainLooper())
// stop in onStop / when the feature ends: client.removeLocationUpdates(callback)
```
- Priorities: HIGH_ACCURACY (GPS, battery heavy), BALANCED (~100 m, Wi-Fi/cell), LOW_POWER (~10 km),
  PASSIVE (piggyback on others' requests).
- Continuous tracking while backgrounded needs a foreground service of type `location`.
- Check settings with `SettingsClient.checkLocationSettings` and prompt to enable location services.

## iOS: Core Location
```swift
let manager = CLLocationManager()
manager.requestWhenInUseAuthorization()
// iOS 17+: async updates
for try await update in CLLocationUpdate.liveUpdates(.default) {
    if let loc = update.location { handle(loc) }
}
```
- Classic delegate API: `desiredAccuracy` (`kCLLocationAccuracyHundredMeters` etc.), `distanceFilter`,
  `startUpdatingLocation()`; `requestLocation()` for a single fix.
- Background: enable the Location updates background mode, `allowsBackgroundLocationUpdates = true`,
  and on iOS 17+ use `CLBackgroundActivitySession` to keep receiving updates.
- **Significant-location-change** and **visits** monitoring are very low power and relaunch the app
  when terminated - good for "where has the user been" features.

## Geofencing
- Android: `GeofencingClient.addGeofences` with up to 100 geofences per app (per device user); transitions
  ENTER/EXIT/DWELL delivered to a `BroadcastReceiver` via PendingIntent (mutable flag required for
  geofence PendingIntents). Needs background location for triggers while the app is not visible.
  Re-register after a reboot or when Google Play services is killed and restarted (geofences are cleared). Minimum radius 100-150 m recommended; use DWELL to cut alert spam.
- iOS: `CLMonitor` (iOS 17) or legacy region monitoring (`startMonitoring(for: CLCircularRegion)`),
  max 20 regions per app; register the nearest 20 and rotate as the user moves. Wakes or relaunches
  the app on crossing; requires Always authorisation.
- Android alerts are usually under 2 minutes late, 2-3 minutes under Background Location Limits, and up to 6 minutes
  when the device is stationary; Wi-Fi accuracy is about 50 m. Geofences are not suitable for precise triggers.

## Battery and privacy
- Use the lowest accuracy and frequency that work; stop updates when not needed.
- Batch background updates (`setMaxUpdateDelayMillis` on Android).
- Disclose collection in privacy labels / Data safety; avoid storing raw location history unless the
  feature needs it, and offer deletion.

## Verify
- [ ] Feature works with approximate location and handles denial.
- [ ] Location updates stop when the screen/feature is gone (battery profiler).
- [ ] Geofences re-registered after reboot (Android) and tested with mock locations / GPX routes.
