---
id: computing-software.software-engineering.java.static-analysis-with-errorprone-and-spotbugs
name: static-analysis-with-errorprone-and-spotbugs
category: computing-software
field: software-engineering
product: java
tags: [java, java-code-quality, errorprone-spotbugs, error-prone, spotbugs, nullaway, static-analysis]
level: practitioner
status: docs-checked
description: "Catch Java bugs at build time with Error Prone (javac plugin) and SpotBugs (bytecode): Maven setup, JDK module flags, NullAway, Find Security Bugs, adoption."
sources: ["https://errorprone.info/docs/installation", "https://spotbugs.readthedocs.io/en/latest/maven.html", "https://github.com/uber/NullAway"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error Prone and SpotBugs

## Error Prone (compile time, javac plugin)
Error Prone must run on JDK 21 or newer (it can still build Java 8 code with the right `-source`/`-target`/`-bootclasspath` or `--release` flags). Older JDKs need older unmaintained releases: 2.10.0 is the last for JDK 8, 2.31.0 for JDK 11, 2.42.0 for JDK 17.

Maven, in `maven-compiler-plugin` configuration:
```xml
<compilerArgs>
  <arg>-XDcompilePolicy=simple</arg>
  <arg>--should-stop=ifError=FLOW</arg>
  <arg>-Xplugin:ErrorProne</arg>
</compilerArgs>
<annotationProcessorPaths>
  <path><groupId>com.google.errorprone</groupId><artifactId>error_prone_core</artifactId><version>${error-prone.version}</version></path>
</annotationProcessorPaths>
```
- JEP 396 (strong encapsulation of JDK internals) requires `--add-exports` for the `jdk.compiler` javac packages (api, file, main, model, parser, processing, tree, util) and `--add-opens` for `code` and `comp`. If the compiler plugin forks or uses toolchains, pass them as `-J--add-exports=...` under `compilerArgs`; otherwise put them in `.mvn/jvm.config`. The install page lists the full set.
- The installation page notes `-XDaddTypeAnnotationsToSymbol=true` is needed only when building with JDK 21.
- Setting `annotationProcessorPaths` stops javac scanning the classpath for processors, so add other processors (for example AutoValue) to that list too.
- Gradle is covered by an external contribution (tbroyer/gradle-errorprone-plugin). On the command line use `-processorpath` plus `-Xplugin:ErrorProne`, with options such as `-XepDisableAllChecks -Xep:CollectionIncompatibleType:ERROR` inside the plugin string. Check severity is raised with `-Xep:Name:ERROR`.
- **NullAway** is an Error Prone check: enable it as an ERROR check and tell it which packages to treat as annotated (`-XepOpt:NullAway:AnnotatedPackages=...`, or `option("NullAway:AnnotatedPackages", "com.uber")` in the Gradle plugin DSL). Any `@Nullable` annotation works (JSpecify, AndroidX, JetBrains). To try NullAway alone, disable all other checks.

## SpotBugs (bytecode analysis)
Add `spotbugs-maven-plugin` to the `pom.xml`. Goals: `spotbugs` analyses, `check` analyses and fails the build if bugs are found, `gui` opens the result viewer, `help` shows usage.

Find Security Bugs is a SpotBugs plugin for security audits of web and Android apps (SQL/HQL, command and XPath injection, weak cryptography). Register it under `<plugins>` in the plugin configuration with groupId `com.h3xstream.findsecbugs` and artifactId `findsecbugs-plugin`; an include filter matching `<Bug category="SECURITY"/>` limits reports to security findings.

## Adoption strategy
1. Turn on with warnings only; record the baseline.
2. Fix categories one by one and raise each to ERROR so it cannot regress.
3. Run Error Prone on every build and SpotBugs `check` in CI.

## Verify
Add a deliberate bug (for example `new Exception();` without `throw`, flagged as DeadException) and confirm the build fails; remove it.

## Checked
Read the Error Prone installation page in full, the SpotBugs Maven page in full and the NullAway README. Removed as unconfirmed: the SpotBugs effort and threshold settings, the exclude-file and `@SuppressFBWarnings` snippets, Lombok ordering advice, the three-level check severity description, `@SuppressWarnings` suppression advice and the claim of which checks run per build cost.
Method: docs-checked 2026-11-09 against the Error Prone installation page, the SpotBugs Maven plugin page and the NullAway README.
