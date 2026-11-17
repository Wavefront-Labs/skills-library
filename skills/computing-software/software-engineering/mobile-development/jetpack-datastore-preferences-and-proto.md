---
id: computing-software.software-engineering.mobile-development.jetpack-datastore-preferences-and-proto
name: jetpack-datastore-preferences-and-proto
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, datastore, preferences-datastore, proto-datastore, sharedpreferences-migration, kotlin-flow]
level: practitioner
status: docs-checked
description: "Replace SharedPreferences with Jetpack DataStore: Preferences versus typed DataStore, reading as Flow, transactional edit, SharedPreferences migration, single-instance rule."
sources: ["https://developer.android.com/topic/libraries/architecture/datastore", "https://developer.android.com/codelabs/android-preferences-datastore"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jetpack DataStore

DataStore stores key-value pairs (Preferences DataStore) or typed objects (via a `Serializer`,
for example protocol buffers or JSON) using Kotlin coroutines and Flow, asynchronously,
consistently and transactionally. The codelab explains why to leave `SharedPreferences`: its
synchronous API looks safe on the UI thread but does disk I/O, `apply()` can block the UI thread
on `fsync()` and become a source of ANRs, it has no error signalling and no transactional API.

## Preferences DataStore
```kotlin
// top level of a Kotlin file, once
val Context.settings: DataStore<Preferences> by preferencesDataStore(
    name = "settings",
    produceMigrations = { ctx -> listOf(SharedPreferencesMigration(ctx, "legacy_prefs")) }
)
private val DARK = booleanPreferencesKey("dark_mode")

val darkMode: Flow<Boolean> = context.settings.data
    .catch { if (it is IOException) emit(emptyPreferences()) else throw it }
    .map { it[DARK] ?: false }

suspend fun setDark(v: Boolean) = context.settings.edit { it[DARK] = v }
```
- Reading throws `IOException` when the file read fails: catch it before `map` and emit
  `emptyPreferences()`, rethrowing other exceptions. `edit` can also throw `IOException`.
- `edit` transforms the state transactionally. `updateData` (typed DataStore) runs its block as
  one atomic read-modify-write transaction.
- Migrations run before any data access: they must succeed before `data` emits or `edit`
  updates. Pass `SharedPreferencesMigration` in `produceMigrations`.
- Preferences DataStore needs no predefined schema and gives no type safety.

## Typed DataStore (Proto or JSON)
Define the data schema and a `Serializer<T>` with a default value used when no file exists
yet, then create it with the `dataStore(fileName, serializer)` property delegate at the top
level of a file. The type `T` must be immutable; mutating it breaks DataStore's consistency.

## Gotchas
- Never create more than one `DataStore` instance for a file in the same process: DataStore
  throws `IllegalStateException` on read or update. A top-level property delegate keeps one
  instance.
- DataStore suits small datasets; for large or complex data, partial updates or referential
  integrity use Room.
- Corrupt-file recovery: pass a `corruptionHandler` such as `ReplaceFileCorruptionHandler`.

## Checked
Confirmed in the DataStore guide and the Preferences DataStore codelab: API shape, IOException
handling, `edit`/`updateData` transactions, migrations ordering, single-instance rule,
immutability, Room guidance and `corruptionHandler`. Removed as not stated: "each write rewrites
the file", that `runBlocking` reads risk ANRs, and that the migration deletes the old file's keys.
Method: docs-only read of cited pages, 2026-11-08
