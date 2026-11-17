---
id: computing-software.software-engineering.groovy.groovy-modules-packaging
name: groovy-modules-packaging
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, groovy-modules-packaging]
level: advanced
status: draft
description: "Groovy modules in the distribution, building a jar, compiling scripts to classes and shipping a runnable fat jar."
sources:
  - https://groovy-lang.org/download.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Modules, packaging and scripts to jars
- Modules: `groovy` core, `groovy-xml`, `groovy-json`, `groovy-sql`, `groovy-templates`, `groovy-test`, `groovy-datetime`, `groovy-console`, `groovy-groovysh`, `groovy-yaml`, `groovy-toml`, `groovy-cli-picocli`.
- Compile scripts: `groovyc -d out Script.groovy` creates `Script.class` with a `main`; run `java -cp out:groovy.jar Script`.
- Fat jar via Gradle (`shadow` plugin) or Maven shade; include required `groovy-*` module jars and keep `META-INF/services` and extension descriptors (merge them).
- Reproducibility: a fixed `@Grab` set vs a built jar.

## Gotchas
- Shading drops or overwrites `META-INF/groovy/org.codehaus.groovy.runtime.ExtensionModule` unless merged.
- Classpath separator is `;` on Windows and `:` elsewhere.

## Self-check
Compile a script, run it with `java -cp`, and confirm output.
