---
id: computing-software.software-engineering.spring-boot.logging-defaults-and-console
name: logging-defaults-and-console
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, logging, logback, console-output, debug-mode, ansi-color, log-format]
level: intro
status: docs-checked
description: "Default Spring Boot logging with Logback, the log line fields, --debug and --trace modes, disabling console logging and ANSI color settings."
sources:
  - https://docs.spring.io/spring-boot/reference/features/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Boot uses Commons Logging internally and leaves the implementation open; defaults exist for Java Util Logging, Log4j2 and Logback. With the starters, Logback is used. In a servlet container or application server, Java Util Logging output is not routed into your application's logs.

Default line fields: date and time (milliseconds), level (ERROR, WARN, INFO, DEBUG, TRACE; Logback maps FATAL to ERROR), process ID, a `---` separator, application name in brackets (only if `spring.application.name` is set), application group in brackets (only if `spring.application.group` is set), thread name, correlation ID (if tracing is enabled), logger name, message. Hide the name or group with `logging.include-application-name=false` or `logging.include-application-group=false`.

Console output logs ERROR, WARN and INFO by default.
- `java -jar myapp.jar --debug` (or `debug=true` in application.properties) turns more output on for core loggers (embedded container, Hibernate, Spring Boot). It does not log everything at DEBUG.
- `--trace` (or `trace=true`) enables trace for core loggers (embedded container, Hibernate schema generation, the Spring portfolio).
- `logging.console.enabled=false` disables console logging.

Color: used when the terminal supports ANSI; override detection with `spring.output.ansi.enabled`. Use the `%clr` conversion word, for example `%clr(%5p)` colors by level (FATAL and ERROR red, WARN yellow, INFO, DEBUG and TRACE green). Pass options such as `%clr(%d{yyyy-MM-dd'T'HH:mm:ss.SSSXXX}){yellow,bold}`.
- Text colors: black, blue, cyan, green, magenta, red, white, yellow and their `bright_` forms.
- Backgrounds: `bg_` plus those color names.
- Styles: bold, faint, italic, normal, reverse, underline.

## Checked

2026-11-07

Read logging.adoc (docs-repo source of the cited Logging page) in full (935 lines), using the intro, Log Format, Console Output and Color-coded Output sections. The embedded sample partial (logging-format.txt) was not opened.
Confirmed: Commons Logging with Java Util Logging, Log4j2 and Logback defaults and Logback with the starters; the servlet-container Java Util Logging TIP; the field list (date/time, level, process ID, ---, application name and group only when set, thread name, correlation ID if tracing, logger name, message); Logback FATAL mapped to ERROR; logging.include-application-name / -group false; ERROR, WARN, INFO by default; --debug / debug=true and --trace / trace=true with their core-logger lists and the "does not log everything at DEBUG" note; logging.console.enabled; ANSI detection with spring.output.ansi.enabled; %clr(%5p) level-colour table; the yellow,bold example; every supported text colour, background colour and style.
Nothing trimmed.

Method: documentation only; no commands were run.
