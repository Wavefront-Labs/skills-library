---
id: computing-software.software-engineering.ktor.ktor-server-type-safe-routing
name: ktor-server-type-safe-routing
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, resources, type-safe-routing, kotlinx-serialization, reverse-routing, href]
level: advanced
status: docs-checked
description: "Use the Ktor Resources plugin for type-safe routing: @Resource classes with query/path params and nesting, typed get/post handlers, and href reverse routing."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-resources.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/resource-routing/src/main/kotlin/resourcerouting/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type-safe routing with the Ktor Resources plugin

The Resources plugin (artifact `io.ktor:ktor-server-resources`, package `io.ktor.server.resources`) lets classes act as typed routes. Resource classes need `@Serializable` behaviour (`@Resource` provides it through kotlinx.serialization), so add the Kotlin serialization plugin to the build first. Install with `install(Resources)`.

## Resource classes
```kotlin
import io.ktor.resources.*

@Resource("/articles")
class Articles(val sort: String? = "new") {   // query parameter /articles?sort=new
    @Resource("new")
    class New(val parent: Articles = Articles())      // /articles/new

    @Resource("{id}")
    class Id(val parent: Articles = Articles(), val id: Long) {   // /articles/12
        @Resource("edit")
        class Edit(val parent: Id)
    }
}
```

Nested classes must have a property whose type is the outer class. A plain property is a query parameter; a `{id}` segment matches a path segment and captures it as the parameter named `id`.

## Route handlers
Pass the class as a type argument to the verb functions; the resource instance arrives as the lambda parameter:

```kotlin
fun Application.module() {
    install(Resources)
    routing {
        get<Articles> { article ->
            // Get all articles ...
            call.respondText("List of articles sorted starting from ${article.sort}")
        }
        get<Articles.New> {
            // Show a page with fields for creating a new article ...
            call.respondText("Create a new article")
        }
        post<Articles> {
            // Save an article ...
            call.respondText("An article is saved", status = HttpStatusCode.Created)
        }
        get<Articles.Id> { article ->
            // Show an article with id ${article.id} ...
            call.respondText("An article with id ${article.id}", status = HttpStatusCode.OK)
        }
        get<Articles.Id.Edit> { article ->
            // Show a page with fields for editing an article ...
            call.respondText("Edit an article with id ${article.parent.id}", status = HttpStatusCode.OK)
        }
        put<Articles.Id> { article ->
            // Update an article ...
            call.respondText("An article with id ${article.id} updated", status = HttpStatusCode.OK)
        }
        delete<Articles.Id> { article ->
            // Delete an article ...
            call.respondText("An article with id ${article.id} deleted", status = HttpStatusCode.OK)
        }
    }
}
```

The `post`/`put` imports come from `io.ktor.server.resources` (`io.ktor.server.resources.post`, `io.ktor.server.resources.put`). Handler roles: `get<Articles>` list sorted by `sort`; `get<Articles.New>` create form; `post<Articles>` receives form parameters or a JSON object (with ContentNegotiation); `get<Articles.Id>` one article; `get<Articles.Id.Edit>` edit form; `put<Articles.Id>` receives form parameters; `delete<Articles.Id>` delete.

## Reverse routing (build links)
The plugin adds an overloaded `href` on `Application`. For the `Edit` resource with id 123 it yields `/articles/123/edit?sort=new`, because the parent `Articles` supplies the default `sort`. Pass a `URLBuilder` to include host and protocol and extra query parameters, e.g. result `https://ktor.io/articles?token=123`. Use links in HTML DSL pages or redirect responses.

```kotlin
val link: String = href(Articles.Id.Edit(Articles.Id(id = 123)))   // /articles/123/edit?sort=new

val urlBuilder = URLBuilder(URLProtocol.HTTPS, "ktor.io", parameters = parametersOf("token", "123"))
href(Articles(sort = null), urlBuilder)
val link2: String = urlBuilder.buildString()   // https://ktor.io/articles?token=123
```

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-resources.md, codeSnippets/snippets/resource-routing/src/main/kotlin/resourcerouting/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
