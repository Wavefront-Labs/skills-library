---
id: computing-software.software-engineering.ktor.ktor-swagger-ui
name: ktor-swagger-ui
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, swagger, openapi, api-docs, cors, server]
level: practitioner
status: docs-checked
description: "Serve Swagger UI from Ktor with swaggerUI(): a static OpenAPI file or runtime-generated spec, document metadata, UI version choice, and CORS."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-swagger-ui.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor Swagger UI

Serve Swagger UI for an OpenAPI spec so you can explore endpoints in the browser. Dependency: `io.ktor:ktor-server-swagger` (package `io.ktor.server.plugins.swagger`). Native server targets are not supported.

## Static spec file

```kotlin
import io.ktor.server.plugins.swagger.*

routing {
    swaggerUI(path = "swagger", swaggerFile = "openapi/documentation.yaml")
}
```

This creates a GET endpoint at `swagger`. The file is looked up in application resources first, then on the file system via `java.io.File`.

## Spec generated at runtime

Use metadata from the OpenAPI compiler plugin plus route annotations:

```kotlin
swaggerUI("/swaggerUI") {
    info = OpenApiInfo("My API", "1.0")
    source = OpenApiDocSource.Routing(ContentType.Application.Json) {
        routingRoot.descendants()
    }
}
```

The documentation at `/swaggerUI` reflects the current application state.

## Configure the document

In the `swaggerUI {}` block set `info` and define tags with `tag()`:

```kotlin
swaggerUI("/swagger") {
    info = OpenApiInfo("Books API from routes", "1.0.0")
    tag(name = "Books", description = "Operations on books")
}
```

Other top-level properties (servers, security requirements, reusable components, external documentation, extensions) are listed in the `SwaggerConfig` API reference.

## UI version

Ktor uses a predefined Swagger UI version by default; set the `version` property to change it. Gotcha: Swagger UI 5.x is required for OpenAPI 3.1.x documents; 4.x supports only 3.0.x.

## CORS

Configure CORS first so Swagger UI can reach your API. The page's example uses `anyHost` plus `allowHeader` for `Content-Type` (needed for content negotiation).

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-swagger-ui.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
