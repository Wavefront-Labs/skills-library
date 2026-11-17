---
id: computing-software.software-engineering.spring-boot.relaxed-binding-rules
name: relaxed-binding-rules
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, relaxed-binding, kebab-case, environment-variables, map-binding, configurationproperties]
level: practitioner
status: docs-checked
description: "Property name forms accepted by relaxed binding, converting names to environment variables, list and Map key rules, and binding cache behaviour."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Environment property names need not match bean property names exactly. For prefix `my.main-project.person` and field `firstName`, all of these bind:
- `my.main-project.person.first-name` (kebab case, recommended in properties/YAML)
- `my.main-project.person.firstName` (camel case)
- `my.main-project.person.first_name` (underscore)
- `MY_MAINPROJECT_PERSON_FIRSTNAME` (upper case, recommended for environment variables)

The annotation `prefix` must be kebab case. Store properties as lowercase kebab, for example `my.person.first-name=Rod`.

Lists: properties and system properties use `[ ]` or comma-separated values; YAML uses YAML lists or comma-separated values.

Environment variables: replace `.` with `_`, remove `-`, uppercase. `spring.main.log-startup-info` becomes `SPRING_MAIN_LOGSTARTUPINFO`. For lists surround the index with underscores: `my.service[0].other` becomes `MY_SERVICE_0_OTHER`. Applies to the `systemEnvironment` source and any source named `*-systemEnvironment`.

Maps: if the key is not wrapped in `[]`, characters other than alphanumerics, `-` and `.` are removed. In YAML quote the bracketed keys:
```yaml
my:
  map:
    "[/key1]": "value1"
    "/key3": "value3"
```
`/key1` keeps its slash; `/key3` becomes `key3`. For scalar value types (enums and `java.lang` types except `Object`) keys with `.` need no brackets: `a.b=c` into `Map<String,String>` gives `{"a.b"="c"}`. For `Map<String,Object>`, `a.b=c` gives `{"a"={"b"="c"}}` while `[a.b]=c` gives `{"a.b"="c"}`.

Maps from environment variables: the variable name is lowercased before binding, so keys are lowercase (`MY_PROPS_VALUES_KEY=VALUE` gives `{"key"="VALUE"}`; the value keeps its case).

Caching: relaxed binding caches only immutable property sources by default; adjust with `ConfigurationPropertyCaching`.

## Checked

2026-11-07. Read features/external-config.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
