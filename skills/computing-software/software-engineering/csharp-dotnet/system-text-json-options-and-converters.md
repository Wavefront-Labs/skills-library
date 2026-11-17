---
id: computing-software.software-engineering.csharp-dotnet.system-text-json-options-and-converters
name: system-text-json-options-and-converters
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-json, system-text-json-options, json-converters, json-polymorphism, utf8jsonreader, jsonstringenumconverter, jsonserializeroptions]
level: practitioner
status: docs-checked
description: "Configure System.Text.Json: shared JsonSerializerOptions, web defaults, custom JsonConverter<T> and [JsonPolymorphic] type discriminators (.NET 7)."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/configure-options", "https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/converters-how-to", "https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/polymorphism"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System.Text.Json options, converters and polymorphism

## Options (create once, reuse)
```csharp
static readonly JsonSerializerOptions Opts = new(JsonSerializerDefaults.Web)
{
    DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
};
```
`JsonSerializerDefaults.Web` gives the defaults ASP.NET Core uses; from .NET 9 the `JsonSerializerOptions.Web` singleton exposes the same options. Reuse one options instance for every call: caches on it are thread-safe and the instance is immutable after the first serialization or deserialization. Constructing a new options instance from an existing one does not copy its cache, so it is not the same as reusing it.

## Custom converter
Derive from `JsonConverter<T>`, override `Read` and `Write`, and apply it with the `[JsonConverter(typeof(MyConverter))]` attribute on a property or type (or add it to `options.Converters`). `JsonConverterAttribute` also supports open generic converter types on generic types when the total type-parameter arity matches. For object converters the reader loops until `JsonTokenType.EndObject`.

## Polymorphism (.NET 7+)
```csharp
[JsonPolymorphic(TypeDiscriminatorPropertyName = "kind",
                 UnknownDerivedTypeHandling = JsonUnknownDerivedTypeHandling.FailSerialization)]
[JsonDerivedType(typeof(Circle), "circle")]
[JsonDerivedType(typeof(Square), "square")]
public abstract record Shape;
```
- Other `UnknownDerivedTypeHandling` values are `FallBackToBaseType` and `FallBackToNearestAncestor`.
- Pick a `TypeDiscriminatorPropertyName` that does not conflict with a property in the hierarchy.
- Metadata properties normally have to come first in the JSON; `AllowOutOfOrderMetadataProperties = true` on the options relaxes that.

## Gotchas
- Configure ASP.NET Core's own JSON options through the framework's options hooks rather than a private instance, so request binding and your direct calls agree.
- Source generation is supported for polymorphism but not with the fast path; see the polymorphism page.

## Checked
Date: 2026-11-09. Confirmed on the three cited Learn pages: `JsonSerializerDefaults.Web`, `JsonSerializerOptions.Web` (.NET 9), options-reuse guidance and thread-safety, `DefaultIgnoreCondition = WhenWritingNull` sample, `[JsonConverter]` usage and open-generic support, `EndObject` loop, polymorphism attributes, the three `JsonUnknownDerivedTypeHandling` values, discriminator-name conflict rule and `AllowOutOfOrderMetadataProperties`. Removed unconfirmed claims: `UnmappedMemberHandling`, `RespectNullableAnnotations`, `MaxDepth` values, `JsonStringEnumConverter` options, `IncludeFields`/`[JsonInclude]`, `WriteAsString`, `DictionaryKeyPolicy`, the Unix-time converter sample, ASP.NET hook method names, and the test advice.
Method: documentation only; no commands were run.
