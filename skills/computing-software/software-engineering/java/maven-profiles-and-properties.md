---
id: computing-software.software-engineering.java.maven-profiles-and-properties
name: maven-profiles-and-properties
category: computing-software
field: software-engineering
product: java
tags: [java, maven, maven-profiles, maven-properties, resource-filtering, activation, settings-xml]
level: practitioner
status: docs-checked
description: "Use Maven properties and profiles well: precedence, profile activation (-P, JDK, OS, property, file), resource filtering, and avoiding per-environment artifacts."
sources: ["https://maven.apache.org/guides/introduction/introduction-to-profiles.html", "https://maven.apache.org/pom.html#Properties", "https://maven.apache.org/plugins/maven-resources-plugin/examples/filter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Maven profiles and properties

**Goal:** variant builds (CI-only checks, native image, JDK-specific flags) without
per-environment artifacts or unreadable POMs.

## Properties
```xml
<properties>
  <maven.compiler.release>21</maven.compiler.release>
  <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  <jackson.version>2.17.2</jackson.version>
</properties>
```
Reference as `${jackson.version}`. Built-ins include `${project.version}`, `${project.basedir}` and `${env.NAME}` environment variables (see the POM reference, Properties section).

## Profiles
```xml
<profiles>
  <profile>
    <id>ci</id>
    <activation><property><name>env.CI</name></property></activation>
    <build><plugins>
      <plugin><groupId>org.jacoco</groupId><artifactId>jacoco-maven-plugin</artifactId>...</plugin>
    </plugins></build>
  </profile>
  <profile>
    <id>jdk-23-preview</id>
    <activation><jdk>[23,)</jdk></activation>
    <properties><jdk.newer>true</jdk.newer></properties>
  </profile>
</profiles>
```
Activation options: `-P ci` (explicit), `<activeByDefault>` (deactivated as soon as any other
profile in the POM is activated - surprising; avoid), `<jdk>`, `<os>`, `<property>` (with or
without value, `!name` to negate), `<file><exists>`/`<missing>`.
Deactivate: `-P !ci` (quote in shells: `-P '!ci'`).

## Inspecting
```bash
mvn help:active-profiles
mvn help:effective-pom -P ci > effective.xml     # the POM Maven actually runs
mvn help:evaluate -Dexpression=jackson.version
```

## Resource filtering
```xml
<build><resources>
  <resource><directory>src/main/resources</directory><filtering>true</filtering>
    <includes><include>version.properties</include></includes></resource>
  <resource><directory>src/main/resources</directory><filtering>false</filtering>
    <excludes><exclude>version.properties</exclude></excludes></resource>
</resources></build>
```
Filter only specific files: filtering binaries (fonts, keystores) corrupts them, and
`${...}` in Spring config would be replaced at build time.

## Anti-pattern: dev/test/prod profiles producing different JARs
One artifact should be promoted through environments; inject environment config at runtime
(env vars, Spring profiles, config server). Build-time env profiles break "what we tested is
what we ship".

## settings.xml profiles
Repository mirrors, credentials and per-machine properties belong in `~/.m2/settings.xml`
(servers, mirrors, profiles), never in the POM.

## Checked
2026-10-28: Confirmed in the Maven profiles guide: activeByDefault is deactivated when another profile in the POM is activated, activation by jdk (ranges), property (with ! negation), file exists/missing; POM reference for properties. Removed the property precedence claim, the enablePreview property and the -q -DforceStdout flags (not in fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] `mvn help:effective-pom` reviewed after adding a profile.
- [ ] The same JAR checksum is deployed to every environment.
