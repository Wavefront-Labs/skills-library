---
id: computing-software.software-engineering.spring-boot.property-type-conversion
name: property-type-conversion
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, duration, datasize, period, base64, conversionservice, configurationpropertiesbinding]
level: practitioner
status: docs-checked
description: "Property formats for Duration, Period, DataSize and base64 Resource values, and how to add custom converters for @ConfigurationProperties binding."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Spring Boot coerces external properties to the bound type.

Duration: a plain long (milliseconds unless `@DurationUnit` says otherwise), ISO-8601 (`PT30S`), or value plus unit (`30s`). With `@DurationUnit(ChronoUnit.SECONDS)` (the page's `sessionTimeout` example) `30`, `PT30S` and `30s` are equivalent; with the default millisecond unit `500`, `PT0.5S` and `500ms` are equivalent (the page's `readTimeout` example). Units: `ns`, `us`, `ms`, `s`, `m`, `h`, `d`.

Period: a plain int (days unless `@PeriodUnit`), ISO-8601, or pairs such as `1y3d`. Units: `y`, `m`, `w`, `d`. Weeks are only a shortcut for 7 days.

DataSize (Spring `DataSize`): a plain long (bytes unless `@DataSizeUnit`) or value plus unit: `10` equals `10MB` when the unit is megabytes; `256` equals `256B`. Units: `B`, `KB`, `MB`, `GB`, `TB`.

When upgrading a `Long` property to these types, define the unit with `@DurationUnit` or `@DataSizeUnit` if it is not milliseconds or bytes; the page says this gives a transparent upgrade path while supporting a richer format.

Base64: a `Resource` property accepts `base64:` text, for example
```yaml
my:
  property: base64:SGVsbG8gV29ybGQ=
```
A `Resource` can also be given as a path.

Custom conversion: provide a `ConversionService` bean named `conversionService`, custom property editors via a `CustomEditorConfigurer` bean, or converters on beans annotated `@ConfigurationPropertiesBinding`. These beans are requested very early, so limit their dependencies. A `@Bean` method qualified with `@ConfigurationPropertiesBinding` should be `static` to avoid the "not eligible for getting processed by all BeanPostProcessors" warning. Consider renaming your own `ConversionService` if only the qualified converters are needed.

## Checked

2026-11-07. Read features/external-config.html (Properties Conversion, Durations) in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. Qualified the Duration equivalence: 30, PT30S and 30s are equivalent only with @DurationUnit(ChronoUnit.SECONDS); 500, PT0.5S and 500ms with the default millisecond unit. Aligned the upgrade-path sentence with the page. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
