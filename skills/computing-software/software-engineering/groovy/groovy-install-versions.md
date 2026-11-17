---
id: computing-software.software-engineering.groovy.groovy-install-versions
name: groovy-install-versions
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, groovy-install-versions, groovy-install]
level: intro
status: draft
description: "Install Groovy via SDKMAN or the distribution zip; supported JDK pairing; the org.apache.groovy coordinates."
sources:
  - https://groovy-lang.org/download.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Installing Groovy and picking a version
- SDKMAN: `sdk install groovy` / `sdk use groovy <version>` / `sdk default groovy`.
- Distribution zip: unpack, set `GROOVY_HOME`, add `bin` to `PATH`.
- Maven coordinates: `org.apache.groovy:groovy` (4.x and later), modules such as `groovy-json`, `groovy-sql`, `groovy-xml`, `groovy-test`; `groovy-all` is a POM aggregate.
- Check JDK support in the release notes for your Groovy version (unconfirmed which JDK each version supports).
- Wrapper-style reproducibility: pin `groovy` in Gradle/Maven rather than relying on system Groovy.

## Gotchas
- `groovy` on PATH may be older than the build's Groovy.
- Groovy 3 to 4 renamed packages in some modules and the group id: audit imports.

## Self-check
`groovy --version` and `java -version` show the expected pairing.
