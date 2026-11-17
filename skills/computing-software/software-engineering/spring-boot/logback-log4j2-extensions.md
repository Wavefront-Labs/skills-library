---
id: computing-software.software-engineering.spring-boot.logback-log4j2-extensions
name: logback-log4j2-extensions
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, logging, springprofile, springproperty, logback-spring-xml, log4j2-spring-xml, lookups]
level: practitioner
status: docs-checked
description: "Use springProfile, springProperty and Log4j2 SpringProfile and spring: lookups in logback-spring.xml or log4j2-spring.xml for profile and Environment aware logging."
sources:
  - https://docs.spring.io/spring-boot/reference/features/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Extensions work only in `logback-spring.xml` / `log4j2-spring.xml` (or a file named via `logging.config`), because plain `logback.xml` / `log4j2.xml` load too early. Logback extensions cannot be used with Logback configuration scanning; changing the file then logs "no applicable action for [springProperty]" errors.

Logback profile sections (anywhere within `<configuration>`):
```xml
<springProfile name="staging"> ... </springProfile>
<springProfile name="dev | staging"> ... </springProfile>
<springProfile name="!production"> ... </springProfile>
```
`name` takes a profile name or an expression such as `production & (eu-central | eu-west)`.

Logback Environment properties:
```xml
<springProperty scope="context" name="fluentHost" source="myapp.fluentd.host"
		defaultValue="localhost"/>
```
`source` is read from the Spring Environment and must be kebab case; `scope` stores it elsewhere than local; `defaultValue` is the fallback. Then use `${fluentHost}`.

Log4j2: use the `<SpringProfile name="...">` tag (same name/expression rules, anywhere within `<Configuration>`). Do not include `org.apache.logging.log4j:log4j-spring-boot` in the build, since Boot's extensions supersede it.

Log4j2 Environment lookups use the `spring:` prefix with a kebab-case key:
```xml
<Properties>
	<Property name="applicationName">${spring:spring.application.name}</Property>
</Properties>
```

Log4j2 system properties loaded after Log4j2 initialization can be set in the Environment, for example `log4j2.skipJansi=false` in `application.properties`. The Environment is consulted only when system properties and OS environment variables lack the value. Properties read during early initialization cannot reference the Environment.

## Checked

2026-11-07

Read logging.adoc (docs-repo source of the cited Logging page) in full (935 lines), using the Logback Extensions and Log4j2 Extensions sections (including the Log4j2 System Properties part).
Confirmed: extensions need logback-spring.xml / log4j2-spring.xml or a logging.config property; incompatibility with Logback autoScan and the quoted "no applicable action for [springProperty]" error; springProfile placement, name as profile or expression, the three sample forms; springProperty scope, source (kebab case), defaultValue and the fluentHost example; SpringProfile for Log4j2; the log4j-spring-boot exclusion; spring: lookups with kebab-case keys and the applicationName example; log4j2.skipJansi=false in application.properties; Environment consulted only when system properties and OS environment lack the value; early-initialization properties cannot reference the Environment.
Nothing trimmed.

Method: documentation only; no commands were run.
