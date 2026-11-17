---
id: computing-software.software-engineering.spring-boot.mvc-cors-and-template-engines
name: mvc-cors-and-template-engines
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, cors, crossorigin, addcorsmappings, thymeleaf, freemarker, mustache, groovy-templates]
level: intro
status: docs-checked
description: "Configure CORS with @CrossOrigin or a WebMvcConfigurer addCorsMappings bean, and use auto-configured template engines from src/main/resources/templates."
sources:
  - https://docs.spring.io/spring-boot/reference/web/servlet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CORS: Spring MVC has supported CORS since 4.2. Controller method configuration with `@CrossOrigin` needs no special Boot configuration. Global CORS configuration is defined by registering a `WebMvcConfigurer` bean with a customized `addCorsMappings(CorsRegistry)` method.

Template engines: Spring MVC can serve dynamic HTML as well as REST. Boot auto-configures:
- FreeMarker
- Groovy
- Thymeleaf
- Mustache

With the default configuration templates are picked up from `src/main/resources/templates`.

Classpath-order trap: depending on how you run the application, the IDE may order the classpath differently. Running from the IDE's main method differs from running via Maven or Gradle or from the packaged jar, which can cause Boot to fail to find the expected template. If so, reorder the classpath in the IDE to put the module's classes and resources first.

JSPs should be avoided if possible because of known limitations with embedded servlet containers (see embedded-servlet-container-customizing).

Cache-busting link rewriting in templates is done by `ResourceUrlEncodingFilter`, auto-configured for Thymeleaf and FreeMarker (see mvc-static-content-and-welcome-page).

## Checked

2026-11-07. Read web/servlet.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. Trimmed the template-engine list to the engines the page names (Groovy entry corrected). The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
