---
id: computing-software.software-engineering.spring-boot.merging-lists-and-maps
name: merging-lists-and-maps
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, merging, lists, maps, profile-override, configurationproperties]
level: practitioner
status: docs-checked
description: "How list and Map properties behave when set in several places or profiles: lists are replaced entirely, Maps are merged per key by priority."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Lists replace; Maps merge.

List rule: when a list is configured in more than one place, the highest-priority definition replaces the whole list. Example:
```yaml
my:
  list:
  - name: "my name"
    description: "my description"
---
spring:
  config:
    activate:
      on-profile: "dev"
my:
  list:
  - name: "my another name"
```
With `dev` active, `MyProperties.list` holds one entry (name `my another name`, description `null`). The second document does not add an item and does not merge fields. With multiple profiles defining a list, only the highest-priority one is used. In YAML, comma-separated and YAML lists both fully override.

Map rule: Map properties bind from several sources, but for the same key the highest priority wins. With
```yaml
my:
  map:
    key1:
      name: "my name 1"
      description: "my description 1"
---
spring:
  config:
    activate:
      on-profile: "dev"
my:
  map:
    key1:
      name: "dev name 1"
    key2:
      name: "dev name 2"
      description: "dev description 2"
```
the `dev` profile yields `key1` (name `dev name 1`, description `my description 1`) and `key2`.

These rules apply to all property sources, not only files.

## Checked

2026-11-07

Read the Merging Complex Types section of external-config.adoc (docs-repo source of the cited Externalized Configuration page) in full (lists, multiple profiles, maps and the closing NOTE). The list/MyProperties and map/MyProperties include examples were not opened; the YAML in the page and skill matches.
Confirmed: whole-list replacement across places; the my name / my another name example with description null; no second instance and no item merging; "highest priority (and only that one)" for lists in multiple profiles; comma-separated and YAML lists both overriding fully; Map binding from several sources with per-key highest priority, the key1/key2 dev example (key1 name "dev name 1" keeps description "my description 1"); the rules apply to all property sources, not only files.
Nothing trimmed.

Method: documentation only; no commands were run.
