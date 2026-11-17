---
id: computing-software.software-engineering.ktor.ktor-thymeleaf
name: ktor-thymeleaf
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, thymeleaf, templates, views, html, server]
level: intro
status: docs-checked
description: "Render Thymeleaf HTML templates in Ktor: add ktor-server-thymeleaf, configure ClassLoaderTemplateResolver, respond with ThymeleafContent, and auto-reload in dev mode."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-thymeleaf.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/thymeleaf/src/main/kotlin/com/example/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/thymeleaf-auto-reload/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor Thymeleaf views

The `Thymeleaf` plugin (package `io.ktor.server.thymeleaf`, artifact `io.ktor:ktor-server-thymeleaf`) lets you use Thymeleaf templates as views. Native server targets are not supported.

## Steps

1. Add `io.ktor:ktor-server-thymeleaf` to the build script.
2. Install the plugin: `install(Thymeleaf) { ... }`.
3. In the block, configure a `ClassLoaderTemplateResolver`. The page's example makes Ktor find `*.html` templates in the `templates` package relative to the current classpath (so files live in `resources/templates`):

```kotlin
install(Thymeleaf) {
    setTemplateResolver(ClassLoaderTemplateResolver().apply {
        prefix = "templates/"
        suffix = ".html"
        characterEncoding = "utf-8"
    })
}
```

4. Create a template such as `index.html` in `resources/templates`:

```html
<html xmlns:th="http://www.thymeleaf.org">
    <body>
        <h1 th:text="'Hello, ' + ${user.name}"></h1>
    </body>
</html>
```

5. Define a data class for the model: `data class User(val id: Int, val name: String)`.
6. In a route, pass `ThymeleafContent` to `call.respond` with the template name and a model map:

```kotlin
get("/index") {
    val sampleUser = User(1, "John")
    call.respond(ThymeleafContent("index", mapOf("user" to sampleUser)))
}
```

## Auto-reload during development

The `thymeleaf-auto-reload` example reloads Thymeleaf templates automatically when Ktor's development mode is used: a `FileTemplateResolver` (no cache) in development mode, a `ClassLoaderTemplateResolver` otherwise.

```kotlin
install(Thymeleaf) {
    setTemplateResolver((if (developmentMode) {
        FileTemplateResolver().apply {
            cacheManager = null
            prefix = "src/main/resources/templates/"
        }
    } else {
        ClassLoaderTemplateResolver().apply {
            prefix = "templates/"
        }
    }).apply {
        suffix = ".html"
        characterEncoding = "utf-8"
    })
}
```

## Gotchas

- The resolver configuration controls the file suffix; the example sets `suffix = ".html"`.
- `ClassLoaderTemplateResolver` looks templates up on the classpath (prefix `templates/`, i.e. `resources/templates`); the dev-mode example instead reads `src/main/resources/templates/` from disk with `FileTemplateResolver`.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-thymeleaf.md, codeSnippets/snippets/thymeleaf/src/main/kotlin/com/example/Application.kt, codeSnippets/snippets/thymeleaf-auto-reload/src/main/kotlin/com/example/Application.kt.

Removed or changed: replaced an unconfirmed Gotchas claim that templates must be under resources (the dev-mode example reads from src/main/resources/templates on disk) with what the page shows.

Method: documentation only; no commands were run.
