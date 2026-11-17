---
id: computing-software.devops-ci-cd.gradle.gradle-build-cache-setup
name: gradle-build-cache-setup
category: computing-software
field: devops-ci-cd
product: gradle
tags: [build-cache, remote-cache, cacheable-task, cache-key, path-sensitivity, org-gradle-caching]
level: advanced
status: docs-checked
description: "Enable the Gradle build cache, configure local and HTTP remote caches, mark tasks cacheable and avoid cache misses."
sources: ["https://docs.gradle.org/current/userguide/build_cache.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle build cache setup

Enable with `--build-cache` for one run or `org.gradle.caching=true` in `gradle.properties` (`--no-build-cache` disables). Local entries default to Gradle User Home.

```groovy
buildCache {
    local {
        enabled = true
        push = true
        directory = new File(rootDir, 'build-cache')
    }
    remote(HttpBuildCache) {
        url = 'https://example.com:8123/cache/'
        push = System.getenv().containsKey('CI')   // CI writes, developers read
    }
}
```

Reads go local first, then remote, and remote hits are copied locally. `push` defaults to true for local and false for remote (Kotlin: `isPush`). HTTP: `GET` loads an entry (2xx or 404), `PUT` stores it (2xx success; 413 is not an error). `allowUntrustedServer` is a security risk.

Cacheable tasks: annotate a task type `@CacheableTask` (not inherited by subclasses) or mark it `@DisableCachingByDefault`; for a non-cacheable class use `outputs.cacheIf { true }`. Use `@PathSensitive(PathSensitivity.RELATIVE)` on inputs so entries work across different paths.

The cache key covers the task type and classpath, output property names, input names and values, the Gradle distribution, buildSrc and plugin classpath, and build script content when it affects the task. The task path is not part of the key.

Avoiding misses: missing inputs cause wrong hits, volatile data or absolute paths cause needless misses (use input normalization). A build run twice must be `UP-TO-DATE`; caching cannot fix that. Test cacheability and relocatability with TestKit. Hits appear as `FROM-CACHE`. Gradle periodically removes stale local entries; tune via an init script.

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: nothing.
Method: documentation only; no commands were run.
