---
id: computing-software.software-engineering.spring-boot.spring-config-import
name: spring-config-import
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, spring-config-import, config-data, extensionless, encoding, env-prefix, import]
level: practitioner
status: docs-checked
description: "Import extra config data with spring.config.import, including fixed versus import-relative paths, file attributes, extensionless files and env: variables."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spring.config.import` pulls further config data into the Environment.

```yaml
spring:
  application:
    name: "myapp"
  config:
    import: "optional:file:./dev.properties"
```

- Imports are inserted as documents immediately below the declaring document, so imported values take precedence over the file that triggered them. Declaration order within a document does not matter.
- Several locations under one key are processed in order; later imports win.
- An import is processed only once however often it is declared.
- Profile-specific variants (`my-<profile>.properties`) are also considered.
- Properties files default to ISO-8859-1; use `"classpath:import.properties[encoding=utf-8]"`.

Fixed versus import relative: a location starting with `/` or a URL prefix (`file:`, `classpath:`) is fixed; all others resolve relative to the declaring file. `optional:` is ignored when deciding. If `/demo/application.properties` has `spring.config.import=optional:core/core.properties`, it loads `/demo/core/core.properties`.

Extensionless files (for example cloud volume mounts) need a hint: `file:/etc/config/myconfig[.yaml]`, shorthand for `[extension=.yaml]`. Multiple attributes: `file:/etc/config/myconfig[extension=.yaml][encoding=utf-8]`.
Environment variable holding properties text (for example `MY_CONFIGURATION` containing `my.name=Service1`):
`spring.config.import: "env:MY_CONFIGURATION"`. The default extension is `.properties`; an extension hint is supported.

The location API is pluggable: by default you can import Java Properties, YAML and configuration trees, and third-party jars can offer support for other technologies (the page imagines Consul, Apache ZooKeeper or Netflix Archaius). To support your own locations, see `ConfigDataLocationResolver` and `ConfigDataLoader` in `org.springframework.boot.context.config`.

## Checked

2026-11-07. Read features/external-config.html (Importing Additional Configuration) in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. Removed an attributes-at-end sentence the page does not give. Reworded the third-party location sentence to the page's pluggable-API wording (Consul, ZooKeeper, Archaius are the page's imagined examples) and pointed at ConfigDataLocationResolver and ConfigDataLoader. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
