---
id: computing-software.devops-ci-cd.dagger.function-caching-policies
name: function-caching-policies
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, function-caching, cache, ttl, session-cache, never-cache, performance]
level: practitioner
status: docs-checked
description: "Set per-function cache policy in Dagger modules (default 7-day TTL, TTL string, session, never) and understand cache keys, layer caching and secrets."
sources: [https://docs.dagger.io/0.21/extending/function-caching]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger function caching

Goal: decide how long a module function's result may be reused. From the Dagger 0.21 docs.

## Policies
| Policy | Go | Python | TypeScript |
|---|---|---|---|
| default | no annotation | `@dagger.function` | `@func()` |
| TTL | `// +cache="10s"` | `@dagger.function(cache="10s")` | `@func({ cache: "10s" })` |
| session | `// +cache="session"` | `cache="session"` | `cache: "session"` |
| never | `// +cache="never"` | `cache="never"` | `cache: "never"` |

- Default: cached with the maximum TTL, currently 7 days, for identical inputs.
- TTL: duration string, integer plus `s`, `m` or `h` (for example `10s`, `42m`). Minimum 1s, maximum 7 days. The countdown starts when the function begins executing; after expiry the next call recomputes. Suits network lookups you want refreshed periodically.
- Session: lives for the engine session (from a client connecting, such as `dagger call`, `dagger -c` or an SDK app, until it disconnects). Callers in the session share the result; concurrent clients do not.
- Never: runs on every call.

Go example:
```go
// +cache="10s"
func (Tokens) ShortLived() string { return rand.Text() }
```

## What forms the cache key
The module source code, the argument values, and the parent object's values. Any change is a miss; editing a module's source invalidates all caches of its functions.

## Function cache vs layer cache
A function cache hit skips the body entirely. A miss runs the body, but `withExec`, `withFile`, `withDirectory` and similar steps inside can still hit layer cache. `cache="never"` does not disable layer caching. To force one step to rerun, add a cache-busting input to it (for example a timestamp env var used only for that step). `withVolatileVariable` is an expert-only escape hatch for non-secret metadata (commit SHA, run ID) that must not invalidate exec cache; cached results may then be stale.

## Secrets
Secrets are never cached on disk. Functions returning values that reference secrets from a provider (`env://MY_SECRET`) may be cached using a derived hash. Secrets created with `SetSecret` inside a function block persistent caching: the call behaves as "session" (or "never" if configured so).

## Gotchas
- A TTL is an upper bound, not a retention guarantee; the engine may prune results when disk is low.
- Before engine v0.19.4 every function behaved as "session". After `dagger develop` such modules gain `"disableDefaultFunctionCaching": true` in `dagger.json`; delete the line once functions are annotated to adopt the new default. Functions pulling external data may need an explicit TTL, session or never.

Related: cache-volumes-dependencies, secrets-handling-and-caching.

## Checked

2026-11-07

Read extending/modules/function-caching.mdx in full (live slug /extending/function-caching, which returns 200): default policy and 7-day maximum TTL, TTL duration format with 1s minimum and 7-day maximum, session definition, never, cache-key inputs, function versus layer caching including the withVolatileVariable note, secrets and SetSecret behaviour, TTLs as an upper bound, and the v0.19.4 backwards-compatibility section with disableDefaultFunctionCaching. Every policy table cell matches the page's Go, Python and TypeScript snippets. No corrections needed.

Method: documentation only; no commands were run.
