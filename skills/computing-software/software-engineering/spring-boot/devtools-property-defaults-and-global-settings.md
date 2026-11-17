---
id: computing-software.software-engineering.spring-boot.devtools-property-defaults-and-global-settings
name: devtools-property-defaults-and-global-settings
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, devtools, property-defaults, livereload, global-settings, spring-boot-devtools-properties]
level: practitioner
status: docs-checked
description: "Devtools development-time property defaults (caches off), web debug logging, deprecated LiveReload and global devtools settings in $HOME/.config/spring-boot."
sources:
  - https://docs.spring.io/spring-boot/reference/using/devtools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Property defaults: libraries cache for performance (template engines cache compiled templates, Spring MVC adds HTTP caching headers to static resources), which hinders development. `spring-boot-devtools` disables cache options by default and also adjusts tracing probability for development (the page says the default probability may not log all traces used for testing). Opt out with `spring.devtools.add-properties: false` in `application.properties`. (The full applied-property table is a generated partial that is not in the docs repo and was not read, so no individual default beyond those named here is claimed.)

Web debugging: devtools suggests `DEBUG` logging for the `web` logging group to see the request, handler and response outcome. To log all request details including potentially sensitive information, set `spring.mvc.log-request-details` or `spring.http.codecs.log-request-details`.

LiveReload: deprecated as of Spring Boot 4.1.0 with no replacement. An embedded LiveReload server triggers a browser refresh on resource change (extensions exist for Chrome, Firefox, Safari). Start it with `spring.devtools.livereload.enabled=true`. Only one LiveReload server can run at a time (with several apps from an IDE only the first gets it), and automatic restart must be enabled to trigger it.

Global settings: put any of these in `$HOME/.config/spring-boot`, applying to all devtools-using applications on the machine:
1. `spring-boot-devtools.properties`
2. `spring-boot-devtools.yaml`
3. `spring-boot-devtools.yml`
```yaml
spring:
  devtools:
    restart:
      trigger-file: ".reloadtrigger"
```
Change `$HOME` with the `SPRING_DEVTOOLS_HOME` environment variable or `spring.devtools.home` system property. If none is found there, the root of `$HOME` is searched for `.spring-boot-devtools.properties` (shares config with older Boot versions). Profiles are not supported in these files: no `spring-boot-devtools-<profile>.properties` filenames, no `spring.config.activate.on-profile` documents, and profiles activated there do not affect profile-specific files.

## Checked

2026-11-07

Read devtools.adoc (docs-repo source of the cited Developer Tools page) in full (448 lines), using Property Defaults, LiveReload, Global Settings and Configuring File System Watcher. The devtools-property-defaults partial (the table of applied properties) is generated at build time, is not in the docs repo clone and was not read.
Confirmed: caching rationale (template engines, Spring MVC static-resource headers); caches disabled by default; spring.devtools.add-properties false; DEBUG for the web group and the spring.mvc.log-request-details / spring.http.codecs.log-request-details properties; LiveReload deprecated as of Spring Boot 4.1.0 with no replacement, embedded server, Chrome/Firefox/Safari extensions, spring.devtools.livereload.enabled, one server at a time, restart must be enabled; the three global files in $HOME/.config/spring-boot, trigger-file example, SPRING_DEVTOOLS_HOME and spring.devtools.home, the .spring-boot-devtools.properties fallback in $HOME, and the profiles-not-supported NOTE.
Trimmed: "sets tracing probability to 100%" replaced by the page's more careful wording, since the page sentence is ambiguous and the table that would settle it was not readable.

Method: documentation only; no commands were run.
