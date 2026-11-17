---
id: computing-software.software-engineering.ktor.ktor-freemarker
name: ktor-freemarker
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, freemarker, templates, views, ftl, server]
level: intro
status: docs-checked
description: "Render FreeMarker .ftl templates in Ktor: add ktor-server-freemarker, set templateLoader in the install block, and respond with FreeMarkerContent."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-freemarker.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/freemarker/src/main/kotlin/com/example/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/freemarker/src/main/resources/templates/index.ftl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor FreeMarker views

Install the `FreeMarker` plugin (package `io.ktor.server.freemarker`, artifact `io.ktor:ktor-server-freemarker`) to use FreeMarker templates as views. Native server targets are not supported.

## Steps

1. Add the dependency `io.ktor:ktor-server-freemarker` to the build script.
2. Install the plugin with `install(FreeMarker) { ... }` in your application module.
3. Inside the block, assign a FreeMarker `TemplateLoader` to the `templateLoader` property. The page's example makes Ktor look up templates in the `templates` package relative to the current classpath (i.e. files under `resources/templates`).
4. Put a template such as `index.ftl` in `resources/templates`.
5. Define a data class for the model (the page uses a user model).
6. In a route, respond by passing `FreeMarkerContent` to `call.respond`, giving the template name and the data model.

```kotlin
import freemarker.cache.*
import io.ktor.server.freemarker.*

fun Application.module() {
    install(FreeMarker) {
        templateLoader = ClassTemplateLoader(this::class.java.classLoader, "templates")
    }
    routing {
        get("/index") {
            val sampleUser = User(1, "John")
            call.respond(FreeMarkerContent("index.ftl", mapOf("user" to sampleUser)))
        }
    }
}

data class User(val id: Int, val name: String)
```

`resources/templates/index.ftl`:

```html
<html>
    <body>
        <h1>Hello, ${user.name}!</h1>
    </body>
</html>
```

## Gotchas

- The key in the model map (`user`) is the name the template uses.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-freemarker.md, codeSnippets/snippets/freemarker/src/main/kotlin/com/example/Application.kt, codeSnippets/snippets/freemarker/src/main/resources/templates/index.ftl.

Removed or changed: removed an unconfirmed Gotchas bullet about TemplateLoader types.

Method: documentation only; no commands were run.
