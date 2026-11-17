---
id: computing-software.software-engineering.ktor.ktor-server-single-page-application
name: ktor-server-single-page-application
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, single-page-application, spa, react, static-content, kotlin]
level: intro
status: docs-checked
description: "Serve React, Angular or Vue single-page apps from Ktor with singlePageApplication, and customise resource serving with useResources, filesPath, defaultPage, ignoreFiles."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-serving-spa.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serving single-page applications with Ktor

Only the `ktor-server-core` dependency is needed. You must say where the app lives: a local folder or a classpath resource package, and give at least that folder or package name.

## Framework build from a folder
With a `react-app` folder in the project root (containing `index.html` and a `static` subfolder), call `singlePageApplication` inside `routing` and pass the folder to the `react` function:

```kotlin
import io.ktor.server.application.*
import io.ktor.server.http.content.*
import io.ktor.server.routing.*

fun Application.module() {
    routing {
        singlePageApplication {
            react("react-app")
        }
    }
}
```

Ktor finds `index.html` automatically. For other frameworks use the matching functions, such as `angular`, `vue`, `ember`.

## Custom settings (resources example)
For an app in the `sample-web-app` resource package (`main.html`, `ktor_logo.png`, `css/styles.css`, `js/script.js`) configure the block with:
- `useResources`: serve from a resource package.
- `filesPath`: path under which the application is located.
- `defaultPage`: default resource to serve (`main.html` here instead of `index.html`).
- `ignoreFiles`: ignores paths that contain `.txt` at the end.

Full sample: the `single-page-application` project in the ktor-documentation code snippets.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-serving-spa.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
