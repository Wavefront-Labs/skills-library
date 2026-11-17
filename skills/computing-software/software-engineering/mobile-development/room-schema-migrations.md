---
id: computing-software.software-engineering.mobile-development.room-schema-migrations
name: room-schema-migrations
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, room, room-migrations, sqlite, schema-export, automigration, database-versioning]
level: practitioner
status: docs-checked
description: "Migrate Room databases safely: exported schemas, AutoMigration and specs, manual Migration objects, MigrationTestHelper tests and why destructive fallback deletes user data."
sources: ["https://developer.android.com/training/data-storage/room/migrating-db-versions", "https://developer.android.com/training/data-storage/room/testing-db"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Room schema migrations

The code below follows the current Android migration page, which uses the Room 3 artifacts
(`androidx.room3`). Older Room 2 projects use different package names and a
`SupportSQLiteDatabase`-based `migrate`; check the page for your Room version.

## Export schemas
Room exports the schema to JSON files at compile time; these files are the schema history.
Store them in version control so lower versions can be recreated for tests and automated
migration generation.
```kotlin
// With the Room Gradle Plugin
plugins { id("androidx.room3") }
room3 { schemaDirectory("$projectDir/schemas") }
```
Without the plugin, set the `room.schemaLocation` annotation processor option; the page passes it
through a Gradle `CommandLineArgumentProvider` so Gradle knows about the directory (for KAPT/javac
the value is `-Aroom.schemaLocation=...`). With flavors or build types that change the schema,
repeat `schemaDirectory` with a variant match name as first argument.

## AutoMigration (simple changes)
```kotlin
@Database(
    version = 2,
    entities = [User::class],
    autoMigrations = [AutoMigration(from = 1, to = 2)]
)
abstract class AppDatabaseV2 : RoomDatabase()
```
Automated migrations need the generated schema for both versions: they fail if `exportSchema`
is `false` or the higher version has not been compiled yet. When Room cannot decide (deleting
or renaming a table or column) it gives a compile-time error and you supply an
`AutoMigrationSpec` annotated with `@DeleteTable`, `@RenameTable`, `@DeleteColumn` or
`@RenameColumn`, then set it in `@AutoMigration(spec = ...)`. A spec can also implement
`onPostMigrate`. In Kotlin, several annotations of the same kind need a container such as
`@RenameTable.Entries`.

## Manual migration (complex changes)
For changes Room cannot infer (for example splitting a table), implement `Migration(start, end)`
and register it with `addMigrations(...)`:
```kotlin
val MIGRATION_2_3 = object : Migration(2, 3) {
    override suspend fun migrate(connection: SQLiteConnection) {
        connection.executeSQL("ALTER TABLE Book ADD COLUMN pub_year INTEGER")
    }
}
```
Use full SQL strings in migrations rather than constants that stand for queries. You can mix
automated and manual migrations across versions; if both exist for the same version, Room uses
the manual one.

## Missing paths and destructive fallback
If Room finds no migration path it throws `IllegalStateException`. `fallbackToDestructiveMigration`
makes Room permanently delete all data in the tables instead, so avoid it where user data
matters. Narrower options: `fallbackToDestructiveMigrationFrom` (only from named versions) and
`fallbackToDestructiveMigrationOnDowngrade`.

## Test migrations
Add the `room3-testing` artifact and export the schema first. `MigrationTestHelper` reads the
exported schema files and is a JUnit4 `TestRule`. Create the old version with
`helper.createDatabase(1)`, insert rows with SQL (DAOs expect the latest schema), then
`helper.runMigrationsAndValidate(2, listOf(MIGRATION_1_2))`; the helper verifies the schema
but you must check the data survived. Also add a test that builds the latest database with all
migrations from the earliest version, so Room validates the schema after every migration runs.

## Checked
Confirmed against the Room migration page (AutoMigration, specs, manual migrations, schema
export, test helper, destructive fallback variants) and the Room test and debug page.
Removed as not stated: the old Room 2 `ksp { arg(...) }` one-liner and `SupportSQLiteDatabase`
example, the NOT NULL DEFAULT metadata rule and the advice never to edit schema JSON.
Method: docs-only read of cited pages, 2026-11-08
