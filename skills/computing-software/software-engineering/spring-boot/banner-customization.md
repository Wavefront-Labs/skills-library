---
id: computing-software.software-engineering.spring-boot.banner-customization
name: banner-customization
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, banner, banner-txt, spring-banner-location, banner-mode, ansi]
level: intro
status: docs-checked
description: "Change the Spring Boot startup banner with banner.txt, spring.banner.location, variables like application.version, banner-mode and a programmatic Banner."
sources:
  - https://docs.spring.io/spring-boot/reference/features/spring-application.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replace the banner by adding `banner.txt` to the classpath or setting `spring.banner.location`. For a non-UTF-8 file set `spring.banner.charset`.

Inside `banner.txt` you can use any Environment key plus:
- `${application.version}`: version from `MANIFEST.MF` (`Implementation-Version: 1.0` prints `1.0`)
- `${application.formatted-version}`: formatted, such as `(v1.0)`
- `${spring-boot.version}`: the Spring Boot version
- `${spring-boot.formatted-version}`: formatted with brackets and a `v` prefix
- `${Ansi.NAME}` (also `${AnsiColor.NAME}`, `${AnsiBackground.NAME}`, `${AnsiStyle.NAME}`): an ANSI escape code by name
- `${application.title}`: `Implementation-Title` from `MANIFEST.MF`

Programmatic: `SpringApplication.setBanner(...)` with your own `Banner` implementation and `printBanner()`.

`spring.main.banner-mode` chooses where it goes: `console` (System.out), `log` (the configured logger) or `off`. The printed banner is registered as a singleton bean named `springBootBanner`.

The `application.title`, `application.version` and `application.formatted-version` properties are only available when launching with `java -jar` or `java -cp` using Spring Boot launchers. They do not resolve for an unpacked jar started via `java -cp <classpath> <mainclass>` or a native image. Launch a packed jar with `java -jar`, or an unpacked one with `java org.springframework.boot.loader.launch.JarLauncher`.

Turning the banner off in code: create a local `SpringApplication` instance and customize it (see springapplication-customization).

## Checked

2026-11-07

Read spring-application.adoc in full (cited SpringApplication page), focusing on Customizing the Banner and Customizing SpringApplication. The MyApplication include example was not opened.
Confirmed: banner.txt on the classpath or spring.banner.location; spring.banner.charset for non-UTF-8; every variable in the Banner variables table (application.version, application.formatted-version, spring-boot.version, spring-boot.formatted-version, Ansi/AnsiColor/AnsiBackground/AnsiStyle NAME, application.title) with the MANIFEST.MF examples; setBanner(...) with the Banner interface and printBanner(); spring.main.banner-mode values console, log, off; springBootBanner singleton bean; the java -jar / java -cp launcher caveat, unpacked-jar and native-image caveats, and JarLauncher advice.
Nothing trimmed.

Method: documentation only; no commands were run.
