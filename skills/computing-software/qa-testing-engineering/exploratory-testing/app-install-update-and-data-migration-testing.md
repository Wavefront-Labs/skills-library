---
id: computing-software.qa-testing-engineering.exploratory-testing.app-install-update-and-data-migration-testing
name: app-install-update-and-data-migration-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [app-update-testing, mobile-testing, data-migration, upgrade-testing, room-migrations]
level: practitioner
status: docs-checked
description: "Test app update data migration on Android: Room automated and manual migrations, exported schemas, MigrationTestHelper tests and missing-path behaviour."
sources:
  - https://developer.android.com/training/data-storage/room/migrating-db-versions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App update and local database migration testing (Android Room)

**Goal:** users who update keep their data; a schema change must not crash the app or silently wipe the on-device database.

## What the docs say
- When an update changes the schema, user data already in the on-device database must be preserved. Room supports automated migrations (`@AutoMigration(from, to)` in `@Database`) and manual ones (a `Migration(startVersion, endVersion)` class added with `addMigrations`).
- Automated migrations need exported schemas for both versions; if `exportSchema` is false or the higher version has not been compiled yet, they fail. Ambiguous changes (deleting or renaming a table or column) need an `AutoMigrationSpec` with `@DeleteTable`, `@RenameTable`, `@DeleteColumn` or `@RenameColumn`. Complex changes, such as splitting one table into two, need a manual `Migration`.
- If both an automated and a manual migration exist for the same version, Room uses the manual one.
- If Room cannot find a migration path, an `IllegalStateException` occurs. `fallbackToDestructiveMigration()` instead permanently deletes all data in the tables; narrower options are `fallbackToDestructiveMigrationFrom` and `fallbackToDestructiveMigrationOnDowngrade`.

## Tests to run
1. **Schema history is exported and committed.** Room exports schema JSON at compile time; keep the files in version control so lower database versions can be recreated for tests.
2. **Single migration test:** with `MigrationTestHelper` (artifact `room3-testing`; the page notes a JUnit4 `TestRule`), create the old version with `helper.createDatabase(1)`, insert rows with SQL (DAOs expect the latest schema), then `runMigrationsAndValidate(2, listOf(MIGRATION_1_2))`. The helper verifies the schema; you must assert that the data migrated.
3. **All-migrations test:** create the earliest version, build the latest database with every migration added, open it so Room validates the schema, and add your own data checks.
4. **Missing path:** confirm the shipping app does not use destructive fallback by accident, and that a skipped-version upgrade has a path.
5. **Manual exploratory pass:** upgrade a device that holds realistic data from an older build and check lists, drafts and settings are intact.

The page notes the library is moving to a `room3` package namespace (`androidx.room3`); use the artifact and plugin names for the Room version your project is on.

## Verify
Every released schema version has a migration test that checks data, a test covering the whole path from the earliest version, and no unintended destructive fallback.

## Checked
2026-11-09: checked against the Android Migrate your Room database page (read in full). Removed because not confirmed: the ISTQB and Apple sources, Core Data, iOS keychain behaviour, Android auto-backup, forced-update prompts, `adb install -r` and bundletool steps, and the N-3 to N heuristic. The manual exploratory step is advice, not a page claim. Tags `install-testing` and `istqb-mat` trimmed.

Method: documentation only; no commands were run.
