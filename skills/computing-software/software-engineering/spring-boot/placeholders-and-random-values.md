---
id: computing-software.software-engineering.spring-boot.placeholders-and-random-values
name: placeholders-and-random-values
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, placeholders, random-value, property-placeholder, random-int, canonical-form]
level: intro
status: docs-checked
description: "Use property placeholders with defaults in application files, refer to canonical kebab-case names, and generate random.* values for secrets and tests."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Values in `application.properties` and `application.yaml` are filtered through the Environment when used, so they can refer to earlier values such as system properties or environment variables. Syntax is `${name}`, with a default after a colon: `${name:default}`.

```yaml
app:
  name: "MyApp"
  description: "${app.name} is a Spring Boot application written by ${username:Unknown}"
```
If `username` is unset elsewhere, `app.description` is `MyApp is a Spring Boot application written by Unknown`.

Always use the canonical form (lowercase kebab-case) in placeholders so Boot applies relaxed-binding logic. `${demo.item-price}` picks up `demo.item-price`, `demo.itemPrice` and `DEMO_ITEMPRICE`. `${demo.itemPrice}` picks up `demo.itemPrice` and `DEMO_ITEMPRICE` but not `demo.item-price`. The same applies to `@Value`.

Placeholders can also build short variants of existing Spring Boot properties (see the how-to guide on short command line arguments).

Random values come from `RandomValuePropertySource`, which only serves `random.*`:
```yaml
my:
  secret: "${random.value}"
  number: "${random.int}"
  bignumber: "${random.long}"
  uuid: "${random.uuid}"
  number-less-than-ten: "${random.int(10)}"
  number-in-range: "${random.int[1024,65536]}"
```
`random.int*` syntax is `OPEN value (,max) CLOSE` where OPEN and CLOSE are any character and value, max are integers. With `max`, `value` is the minimum and `max` is exclusive.

## Checked

2026-11-07. Read features/external-config.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
