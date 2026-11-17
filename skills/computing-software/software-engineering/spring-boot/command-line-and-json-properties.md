---
id: computing-software.software-engineering.spring-boot.command-line-and-json-properties
name: command-line-and-json-properties
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, command-line, spring-application-json, json-properties, environment-prefix, program-arguments]
level: practitioner
status: docs-checked
description: "Pass properties by --option arguments, SPRING_APPLICATION_JSON, spring.application.json or a JNDI variable, and set an environment variable prefix."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Command line: `SpringApplication` converts arguments starting with `--` (for example `--server.port=9000`) into properties in the Environment. They take precedence over file-based sources. Disable with `SpringApplication.setAddCommandLineProperties(false)`.

JSON properties: environment variables and system properties restrict some names, so encode a block as one JSON structure. At startup `spring.application.json` or `SPRING_APPLICATION_JSON` is parsed into the Environment:
```shell
SPRING_APPLICATION_JSON='{"my":{"name":"test"}}' java -jar myapp.jar
java -Dspring.application.json='{"my":{"name":"test"}}' -jar myapp.jar
java -jar myapp.jar --spring.application.json='{"my":{"name":"test"}}'
```
All three give `my.name=test`. On a classic application server a JNDI variable `java:comp/env/spring.application.json` works too.

Gotcha: `null` values in the JSON are added to the property source, but `PropertySourcesPropertyResolver` treats null as missing, so the JSON cannot override a lower-order property with null.

Environment prefix: call `SpringApplication.setEnvironmentPrefix(...)` before running. With prefix `input`, `remote.timeout` resolves as `INPUT_REMOTE_TIMEOUT` in the system environment. The prefix applies only to system environment properties; other sources keep using `remote.timeout`. Useful when several Boot apps share one environment.

## Checked

2026-11-07

Read the Accessing Command Line Properties, JSON Application Properties and Configuring System Environment Properties sections of external-config.adoc (docs-repo source of the cited Externalized Configuration page) plus the property-source order list. The rest of the page was read for contradictions and none found.
Confirmed: -- arguments become Environment properties and "always take precedence over file-based property sources"; setAddCommandLineProperties(false); spring.application.json / SPRING_APPLICATION_JSON parsed at startup; the three launch forms (env var, -D, --argument), with the page showing my.name=test for the env-var form and presenting the other two as the same JSON supplied differently; JNDI java:comp/env/spring.application.json on a classic application server; the null-value NOTE naming PropertySourcesPropertyResolver; setEnvironmentPrefix with the input / remote.timeout / INPUT_REMOTE_TIMEOUT example and the "only system environment properties" NOTE.
Nothing trimmed.

Method: documentation only; no commands were run.
