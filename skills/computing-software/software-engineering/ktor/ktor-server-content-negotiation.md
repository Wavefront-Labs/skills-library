---
id: computing-software.software-engineering.ktor.ktor-server-content-negotiation
name: ktor-server-content-negotiation
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, content-negotiation, serialization, json, kotlinx-serialization, converters]
level: advanced
status: docs-checked
description: "Set up Ktor ContentNegotiation to serialize/deserialize JSON (kotlinx, Gson, Jackson), XML, CBOR, ProtoBuf or a custom ContentConverter, and receive/respond typed data."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-serialization.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/json-kotlinx/src/main/kotlin/jsonkotlinx/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor server content negotiation and serialization

ContentNegotiation (artifact `io.ktor:ktor-server-content-negotiation`) negotiates media types using the `Accept` and `Content-Type` headers and serializes/deserializes content. Each format needs its own artifact.

## Dependencies and registration
Inside `install(ContentNegotiation) { ... }`:
- kotlinx.serialization JSON: `ktor-serialization-kotlinx-json`, call `json()` (accepts a JsonBuilder block). Add the Kotlin serialization compiler plugin first.
- Gson: `ktor-serialization-gson`, call `gson()` (GsonBuilder settings).
- Jackson: `ktor-serialization-jackson`, call `jackson()` (ObjectMapper settings).
- XML: `ktor-serialization-kotlinx-xml`, call `xml()`; e.g. `xml(format = XML { xmlDeclMode = XmlDeclMode.Charset })`.
- CBOR: `ktor-serialization-kotlinx-cbor`, call `cbor()`; e.g. `cbor(Cbor { ignoreUnknownKeys = true })`.
- ProtoBuf: `ktor-serialization-kotlinx-protobuf`, call `protobuf()`; e.g. `protobuf(ProtoBuf { encodeDefaults = true })`.
- Custom: `register(ContentType.Application.Json, CustomJsonConverter())` per content type.

Each converter import comes from `io.ktor.serialization.kotlinx.<format>.*` (Gson: `io.ktor.serialization.gson.*`, Jackson: `io.ktor.serialization.jackson.*`).

## Receive and send
With kotlinx.serialization, annotate the data class with `@Serializable`. Then:
- `call.receive<Customer>()`: the request `Content-Type` picks the serializer.
- `call.respond(customer)`: the `Accept` header picks the serializer.

```kotlin
@Serializable
data class Customer(val id: Int, val firstName: String, val lastName: String)

install(ContentNegotiation) {
    json(Json {
        prettyPrint = true
        isLenient = true
    })
}
routing {
    get("/customer/{id}") {
        val id: Int by call.parameters
        val customer: Customer = customerStorage.find { it.id == id }!!
        call.respond(customer)
    }
    post("/customer") {
        val customer = call.receive<Customer>()
        customerStorage.add(customer)
        call.respondText("Customer stored correctly", status = HttpStatusCode.Created)
    }
}
```

Gson and Jackson variants configure the builder in the block, e.g. `gson { setPrettyPrinting() }` or `jackson { registerModule(JavaTimeModule()) }`.

kotlinx.serialization also supports built-in classes, deserializing Sequences and serializing Flows.

## Custom serializer
Implement `ContentConverter`:

```kotlin
interface ContentConverter {
    suspend fun serialize(contentType: ContentType, charset: Charset, typeInfo: TypeInfo, value: Any): OutgoingContent?
    suspend fun deserialize(charset: Charset, typeInfo: TypeInfo, content: ByteReadChannel): Any?
}
```

The page points to the `GsonConverter` class as an implementation example. The client has its own separate ContentNegotiation plugin.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-serialization.md, codeSnippets/snippets/json-kotlinx/src/main/kotlin/jsonkotlinx/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
