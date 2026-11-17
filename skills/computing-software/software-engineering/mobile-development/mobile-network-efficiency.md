---
id: computing-software.software-engineering.mobile-development.mobile-network-efficiency
name: mobile-network-efficiency
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-network-efficiency, http-caching, compression, batching, radio-state, low-data-mode, metered-networks, battery]
level: advanced
status: draft
description: "Make mobile apps network-efficient: fewer and smaller requests, HTTP caching, compression, batching for radio power states, prefetch, and honouring metered or Low Data modes."
sources: ["https://developer.android.com/develop/connectivity/network-ops/managing", "https://developer.android.com/develop/connectivity/network-ops/reading-network-state", "https://developer.apple.com/documentation/network/nwpath/isconstrained", "https://developer.apple.com/documentation/foundation/urlsessionconfiguration/allowsexpensivenetworkaccess"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network efficiency on mobile

**Goal:** fast screens on slow networks, low data usage, and less battery drain from the cellular
radio.

## Why mobile networking is different
- Latency dominates: a cellular round trip is often 50-300 ms; ten sequential requests on a screen
  means seconds. Parallelise or combine.
- The **radio power state machine**: after any transfer the cellular radio stays in a high-power
  state for several seconds (tail time). Many small, spread-out requests keep it awake; one batched
  transfer is far cheaper.
- Networks change constantly (Wi-Fi to cellular, tunnels, captive portals); requests fail mid-flight.

## Fewer, smaller requests
- Design screen-shaped endpoints (BFF or GraphQL) to avoid N+1 request waterfalls; use HTTP/2 or
  HTTP/3 multiplexing (OkHttp and URLSession support both).
- Compression: gzip/brotli responses (`Accept-Encoding` is automatic in OkHttp/URLSession); compact
  formats (protobuf) for high-volume APIs.
- Paginate; request only needed fields; serve images at display size in WebP/AVIF.
- Delta sync (`updated_since` cursors, ETags) instead of re-downloading full collections.

## Caching
- Honour HTTP caching: server sends `Cache-Control: max-age`, `ETag`; client caches
  (OkHttp `Cache`, `URLCache`) and revalidates with `If-None-Match` -> 304 with no body.
- Offline-first: render from the local database immediately, refresh in the background
  (stale-while-revalidate).
- Do not disable caches globally to "fix" stale data; fix the server headers.

## Batching and scheduling
- Queue analytics/telemetry and send in batches (every N events or minutes, or when the app
  backgrounds), not per event.
- Defer non-urgent sync to WorkManager / BGTaskScheduler with constraints:
```kotlin
val work = PeriodicWorkRequestBuilder<SyncWorker>(6, TimeUnit.HOURS)
    .setConstraints(Constraints(requiredNetworkType = NetworkType.UNMETERED, requiresCharging = true))
    .build()
```
- Prefer push (FCM/APNs) to trigger fetches over polling. If you must poll, back off when nothing changes.
- Prefetch content likely to be needed (next page, article bodies) when on Wi-Fi and charging.

## Respect user data settings
- Android: `ConnectivityManager.isActiveNetworkMetered`, `NetworkCapabilities.NET_CAPABILITY_NOT_METERED`,
  Data Saver (`getRestrictBackgroundStatus()`) - skip prefetch and lower media quality.
- iOS: Low Data Mode -> `NWPath.isConstrained`; set `URLSessionConfiguration.allowsConstrainedNetworkAccess = false`
  for non-essential traffic, and `allowsExpensiveNetworkAccess` for cellular/hotspot.
- Offer "download on Wi-Fi only" for large media.

## Resilience
- Timeouts per request type; retries with exponential backoff and jitter for idempotent calls only.
- `waitsForConnectivity` (iOS) or WorkManager network constraints instead of failing immediately
  offline.
- Resume large downloads (HTTP Range) and use background transfer sessions.

## Measure
- Android Studio Network Inspector, Charles/Proxyman, Instruments HTTP Traffic; count requests per
  screen and bytes per session.
- Test with network throttling (emulator network profiles, Network Link Conditioner) at 3G-like
  latency and packet loss.
- Field metrics: request latency/error rates by network type in your analytics/APM.

## Verify
- [ ] Each primary screen loads with at most a few parallel requests.
- [ ] Repeat visits get 304s or cache hits (proxy log).
- [ ] Background traffic batched; behaviour checked with Low Data Mode / Data Saver enabled.
