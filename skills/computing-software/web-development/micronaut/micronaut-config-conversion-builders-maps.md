---
id: computing-software.web-development.micronaut.micronaut-config-conversion-builders-maps
name: micronaut-config-conversion-builders-maps
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, type-converter, configuration-builder, mapformat, duration, readablebytes, conversion]
level: practitioner
status: docs-checked
description: "Convert config values to durations, lists, byte sizes and dates, write a custom TypeConverter, fill builders with @ConfigurationBuilder and bind free-form maps."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/configurationProperties.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/customTypeConverter.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: bind non-trivial configuration values. Conversion goes through the `ConversionService` bean; add converters by defining beans of type `TypeConverter`.

## Built-in conversions

- Duration: `10ms`, `10s`, `10m`, `10h`, `10d`, `10ns`, or ISO-8601 `PT15M` (e.g. `micronaut.http.client.read-timeout: 15s`).
- Lists/arrays: comma-separated in properties files, native lists in YAML; generics drive element conversion (`List<Integer>`, `List<URL>`).
- Bytes: annotate a setter parameter with `@ReadableBytes` (`public void setMaxContentLength(@ReadableBytes int maxContentLength)`); accepts `10mb`, `10kb`, `10gb` or raw `1024`.
- Dates: `public void setMyDate(@Format("yyyy-MM-dd") LocalDate date)`.

## Custom TypeConverter

Map-to-`LocalDate` example binding `myapp.updatedAt` given as `day`/`month`/`year` keys:

```java
@Prototype
public class MapToLocalDateConverter implements TypeConverter<Map, LocalDate> {
    private final ConversionService conversionService;

    public MapToLocalDateConverter(ConversionService conversionService) {
        this.conversionService = conversionService;
    }

    @Override
    public Optional<LocalDate> convert(Map propertyMap, Class<LocalDate> targetType, ConversionContext context) {
        Optional<Integer> day = conversionService.convert(propertyMap.get("day"), Integer.class);
        Optional<Integer> month = conversionService.convert(propertyMap.get("month"), Integer.class);
        Optional<Integer> year = conversionService.convert(propertyMap.get("year"), Integer.class);
        if (day.isPresent() && month.isPresent() && year.isPresent()) {
            try {
                return Optional.of(LocalDate.of(year.get(), month.get(), day.get()));
            } catch (DateTimeException e) {
                context.reject(propertyMap, e);
                return Optional.empty();
            }
        }
        return Optional.empty();
    }
}
```

Inject `ConversionService` (Micronaut 4) instead of calling `ConversionService.SHARED`; call `context.reject(..)` on failure so the container gets detail. To add to `ConversionService.SHARED`, register a `TypeConverterRegistrar` via the service loader.

## @ConfigurationBuilder

Fill builder-style classes inside a `@ConfigurationProperties` class:

```java
@ConfigurationProperties("my.engine")
class EngineConfig {
    @ConfigurationBuilder(prefixes = "with")
    EngineImpl.Builder builder = EngineImpl.builder();

    @ConfigurationBuilder(prefixes = "with", configurationPrefix = "crank-shaft")
    CrankShaft.Builder crankShaft = CrankShaft.builder();

    private SparkPlug.Builder sparkPlug = SparkPlug.builder();

    @ConfigurationBuilder(prefixes = "with", configurationPrefix = "spark-plug")
    void setSparkPlug(SparkPlug.Builder sparkPlug) { this.sparkPlug = sparkPlug; }
}
```

Use an empty-string prefix when builder methods have none. Without `configurationPrefix` the class prefix is used. Only single-argument methods are supported unless `allowZeroArgs = true`. Build the final object in a `@Factory` method taking `EngineConfig`.

## @MapFormat

Bind an open-ended map to one property:

```java
@MapFormat(transformation = MapFormat.MapTransformation.FLAT)
private Map<Integer, String> sensors;
```

`MapTransformation.FLAT` gives a flat map, `NESTED` a nested one.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
