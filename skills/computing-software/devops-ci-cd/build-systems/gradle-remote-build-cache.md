---
id: computing-software.devops-ci-cd.build-systems.gradle-remote-build-cache
name: gradle-remote-build-cache
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [gradle, build-systems, gradle-remote-cache, gradle-build-cache, build-cache-node, develocity, httpbuildcache, cacheable-tasks, relocatability, path-sensitivity, build-scan, cache-misses]
level: advanced
status: docs-checked
description: "Share Gradle task outputs across CI and laptops with a remote build cache: Develocity cache node or HTTP cache, push only from CI, making tasks cacheable and relocatable, and finding misses."
sources: ["https://docs.gradle.org/current/userguide/build_cache.html", "https://docs.gradle.org/current/userguide/build_cache_concepts.html", "https://docs.gradle.org/current/userguide/build_cache_debugging.html", "https://docs.gradle.org/current/userguide/common_caching_problems.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle remote build cache

## Enable
```properties
# gradle.properties
org.gradle.caching=true
```
```kotlin
// settings.gradle.kts
val isCi = System.getenv("CI") != null
buildCache {
    local { isEnabled = !isCi }                      // ephemeral CI agents gain nothing locally
    remote<HttpBuildCache> {
        url = uri("https://gradle-cache.example.com/cache/")
        isPush = isCi                                // only CI writes; laptops read
        credentials {
            username = System.getenv("GRADLE_CACHE_USER")
            password = System.getenv("GRADLE_CACHE_PASSWORD")
        }
        isAllowInsecureProtocol = false
    }
}
```
The local cache is enabled by default and stores in the Gradle user home; a build cache stores outputs only when it is enabled and `isPush` is true. With Develocity: the `com.gradle.develocity` plugin and
`buildCache { remote(develocity.buildCache) { isPush = isCi } }`.

## Backends
- **Develocity Build Cache Node** (Docker image `gradle/build-cache-node`): can be used without a Develocity installation with restricted functionality, or connected to Develocity for central management.
- Any HTTP server that supports GET and PUT via `HttpBuildCache`, or a custom `BuildCacheService` implementation.

## Making tasks cacheable
- Task types opt in with `@CacheableTask`; declare inputs and outputs, and use `@PathSensitive(PathSensitivity.RELATIVE)` on file inputs so absolute paths do not enter the cache key.
- Declare every real input of a task that produces cached results (for example `inputs.property(...)`, `inputs.files(...)`); undeclared inputs make hits return stale results.
- Tasks with no outputs or no inputs always execute.

## Why misses happen
- Gradle tracks the Java major version for compilation and test execution; with Java toolchains the vendor and implementation are tracked too. Pin via toolchains
  (`java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }`).
- Absolute paths and volatile inputs such as timestamps in generated files.
- Line endings: Git on Windows with `autocrlf=true` converts line endings; set `autocrlf=false` on build machines that share a cache across operating systems (or normalise with `.gitattributes`).
- Diagnose: `./gradlew build --scan` and compare two scans, or `-Dorg.gradle.caching.debug=true` to log the cache key and input property hashes.

## CI pattern
Seed the cache from `main` builds; PR builds read it (`isPush = false`). Untrusted fork PRs must not push.
The configuration cache (`org.gradle.configuration-cache=true`) is a separate feature that speeds up startup.

## Verify
`./gradlew clean build --build-cache` on a fresh checkout prints cacheable tasks as `FROM-CACHE` when they are served from the cache; a second CI run of the same commit should be mostly `FROM-CACHE`.

## Checked
Date: 2026-10-25. Documentation: Gradle user guide pages "Build cache", "Build cache concepts", "Build cache debugging" and "Common caching problems" (gradle/gradle `platforms/documentation/.../build-cache`), and `HttpBuildCache.java`.
Confirmed: `org.gradle.caching=true`; `FROM-CACHE` output; local cache default and Gradle user home storage; `isPush` semantics; `HttpBuildCache` and its `allowInsecureProtocol` and `allowUntrustedServer` properties; build cache node image and its restricted standalone use; `@CacheableTask` opt-in; `-Dorg.gradle.caching.debug=true`; Java major-version and toolchain tracking; `autocrlf` guidance.
Removed: nginx WebDAV, Artifactory and S3-plugin backends, node UI/replication features, the claims that tests and `Exec`/`JavaExec` tasks are or are not cacheable by default, and the "different JDK vendors" cause without toolchains (Gradle tracks only the major version unless toolchains are used).
Method: documentation only; no commands were run.
