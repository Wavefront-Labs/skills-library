---
id: computing-software.software-engineering.mobile-development.app-lifecycle-and-offline-sync
name: app-lifecycle-and-offline-sync
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, android, app-lifecycle, process-death, state-restoration, savedstatehandle, remembersaveable, scenestorage, scenephase, offline-first, local-database, room, sqlite, core-data, swiftdata, sync-queue, outbox, conflict-resolution, last-write-wins, crdt, workmanager, bgtaskscheduler, doze, background-limits, idempotency, software-engineering]
level: advanced
status: draft
description: "Build mobile apps that survive suspension and process death, restore user state, work offline from a local DB with a durable sync queue, resolve conflicts and respect background limits."
sources: ["Android Developers - Activity lifecycle, Saving UI states, and WorkManager guides", "Apple Developer Documentation - Managing your app's life cycle and BackgroundTasks framework", "Android Developers - Build an offline-first app", "Kleppmann et al., Local-first software (Ink & Switch, 2019)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# App lifecycle and offline sync — never lose the user's work

**Goal:** an app that can be suspended or killed at any moment, reopens exactly where the
user left off, works without a network, and converges with the server without
silently losing edits.

## 1. Assume the process will die
Both OSes suspend backgrounded apps and kill them for memory without calling any
"terminate" callback you can rely on.
- **iOS:** states active → inactive → background → suspended. In SwiftUI observe
  `@Environment(\.scenePhase)`; UIKit uses `sceneWillResignActive`/`sceneDidEnterBackground`.
  Persist at `.inactive`/`.background`, not at termination. Extra time to finish a save:
  `UIApplication.beginBackgroundTask` (a few seconds to roughly 30 s; not guaranteed —
  always call `endBackgroundTask`).
- **Android:** `onStop` is your last reliable callback; after it the process can be
  killed. On return the system recreates the Activity stack and expects you to restore.

## 2. Restore UI state
- **Android:** `ViewModel` survives configuration changes but **not** process death. Put
  small, essential UI state in `SavedStateHandle` (ViewModel) or `rememberSaveable`
  (Compose); these go into the saved-instance Bundle. Keep it tiny — ids and scroll
  positions, not lists — as large Bundles throw `TransactionTooLargeException`
  (binder limit ~1 MB shared across the process). Reload real data from the DB by id.
- **iOS:** `@SceneStorage` for per-scene UI state (selected tab, draft id),
  `NSUserActivity` for deeper restoration and Handoff, `@AppStorage`/UserDefaults only for
  small preferences.
- **Test process death deliberately:** Android — background the app, then
  `adb shell am kill <package>` and reopen from Recents (or enable Developer options ›
  "Don't keep activities"). iOS — background the app and stop it from Xcode, then relaunch;
  swiping away in the app switcher deliberately discards restoration state, so it is not
  the same test.

## 3. Offline-first: the local DB is the source of truth for UI
- UI reads only from the local store (Room, SQLDelight, Core Data/SwiftData, GRDB)
  via observable queries; network results go into the DB, never straight to screen.
- User writes go to the DB **and** to an **outbox/sync queue** table in the same
  transaction: `{op_id UUID, entity, entity_id, op_type, payload, base_version, created_at,
  attempts}`.
- Generate ids on the client (UUIDv4/v7) so offline-created records have stable
  identity; send `op_id` as an **idempotency key** so retries after a lost response
  don't duplicate.
- Pull with a server cursor/change token (`GET /changes?since=<token>`); the server must
  return **tombstones** for deletions or deleted rows reappear.

## 4. The sync engine
1. Trigger on connectivity regained, app foreground, push notification, and periodic
   background work.
2. Push the outbox in order per entity; on success delete the row and store the
   server version; on 4xx validation errors mark it failed and surface it to the user;
   on 5xx/timeout retry with exponential backoff and jitter.
3. Then pull changes and merge into the DB.
- **Android:** `WorkManager` with `Constraints(requiredNetworkType = CONNECTED)`,
  `enqueueUniqueWork(..., ExistingWorkPolicy.KEEP/APPEND)` to avoid duplicate syncs;
  `PeriodicWorkRequest` minimum interval is 15 minutes. Doze and App Standby buckets
  defer work further. Android 14+ requires declared foreground-service types; prefer
  user-initiated data transfer jobs for big user-started uploads (check current docs).
- **iOS:** `BGAppRefreshTask` for short refreshes and `BGProcessingTask` for longer work
  (register identifiers in `Info.plist` under `BGTaskSchedulerPermittedIdentifiers`);
  the system decides when, if ever, they run. Use background `URLSession`
  configurations for large uploads/downloads that continue while suspended.

## 5. Conflict resolution — pick a policy per data type
- **Optimistic concurrency:** each record carries `version`/ETag; the push sends
  `base_version`; server rejects mismatches (`409`/`412`) and the client merges.
- **Last-write-wins** (by server receive time, not device clock) is acceptable for
  low-value fields; apply it **per field**, not per record, to avoid clobbering
  unrelated edits.
- **Merge or ask:** three-way merge against the base, or show both versions.
- **CRDTs** (Automerge, Yjs) for collaborative text/lists where concurrent edits must
  always merge without a server arbiter.
- Counters and sets: send operations (`increment by 2`), not final values.

## Gotchas
- Device clocks are wrong; never order events across devices by local timestamp alone.
- Schema migrations must handle a non-empty outbox written by the previous app version.
- Background work is a hint, not a schedule: force-quit (iOS) or "force stop"
  (Android) prevents it entirely until the next launch; low-power modes defer it.
- An outbox op referencing an entity created by an earlier, still-pending op must wait
  for it (dependency ordering), or the server returns 404.
- Tokens expire offline; refresh before draining the queue, pause on 401.

## Verify
- [ ] Killing the process from the background and reopening restores the screen and any draft.
- [ ] Airplane-mode create/edit/delete works, and all changes reach the server once online.
- [ ] Replaying the same outbox op twice produces one server-side change.
- [ ] A deliberate concurrent edit from two devices resolves per the documented policy.
- [ ] Deletions propagate via tombstones and do not reappear after a pull.
- [ ] Sync is scheduled through WorkManager / BGTaskScheduler with network constraints, not a timer.

Related: computing-software.software-engineering.api-design.rest-resource-design-and-versioning
