---
id: computing-software.software-engineering.java.formatting-with-spotless-and-checkstyle
name: formatting-with-spotless-and-checkstyle
category: computing-software
field: software-engineering
product: java
tags: [java, java-code-quality, spotless-checkstyle, spotless, checkstyle, google-java-format, ratchetfrom]
level: practitioner
status: docs-checked
description: "Enforce Java code style with the Spotless Maven plugin (google-java-format, import order, license header, ratchetFrom) and Checkstyle configuration modules."
sources: ["https://github.com/diffplug/spotless/tree/main/plugin-maven", "https://checkstyle.org/config.html", "https://github.com/google/google-java-format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spotless and Checkstyle

Spotless formats and fixes files; Checkstyle reports violations of configured rules. Use both, and keep their rules from contradicting each other.

## Spotless (Maven)
```xml
<plugin>
  <groupId>com.diffplug.spotless</groupId>
  <artifactId>spotless-maven-plugin</artifactId>
  <version>${spotless.version}</version>
  <configuration>
    <ratchetFrom>origin/main</ratchetFrom>
    <java>
      <googleJavaFormat><version>...</version></googleJavaFormat>
      <removeUnusedImports/>
      <importOrder/>
      <licenseHeader><file>${project.basedir}/license-header</file></licenseHeader>
    </java>
  </configuration>
</plugin>
```
- `mvn spotless:check` reports violations and tells you to run `mvn spotless:apply`, which fixes them.
- `spotless:check` is bound to the `verify` phase by default, so `mvn verify` runs it; bind it to another phase in an execution if you need it earlier.
- `ratchetFrom` limits enforcement to files changed relative to the named git ref, which makes adopting a formatter on an existing codebase painless.
- Alternatives to google-java-format include `palantirJavaFormat` and `eclipse` (formatter XML); `googleJavaFormat` also takes `style` (for example AOSP), `reflowLongStrings` and `formatJavadoc`.
- The `licenseHeader` accepts `content` (with `$YEAR`) or a `file`.
- google-java-format itself needs a JDK (not a JRE) at least as new as the language level of the code being formatted; on JDK 16+ it needs the JEP 396 `--add-exports` JVM flags listed in its README.

## Checkstyle
Checkstyle reads an XML configuration whose modules form a hierarchy and have properties. The distribution ships sample configurations `sun_checks.xml` (Sun conventions) and `google_checks.xml`; start from one and trim.
- Each module has a `severity` property; the default is `error`. `warning` violations are noted, `ignore` ones are not reported. A property can be left to the build with `${checkstyle.javadoc.severity}`-style placeholders that take a `default`.

## Gotchas
- Pin the formatter version in the build so every developer and CI use the same one.
- Keep only the rules you will enforce.

## Verify
Misindent a file: `spotless:check` fails and `spotless:apply` fixes it.

## Checked
Read the Spotless Maven README (the intro, example configuration and Java sections; grepped for ratchetFrom, goals and steps), the full Checkstyle configuration page and the google-java-format README. Removed as unconfirmed: the maven-checkstyle-plugin snippet and options, Gradle commands, a specific pinned formatter version, git blame-ignore advice, pre-commit and format-on-save advice, and suppression-file claims.
Method: docs-checked 2026-11-09 against the Spotless Maven plugin README, the Checkstyle configuration page and the google-java-format README.
