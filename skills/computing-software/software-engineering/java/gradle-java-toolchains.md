---
id: computing-software.software-engineering.java.gradle-java-toolchains
name: gradle-java-toolchains
category: computing-software
field: software-engineering
product: java
tags: [java, java-gradle, gradle-toolchains, java-toolchain, jvm-vendor, foojay-resolver, auto-provisioning, java-release]
level: practitioner
status: docs-checked
description: "Pin the JDK a Gradle build uses with java.toolchain, enable foojay auto-provisioning, test on other JDKs, and keep it separate from the JDK that runs Gradle."
sources: ["https://docs.gradle.org/current/userguide/toolchains.html", "https://github.com/gradle/foojay-toolchains"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gradle Java toolchains

By default Gradle uses the same Java toolchain to run Gradle and to build JVM projects. Configuring a toolchain decouples the JDK that builds the project (compile, test, javadoc) from the JDK that runs Gradle, for reproducible builds across developer machines and CI.

## Declare
```kotlin
// build.gradle.kts
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
        vendor = JvmVendorSpec.ADOPTIUM            // optional
    }
}
```
Gradle then configures all compile, test and javadoc tasks to use the toolchain, detects locally installed toolchains, picks a matching one (any Java 21 here), and can download one if none matches. A vendor or implementation may only be set together with `languageVersion`; an invalid spec is a build error since Gradle 8.0. For an unlisted vendor use `JvmVendorSpec.matching("customString")` (case-insensitive match on `java.vendor`). `nativeImageCapable = true` requests a GraalVM Native Image capable toolchain.

Toolchains do not stop accidental use of newer APIs. The `--release` flag does that but does not control which JDK is used; combine them:
```kotlin
tasks.withType<JavaCompile>().configureEach { options.release = 11 }
```

## Auto-detection and auto-provisioning
Detection is on by default and covers OS-specific locations, `JAVA_HOME`, asdf-vm, Jabba, SDKMAN!, Maven toolchain specifications and IntelliJ IDEA installations. Turn it off with `org.gradle.java.installations.auto-detect=false`. Extra locations: `org.gradle.java.installations.fromEnv=JDK8,JRE17` and `org.gradle.java.installations.paths=<comma-separated paths>`; these extend, and do not outrank, auto-detected ones.

If nothing matches, Gradle can download a JDK only when a toolchain download repository is configured, for example the Foojay resolver in `settings.gradle.kts`:
```kotlin
plugins { id("org.gradle.toolchains.foojay-resolver-convention").version("<version>") }
```
(the Gradle docs and the plugin README show `1.0.0`; check the current version on the Plugin Portal). Downloaded JDKs go into the Gradle User Home (a `/jdks` directory), only GA releases are downloaded, and auto-provisioning never updates JDKs already installed. Disable downloads with `org.gradle.java.installations.auto-download=false`, then stop the daemon with `./gradlew --stop`. With several repositories declared in `toolchainManagement`, Gradle downloads from the first one that matches.

## Per-task toolchains (e.g. test on another JDK)
```kotlin
tasks.register<Test>("testsOn17") {
    javaLauncher = javaToolchains.launcherFor {
        languageVersion = JavaLanguageVersion.of(17)
    }
}
```
The `javaToolchains` extension provides `JavaCompiler`, `JavaLauncher` (used by `JavaExec` and `Test`) and `JavadocTool`. `./gradlew -q javaToolchains` lists detected toolchains, how each was detected, and whether auto-detection and auto-download are enabled.

## Selection order
Gradle sorts matching installations and picks the first: the installation currently running Gradle, then JDKs over JREs, then vendor priority (ADOPTIUM first, then ADOPTOPENJDK, AMAZON, APPLE, AZUL, BELLSOFT, GRAAL_VM, and so on), then higher major, then higher minor version, then path.

## Gotchas
- `JAVA_HOME` applies globally and cannot give different projects different JDKs; the docs recommend toolchains instead. `sourceCompatibility`/`targetCompatibility` do not guarantee the right JDK.
- Without a toolchain, Gradle may fall back to the IDE's Gradle JVM setting, which can differ per developer.
- Daemons cache toolchain configuration; stop the daemon after changing it.
- The docs discourage multiple toolchains on musl-based systems (most Alpine distributions).

## Verify
`./gradlew -q javaToolchains` lists the pinned JDK; a compile with `options.release` set rejects a newer API.

## Checked
Read the Gradle "Toolchains for JVM projects" page (documents Gradle 9.8.2) and the foojay-toolchains README in full. Removed because neither page states them: the Windows registry/Homebrew detection list, the `~/.gradle/jdks` literal path, Gradle 8.x JDK compatibility, build-cache invalidation by vendor, the Kotlin `jvmToolchain` note, the Windows path advice and the `0.8.0` plugin version.
Method: docs-only read of cited pages, 2026-11-08
