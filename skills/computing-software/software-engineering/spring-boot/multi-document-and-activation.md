---
id: computing-software.software-engineering.spring-boot.multi-document-and-activation
name: multi-document-and-activation
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, multi-document, yaml, spring-config-activate, on-profile, on-cloud-platform]
level: practitioner
status: docs-checked
description: "Split one properties or YAML file into documents and activate them conditionally with spring.config.activate.on-profile or on-cloud-platform."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A single physical file can hold several logical documents, each added independently. They are processed top to bottom and later ones override earlier ones.

YAML uses `---`:
```yaml
spring:
  application:
    name: "MyApp"
---
spring:
  application:
    name: "MyCloudApp"
  config:
    activate:
      on-cloud-platform: "kubernetes"
```
`.properties` files use a `#---` or `!---` comment:
```properties
spring.application.name=MyApp
#---
spring.application.name=MyCloudApp
spring.config.activate.on-cloud-platform=kubernetes
```
Separator rules for properties: no leading whitespace, exactly three hyphens, and the lines immediately before and after must not use the same comment prefix.

Activation properties (`spring.config.activate.*`):
- `on-profile`: a profile expression that must match, or a list of expressions of which at least one must match.
- `on-cloud-platform`: the `CloudPlatform` that must be detected.

Example: second document active only on Kubernetes and only with profile `prod` or `staging`:
```yaml
myprop:
  "always-set"
---
spring:
  config:
    activate:
      on-cloud-platform: "kubernetes"
      on-profile: "prod | staging"
myotherprop: "sometimes-set"
```
Multi-document files cannot be loaded with `@PropertySource` or `@TestPropertySource`.

## Checked

2026-11-07. Read features/profiles.html and features/external-config.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
