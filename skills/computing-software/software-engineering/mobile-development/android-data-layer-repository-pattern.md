---
id: computing-software.software-engineering.mobile-development.android-data-layer-repository-pattern
name: android-data-layer-repository-pattern
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, repository-pattern, data-layer, single-source-of-truth, data-sources, room, retrofit, architecture]
level: practitioner
status: docs-checked
description: "Structure the Android data layer: repositories as the public API, local and remote data sources, a single source of truth, mapping DTOs to models and error handling."
sources: ["https://developer.android.com/topic/architecture/data-layer", "https://developer.android.com/topic/architecture/data-layer/offline-first"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data layer and the repository pattern

The data layer exposes application data through repositories; each repository hides data sources (network, database, files) behind one API and is the **single source of truth** for its data type.

```kotlin
interface ArticleRepository {
    fun observeArticles(): Flow<List<Article>>        // reads come from the database
    suspend fun refresh(): Result<Unit>               // writes go network -> database
}

class OfflineFirstArticleRepository(
    private val dao: ArticleDao,
    private val api: ArticleApi,
    private val io: CoroutineDispatcher = Dispatchers.IO
) : ArticleRepository {

    override fun observeArticles() = dao.observeAll().map { rows -> rows.map(ArticleEntity::toModel) }

    override suspend fun refresh(): Result<Unit> = withContext(io) {
        try {
            val remote = api.getArticles()                    // DTOs
            dao.upsertAll(remote.map(ArticleDto::toEntity))   // DB is the source of truth
            Result.success(Unit)
        } catch (e: IOException) {                            // only expected failures; cancellation propagates
            Result.failure(e)
        }
    }
}
```

## Rules of thumb
- One repository per type of data (articles, users), not per screen; name it type of data + `Repository`. Other layers never touch data sources directly; the repository is the entry point and takes its data sources as constructor dependencies.
- Each data source works with only one source (file, network or database); name it after the data and the source (`NewsRemoteDataSource`), not an implementation detail such as SharedPreferences.
- Expose only what other layers need: separate model classes for network data and app data (DTO -> entity -> model) so an API shape change does not reach the UI.
- Expose `Flow` for data that changes over time and `suspend` functions for one-shot operations; repositories and data sources must be main-safe.
- Resolve conflicts between sources in the repository; the data it exposes always comes straight from the source of truth. For offline-first support, a local data source such as a database is the recommended source of truth.
- Offline writes: write to the local source first, then queue the write and drain the queue as persistent work with WorkManager (see the offline-first guide for conflict strategies such as last write wins).
- Operations that must survive process death (for example finishing a photo upload) are business-oriented: use WorkManager. Work that should outlive a screen belongs in a scope owned by the repository, not the caller's scope.

## Gotchas
- Handle failures with Kotlin's error handling (`try`/`catch` in suspend functions, the `catch` operator in flows). The data layer may expose custom exceptions such as `UserNotAuthenticatedException`, or a `Result<T>` type.
- A repository that exposes both DB and network `Flow`s defeats the single-source-of-truth idea.

Verify: unit test with an in-memory Room database and a fake API; after `refresh()` the `observeArticles()` flow emits the new data, and with the fake API failing it still emits cached data.

## Checked
Date: 2026-11-08. Confirmed against the Android Developers Data layer guide (repository tasks, data source rules and naming, source of truth, main-safe threading, models, business-oriented operations with WorkManager, error handling, in-memory Room testing) and the offline-first guide (local source of truth, mappers, write queues drained with WorkManager, last write wins). Removed the unsupported "mark rows pending" step and the runCatching claim (code now uses try/catch).
Method: documentation only; no commands were run.
