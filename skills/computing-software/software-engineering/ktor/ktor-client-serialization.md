---
id: computing-software.software-engineering.ktor.ktor-client-serialization
name: ktor-client-serialization
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, kotlin, http-client, content-negotiation, json, serialization, xml]
level: practitioner
status: docs-checked
description: "Install Ktor client ContentNegotiation and register JSON (kotlinx, Gson, Jackson), XML, CBOR or ProtoBuf converters to send and receive typed bodies and control Accept."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/client-serialization.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ContentNegotiation and serialization in the Ktor client

`ContentNegotiation` negotiates media types (via `Accept` and `Content-Type`) and serializes request bodies / deserializes response bodies. Built-in formats: JSON, XML, CBOR, ProtoBuf. It needs `ktor-client-content-negotiation` plus one serializer artifact.

## Artifacts

- JSON: `ktor-serialization-kotlinx-json`, `ktor-serialization-gson` or `ktor-serialization-jackson`.
- XML: `ktor-serialization-kotlinx-xml`. CBOR: `ktor-serialization-kotlinx-cbor`. ProtoBuf: `ktor-serialization-kotlinx-protobuf`.
- For `kotlinx.serialization`, first add the Kotlin serialization compiler plugin and annotate classes with `@Serializable`.

## Install and register

```kotlin
val client = HttpClient(CIO) {
    install(ContentNegotiation) {
        json()   // or gson(), jackson(), xml(), cbor(), protobuf()
    }
}
```

Imports: `io.ktor.client.plugins.contentnegotiation.*` plus the serializer package, e.g. `io.ktor.serialization.kotlinx.json.*`.

Customize by passing a config: `json(Json { ... })` (see `JsonBuilder`), a `gson { }` block (`GsonBuilder`), `jackson { enable(SerializationFeature.INDENT_OUTPUT) }` (`ObjectMapper`), `xml(format = XML { xmlDeclMode = XmlDeclMode.Charset })`, `cbor(Cbor { ignoreUnknownKeys = true })`, `protobuf(ProtoBuf { encodeDefaults = true })`.

## Accept header

By default the plugin adds the registered content types to the outgoing `Accept` header. To keep an `Accept` header you set yourself, set `acceptHeaderMergeStrategy = ContentTypeMergeStrategy.SkipIfPresent`; if the request has no `Accept`, the plugin still adds the registered types.

## Send and receive

- Send: `setBody(customer)` and `contentType(ContentType.Application.Json)`. For other formats use the matching type, such as `ContentType.Application.Xml` or `ContentType.Application.Cbor`.
- Receive: `response.body<Customer>()` when the server returns a supported content type.

The server has its own `ContentNegotiation` plugin; make sure you install the client one.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/client-serialization.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
