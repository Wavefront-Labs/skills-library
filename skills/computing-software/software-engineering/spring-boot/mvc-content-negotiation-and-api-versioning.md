---
id: computing-software.software-engineering.spring-boot.mvc-content-negotiation-and-api-versioning
name: mvc-content-negotiation-and-api-versioning
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, spring-mvc, content-negotiation, api-versioning, favor-parameter, pathpatternparser, spring-mvc-apiversion]
level: practitioner
status: docs-checked
description: "Configure MVC content negotiation by query parameter and media types, path matching defaults, and API versioning via spring.mvc.apiversion properties."
sources:
  - https://docs.spring.io/spring-boot/reference/web/servlet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Suffix pattern matching is disabled by default, so `GET /projects/spring-boot.json` does not match `@GetMapping("/projects/spring-boot")`. Use a query parameter instead:
```yaml
spring:
  mvc:
    contentnegotiation:
      favor-parameter: true
      parameter-name: "myparam"
```
`favor-parameter: true` alone makes `?format=json` work; `parameter-name` renames it. Add media types:
```yaml
spring:
  mvc:
    contentnegotiation:
      media-types:
        markdown: "text/markdown"
```
Boot uses `PathPatternParser` for path matching: optimized but restricts some path pattern variants, and incompatible with a DispatcherServlet path prefix (`spring.mvc.servlet.path`).

API versioning: the same `@Controller` path can be mapped several times for different versions. Then configure how the version arrives (header, query parameter, media type parameter, or path), either with a `WebMvcConfigurer` overriding `configureApiVersioning(...)` or properties:
```yaml
spring:
  mvc:
    apiversion:
      default: 1.0.0
      use:
        header: X-Version
```
This reads `X-Version` and defaults to `1.0.0` when absent. If multiple strategies are needed (for example header and query parameter), declare the order programmatically in `configureApiVersioning`. For fuller control define `ApiVersionResolver`, `ApiVersionParser` and `ApiVersionDeprecationHandler` beans; they are injected into the auto-configured MVC setup. `WebClient` and `RestClient` support API versioning too.

Other beans: a `ConfigurableWebBindingInitializer` bean you define is used for `WebDataBinder` initialization.

## Checked

2026-11-07. Read web/servlet.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
