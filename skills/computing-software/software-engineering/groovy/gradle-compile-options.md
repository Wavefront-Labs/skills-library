---
id: computing-software.software-engineering.groovy.gradle-compile-options
name: gradle-compile-options
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, gradle-compile-options]
level: advanced
status: docs-checked
description: "Configure GroovyCompile from Gradle: incremental compilation, compilation avoidance, AST transformation classpath and indy options."
sources:
  - https://docs.gradle.org/current/userguide/groovy_plugin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GroovyCompile options and compiler configuration
The Groovy plugin adds a `GroovyCompile` task per source set. It supports most options of the official Groovy compiler and can use Java toolchains (`javaLauncher`). Configure all of them together:

```groovy
tasks.withType(GroovyCompile).configureEach {
  options.incremental = true
  options.incrementalAfterFailure = true
}
```

- Incremental Groovy compilation is experimental (since Gradle 5.6). It needs Groovy compilation avoidance enabled first, via `enableFeaturePreview('GROOVY_COMPILATION_AVOIDANCE')` in `settings.gradle`, plus the options above.
- Compilation avoidance is incubating; the page warns of known inaccuracies. If a dependent project changes in an ABI-compatible way, dependent Groovy compile tasks stay up to date.
- AST transformations must be declared separately on `astTransformationClasspath`: create a configuration, depend on the transformation project, and add it with `astTransformationClasspath.from(...)`.
- Groovy 6 and later: setting `groovyOptions.optimizationOptions.all = false` or `.indy = false` switches to classic call-site bytecode generation, which needs the `org.apache.groovy:groovy-callsite` module (same version as Groovy) on the compile and runtime classpath; a `compileOnly` dependency is not enough.
- `GroovyCompile` defaults: `classpath` is the source set compile classpath, `source` is `sourceSet.groovy`, `groovyClasspath` is the `groovy` configuration if non-empty.

## Gotchas
- Changes to resources do not trigger recompilation, which can be wrong for extension modules.
- Source-retention annotation changes do not trigger full recompilation, because the Groovy compiler does not keep `@Retention` in generated annotation bytecode (all are RUNTIME).

## Self-check
After enabling both settings, change one Groovy file and confirm only affected classes are recompiled.

## Checked
2026-11-09. Rewritten around what the Gradle Groovy plugin page states (GroovyCompile defaults, toolchains, compilation avoidance, incremental compilation, astTransformationClasspath, Groovy 6 indy and groovy-callsite, known issues). Removed unconfirmed claims: `options.encoding`, `groovyOptions.parameters`, `configurationScript`/`CompilerConfiguration` global `@CompileStatic`, `fork`/`forkOptions` memory settings and the `-Xlint` example.
Method: documentation only; no commands were run.
