---
id: computing-software.software-engineering.spring-boot.mvc-static-content-and-welcome-page
name: mvc-static-content-and-welcome-page
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, static-resources, webjars, cache-busting, welcome-page, favicon, spring-web-resources]
level: practitioner
status: docs-checked
description: "Serve static content from /static, /public, /resources, move it with spring.mvc.static-path-pattern, use WebJars, cache busting, welcome page and favicon."
sources:
  - https://docs.spring.io/spring-boot/reference/web/servlet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default static locations on the classpath: `/static`, `/public`, `/resources`, `/META-INF/resources`, plus the ServletContext root. Boot uses Spring MVC's `ResourceHttpRequestHandler`; override `addResourceHandlers` in a `WebMvcConfigurer` to change it.

- The container's default servlet is off in a stand-alone web app; enable with `server.servlet.register-default-servlet`. It is only a fallback.
- Resources map to `/**`. Relocate with `spring.mvc.static-path-pattern: "/resources/**"`.
- Replace locations with `spring.web.resources.static-locations`; the root servlet context path `/` is automatically added as a location as well.
- WebJars are served from `/webjars/**` (change with `spring.mvc.webjars-path-pattern`). Add `org.webjars:webjars-locator-lite` for version-agnostic URLs: `/webjars/jquery/jquery.min.js` resolves to `/webjars/jquery/x.y.z/jquery.min.js`.
- Do not use `src/main/webapp` for jar packaging; it works only with war and is silently ignored for jars.

Cache busting with a content hash for everything:
```yaml
spring:
  web:
    resources:
      chain:
        strategy:
          content:
            enabled: true
            paths: "/**"
```
Add a fixed version for module-loader paths: under `strategy.fixed` set `enabled: true`, `paths: "/js/lib/"`, `version: "v12"` giving `/v12/js/lib/mymodule.js`. Links are rewritten by `ResourceUrlEncodingFilter`, auto-configured for Thymeleaf and FreeMarker; declare it manually for JSPs. Other engines need template helpers using `ResourceUrlProvider`.

Welcome page: Boot looks for `index.html` in static locations, then an `index` template. It is a fallback after `RouterFunctionMapping`, then `RequestMappingHandlerMapping`, then `WelcomePageHandlerMapping`.

Favicon: a `favicon.ico` in the static locations is used automatically.

No-handler behaviour: Spring MVC throws `NoHandlerFoundException` when no handler is found, but static content mapped to `/**` provides a handler for all requests, so if no static content is available `ResourceHttpRequestHandler` throws `NoResourceFoundException`. For `NoHandlerFoundException` to be thrown, set `spring.mvc.static-path-pattern` to a more specific value such as `/resources/**` or set `spring.web.resources.add-mappings` to `false`.

## Checked

2026-11-07. Read web/servlet.html (static content, welcome page, favicon, path matching) in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. Reworded the root-location line (the root servlet context path is automatically added) and the no-handler paragraph to match the page. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
