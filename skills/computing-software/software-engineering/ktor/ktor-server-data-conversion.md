---
id: computing-software.software-engineering.ktor.ktor-server-data-conversion
name: ktor-server-data-conversion
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, data-conversion, converters, conversionservice, encode-decode, kotlin]
level: advanced
status: docs-checked
description: "Add custom type converters to the Ktor DataConversion plugin with convert<T>, encode and decode, and call the conversion service via fromValues and toValues."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-data-conversion.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor DataConversion plugin

DataConversion (artifact `io.ktor:ktor-server-data-conversion`, package `io.ktor.server.plugins.dataconversion`) serializes and deserializes a list of values. By default `DefaultConversionService` handles strings and common types: numeric types, unsigned integer types, `Uuid` and enums. Install the plugin to extend it with more types.

## Add a converter
Inside the plugin configuration, provide `convert<T> { ... }` for the type and define two functions:

```kotlin
decode { values ->   // (values: List<String>) -> Any?
    // deserialize: values are the repeated values from the URL
}
encode { value ->    // (value: Any?) -> List<String>
    // serialize: return strings representing the value
}
```

## Use the service
Get it from the application: `val dataConversion = application.conversionService`. Then call:
- `fromValues(values: List<String>, type: TypeInfo)`: takes strings and the target `TypeInfo`, returns the decoded value.
- `toValues(value: Any?)`: takes any value, returns a list of strings.

## Example from the page
A converter for `LocalDate`: `encode` formats the value with a `SimpleDateFormat` and returns a list holding the formatted string; `decode` turns the string back into a `LocalDate`. The service is then called manually to obtain the encoded and decoded values.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-data-conversion.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
