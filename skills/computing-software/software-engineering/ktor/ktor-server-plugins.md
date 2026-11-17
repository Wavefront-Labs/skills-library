---
id: computing-software.software-engineering.ktor.ktor-server-plugins
name: ktor-server-plugins
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, plugins, install, routing, kotlin, server]
level: intro
status: docs-checked
description: "Add Ktor server plugins: add the artifact dependency, call install() in embeddedServer or a module, and install plugins on specific routes with override rules."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install and scope Ktor server plugins

Plugins provide functionality separate from application logic: authentication, serialization, content encoding, compression, headers, cookies. A request goes through the request pipeline to the handler, and the response passes through the response pipeline before it reaches the client. Plugins can intercept either side. `routing` is itself a plugin.

## Steps

1. Add the plugin's artifact to the build script. Most plugins need their own dependency; for example `CORS` needs `ktor-server-cors`. The plugin's own docs page names the artifact; the Ktor Project Generator lists all plugins.
2. Ktor installs no plugins by default. Install what the application needs with `install()` during server initialization, either inside `embeddedServer()` or in an application module:

```kotlin
fun Application.module() {
    install(CORS)
    install(Compression)
}
```

3. Configure at install time with a configuration block, for example:

```kotlin
install(Sessions) {
    cookie<MyCookie>("MY_COOKIE")
}
```

## Install on specific routes

Plugins can also be installed inside `routing`, on a `route(...)`, so different resources get different configuration (for example `install(CachingHeaders) { ... }` inside `route("index")`).

Rules when the same plugin is installed at several levels:

- A route-level configuration overrides the global plugin configuration.
- If the same route is defined several times with several installations of the same plugin, routing merges them and the last installation wins. With two `route("index")` blocks each installing `CachingHeaders`, calls to both `/index/a` and `/index/b` are handled by the second installation only.

## Gotchas

- To reuse functionality across applications, write a custom plugin (see ktor-server-custom-plugins).

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-plugins.md.

Removed or changed: removed an unconfirmed Gotchas bullet about a missing dependency being the usual reason install() fails to resolve.

Method: documentation only; no commands were run.
