---
id: computing-software.devops-ci-cd.build-systems.remote-cache-write-permissions-and-poisoning
name: remote-cache-write-permissions-and-poisoning
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, remote-cache-security, cache-poisoning, bazel-remote-cache, read-only-cache, action-cache, build-integrity]
level: practitioner
status: draft
description: "Secure shared build caches against poisoning: who may write, read-only for PRs and laptops, CI-only writers, cache key hygiene, Bazel, Gradle and Turborepo settings, and auditing."
sources:
  - https://bazel.build/remote/caching
  - https://docs.gradle.org/current/userguide/build_cache.html#sec:build_cache_configure_remote
  - https://turbo.build/repo/docs/core-concepts/remote-caching#artifact-integrity-and-authenticity-verification
  - https://github.com/buchgr/bazel-remote
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Remote cache write permissions and poisoning

A remote build cache maps an action/task key to outputs. Anyone who can write an entry can make every later build download their binary for that key - a supply-chain attack that skips source review. Accidental poisoning (non-hermetic action, wrong platform output) is also common.

## Write policy
| Writer | Allow write? |
|---|---|
| Trusted CI on protected branches (main, release) | yes |
| CI for pull requests from forks | no - read only |
| CI for internal PR branches | ideally read only, or a separate cache namespace |
| Developer laptops | read only |
Implement with separate credentials: a read-only token distributed widely, a write token only in protected CI environments.

## Bazel
```
# .bazelrc
build --remote_cache=grpcs://cache.example.com
build --remote_upload_local_results=false          # default for everyone: read only
build:ci-main --remote_upload_local_results=true   # only main-branch CI uses --config=ci-main
build --incompatible_strict_action_env             # stable PATH etc. in cache keys
build --experimental_remote_cache_eviction_retries=1
```
bazel-remote / BuildBuddy / EngFlow support per-credential read/write (`--htpasswd_file` + separate read-only users, or API keys with roles). With remote execution, only the executor writes action results, which is the strongest model: clients can't upload `ActionResult`s at all (`--remote_upload_local_results` disabled server-side).

## Gradle
```kotlin
// settings.gradle.kts
buildCache {
  remote<HttpBuildCache> {
    url = uri("https://gradle-cache.example.com/cache/")
    isPush = System.getenv("CI") == "true" && System.getenv("GITHUB_REF") == "refs/heads/main"
    credentials { username = providers.environmentVariable("CACHE_USER").orNull; password = providers.environmentVariable("CACHE_PASS").orNull }
  }
}
```

## Turborepo / Nx
- Turborepo: `signature: true` in turbo.json with `TURBO_REMOTE_CACHE_SIGNATURE_KEY` to HMAC-sign artifacts; read-only tokens via `--remote-cache-read-only` / `TURBO_REMOTE_CACHE_READ_ONLY=true` for PRs.
- Nx Cloud: read-only vs read-write access tokens; use read-only in PR pipelines.

## Key hygiene (accidental poisoning)
- Include toolchain version, platform, and relevant env vars in keys; exclude volatile ones (timestamps, absolute paths, build numbers).
- Non-hermetic actions (reading undeclared files, network) produce entries that are wrong for other machines. Detect with execution logs: `bazel build --execution_log_json_file=a.json` twice on different machines and diff.
- Platform-specific outputs must have platform in the key (Bazel does via exec properties; custom caches often forget).

## Response to suspected poisoning
1. Revoke write tokens; flush the cache, or switch namespace (Bazel `--remote_instance_name=v2`, Gradle cache URL path change).
2. Rebuild releases from clean (`--noremote_accept_cached`).
3. Audit cache server logs: which identity wrote the entries.

## Verify
- [ ] PR builds and laptops can read but uploads fail (403) - test it.
- [ ] Release builds are verified with a clean, cache-disabled rebuild at least periodically.
