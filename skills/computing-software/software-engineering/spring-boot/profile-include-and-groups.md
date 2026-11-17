---
id: computing-software.software-engineering.spring-boot.profile-include-and-groups
name: profile-include-and-groups
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, profiles, spring-profiles-include, spring-profiles-group, profile-groups]
level: practitioner
status: docs-checked
description: "Add profiles on top of active ones with spring.profiles.include and define profile groups that activate related profiles under one name."
sources:
  - https://docs.spring.io/spring-boot/reference/features/profiles.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Adding profiles: `spring.profiles.include` adds active profiles on top of those from `spring.profiles.active`, instead of replacing them. With
```yaml
spring:
  profiles:
    include:
      - "common"
      - "local"
```
the `common` and `local` profiles are active even when the app runs with `--spring.profiles.active`. Included profiles are added before any `spring.profiles.active` profiles. The Java API is `SpringApplication.setAdditionalProfiles()`.

The property is processed for each property source, so the usual complex-type merging rules for lists do not apply.

Profile groups: when profiles are too fine-grained (for example `proddb` and `prodmq`), define a group with a logical name:
```yaml
spring:
  profiles:
    group:
      production:
      - "proddb"
      - "prodmq"
```
Starting with `--spring.profiles.active=production` activates `production`, `proddb` and `prodmq` together.

Constraint: like `spring.profiles.active`, both `spring.profiles.include` and `spring.profiles.group` can be used only in non-profile-specific documents. They cannot be in profile-specific files or in documents activated by `spring.config.activate.on-profile`.

## Checked

2026-11-07. Read features/profiles.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
