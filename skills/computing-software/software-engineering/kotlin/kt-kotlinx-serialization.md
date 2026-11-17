---
id: computing-software.software-engineering.kotlin.kt-kotlinx-serialization
name: kt-kotlinx-serialization
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-multiplatform, kotlinx-serialization]
level: practitioner
status: docs-checked
description: "Serialize data classes with kotlinx.serialization and configure Json for unknown keys, defaults and polymorphism."
sources: ["https://kotlinlang.org/docs/serialization.html", "https://kotlinlang.org/docs/serialization-configure-json-serialization.html", "https://kotlinlang.org/docs/serialization-json-configuration.html", "https://kotlinlang.org/docs/serialization-customization-options.html", "https://kotlinlang.org/docs/serialization-polymorphism.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kotlinx.serialization JSON
- Apply the serialization compiler plugin (see the setup section of the serialization overview page) and annotate classes with `@Serializable`; rename a property in the encoded form with `@SerialName`.
- Configure a `Json { ... }` instance: `ignoreUnknownKeys = true` tolerates extra keys, and `encodeDefaults` and `explicitNulls` control default and null output (see the Json configuration page for their defaults). Decode with `decodeFromString<T>(text)`.
- Polymorphism uses a class discriminator property, `"type"` by default, configurable through `classDiscriminator`; sealed hierarchies or a `SerializersModule` register subclasses.
- A missing required property raises `MissingFieldException`.
Verify: a round-trip test plus a payload with unknown fields.

## Checked
2026-11-03. Confirmed on the serialization pages: @Serializable, @SerialName, ignoreUnknownKeys, encodeDefaults, explicitNulls, classDiscriminator, default "type" discriminator, MissingFieldException, decodeFromString.
Removed: the plugin id string, specific values for encodeDefaults/explicitNulls and the claim that missing fields throw `SerializationException` (the page names `MissingFieldException`).
Method: documentation only; no commands were run.
