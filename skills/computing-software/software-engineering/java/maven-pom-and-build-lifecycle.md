---
id: computing-software.software-engineering.java.maven-pom-and-build-lifecycle
name: maven-pom-and-build-lifecycle
category: computing-software
field: software-engineering
product: java
tags: [java, java-build, maven, maven-lifecycle, pom-xml, plugins, multi-module, maven-wrapper]
level: practitioner
status: docs-checked
description: "Structure Maven builds: POM essentials, lifecycle phases and plugin bindings, multi-module reactors, wrapper, reproducible builds and the commands that matter."
sources:
  - https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html
  - https://maven.apache.org/pom.html
  - https://maven.apache.org/guides/mini/guide-multiple-modules.html
  - https://maven.apache.org/guides/mini/guide-reproducible-builds.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Maven POM and build lifecycle

**Goal:** a Maven build that is fast, reproducible, and behaves the same on every machine and CI.

## 1. Lifecycle and phases
Default lifecycle (each phase runs all earlier ones): `validate -> compile -> test -> package -> verify -> install -> deploy`. Plugins bind **goals** to phases (`maven-compiler-plugin:compile` at `compile`, `surefire:test` at `test`, `failsafe:integration-test` + `failsafe:verify` around `verify`).
```bash
./mvnw verify                 # what CI should run: unit + integration tests, checks
```
Do not call `integration-test` directly from the command line: Failsafe and container plugins need `verify` to
produce reports and shut the test environment down. `install` copies the package to the local repository for use
by other local projects; `deploy` copies it to the remote repository.

## 2. Minimal modern POM
```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.acme</groupId><artifactId>orders</artifactId><version>1.4.0-SNAPSHOT</version>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.build.outputTimestamp>2026-01-01T00:00:00Z</project.build.outputTimestamp>
  </properties>
  <build>
    <pluginManagement>
      <plugins>
        <plugin><artifactId>maven-surefire-plugin</artifactId><version>CURRENT_VERSION</version></plugin>
        <plugin><artifactId>maven-failsafe-plugin</artifactId><version>CURRENT_VERSION</version></plugin>
      </plugins>
    </pluginManagement>
  </build>
</project>
```
- Pin every plugin version in `pluginManagement`; replace `CURRENT_VERSION` with the release you have verified.
  Reproducible builds need plugin versions that support it (`mvn artifact:check-buildplan` lists the upgrades).
- `project.build.outputTimestamp` enables Reproducible Builds mode for plugins; it is active by default from Maven
  3.10.0 and 4.0.0-beta-5 (MNG-8258), and setting it overrides the inherited default.
- Check reproducibility with `mvn clean install` then `mvn clean verify artifact:compare`; this local test does not
  rule out environment leaks such as username or directory.

## 3. Multi-module layout
Parent POM (`<packaging>pom</packaging>`) holds `<modules>`, `pluginManagement`, `dependencyManagement`; children declare `<parent>` and only what they use. Keep the parent as an aggregator and parent at once for small projects; split them in large orgs.

## 4. Wrapper and enforcer
Commit the Maven wrapper (`mvnw`, `.mvn/wrapper`) so every machine and CI uses the same Maven version, and use the
Maven Enforcer plugin to fail builds on rule violations. Check the plugin documentation for rule names.

## Gotchas
- SNAPSHOT dependencies make builds non-reproducible; forbid them in releases.
- Profiles activated by environment differ between laptop and CI; print them with `help:active-profiles`.

## Checked
2026-11-01. Confirmed against Maven guides (Introduction to the Build Lifecycle, POM reference, Guide to Working
with Multiple Modules, Configuring for Reproducible Builds): default lifecycle phase order, compiler:compile and
surefire:test bindings, Failsafe on integration-test and verify, modelVersion 4.0.0, packaging pom,
outputTimestamp, artifact:check-buildplan and artifact:compare, MNG-8258 default. Removed: -pl/-am/-T/-o flags,
wrapper version, Enforcer rule names, maven.compiler.release note, skipTests semantics, maven.config note,
plugin version numbers.
Method: documentation only; no commands were run.

## Verify
- `./mvnw -B verify` passes from a clean clone with an empty `~/.m2`, and two builds produce identical jar checksums.
