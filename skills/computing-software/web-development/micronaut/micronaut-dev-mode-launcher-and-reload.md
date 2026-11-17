---
id: computing-software.web-development.micronaut.micronaut-dev-mode-launcher-and-reload
name: micronaut-dev-mode-launcher-and-reload
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, dev-mode, hot-reload, livereload, launcher, access-token, bean-retention, development]
level: advanced
status: docs-checked
description: "Start the Micronaut development-mode launcher, understand what a change does (restart, in-place body edit, config refresh), secure the dev pages and use LiveReload."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/devMode/devModeLaunch.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/devMode/devModeReload.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Development mode: launcher, reload behavior, security, LiveReload

Goal: run an app under the `micronaut-dev` launcher and know how edits are applied. Not for production: run the packaged application there. The build plugins normally write the manifest and start the launcher.

## Manifest and start

A `java.util.Properties` file naming main class, reloadable dirs, classpaths, sources and resources:

```properties
micronaut.dev.main-class=example.Application
micronaut.dev.reloadable=build/classes/java/main,build/resources/main
micronaut.dev.compile-classpath=@build/micronaut-dev/compile.argfile
micronaut.dev.processor-path=@build/micronaut-dev/processors.argfile
micronaut.dev.sources.java=src/main/java
micronaut.dev.resources.config=src/main/resources
micronaut.dev.compile.java.output=build/classes/java/main
micronaut.dev.retain=javax.sql.DataSource
micronaut.dev.patch-in-place=true
```

Relative paths resolve against the manifest directory; `@file` reads a list from an argument file; a system property of the same name overrides an entry.

```bash
java -cp @build/micronaut-dev/runtime.argfile io.micronaut.dev.MicronautDevMain --manifest build/micronaut-dev/dev.properties
```

The runtime classpath excludes the project's own class dirs (they are the reloadable tier). On macOS add `micronaut-runtime-osx` for native file events; otherwise (and in native images) directories are compared every 250 ms. Startup logs `Development Mode Active: Not for production usage.`, a link to the development pages with the token, and the LiveReload port. Beans can be conditioned with `@DevelopmentActive` / `@DevelopmentInactive`.

## What a change does

- Source changes compile as one batch into a staging dir; a failed compile leaves the running app untouched and errors are logged (and shown in the browser instead of the page).
- Class change: the old context stops (retaining beans per `BeanRetentionPolicy`), a new class-loader generation starts, `main` runs again. `ClassChangeEvent` goes to the old context, `ReloadCompletedEvent` to the new.
- Method-body-only edits are applied in place (no restart) with `micronaut.dev.strategy=auto` (default) or `reload`, when class structure is unchanged and no generated class changed; this needs the `-javaagent` the build plugins add. `strategy=restart` always restarts.
- Config files are applied in place; a restart happens only if a configuration watch answers `REQUIRES_RESTART`, a singleton received the changed property by `@Value`/`@Property`, or a `@Requires` names the changed property.
- Templates, static files and message bundles restart nothing.
- Retention: `micronaut.dev.retain` or `@Retain`; `micronaut.dev.retain-annotated=false` retains only what `micronaut.dev.retain` names. Beans holding application classes are not retained.

## Dev endpoint and security

With `micronaut-management`: `GET /dev` (generation, strategy, roots, last compile failure) and `POST /dev/reload` (compile everything, restart if changed). The endpoint is sensitive (401) until Micronaut Security protects it or you set `endpoints.dev.sensitive: false`.

```bash
curl -X POST -H 'Content-Type: application/json' -H "X-Micronaut-Dev-Token: $TOKEN" http://localhost:8080/dev/reload
```

- A random 256-bit token is created per launcher start; opening the logged link sets an HttpOnly, SameSite=Strict cookie. Non-browser clients send `X-Micronaut-Dev-Token`; missing token gives 401.
- Only `Host` values `localhost`, `*.localhost`, `127.0.0.1`, `[::1]` are answered, others 403. Add hosts with `-Dmicronaut.dev.allowed-hosts=devbox.lan,app-container` (no wildcards).
- In run mode the server binds to `localhost` (`micronaut.server.host` set at lowest precedence); `micronaut.dev.bind-loopback=false` turns this off.
- `micronaut.dev.access-token.enabled=false` disables the token.

## LiveReload

Add `micronaut-dev-livereload` to the dev runtime classpath: server on port 35729 (`micronaut.dev.livereload.port`), browsers reload on restart or template change and swap stylesheets in place. Pages with a Content-Security-Policy are not injected; `micronaut.dev.livereload.inject-script=false` if you use a browser extension. For non-local origins list them in `micronaut.dev.livereload.allowed-origins` (e.g. `http://devbox.lan:8080,app-container`; entries with `*` are ignored with a warning).

## Native image generation budget

Retired generations are never unloaded in a native image; `micronaut.dev.max-generations` (50 for native, unlimited on JVM; `0` or `unlimited` lifts it) triggers exit status `3` so the launcher is started again.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
