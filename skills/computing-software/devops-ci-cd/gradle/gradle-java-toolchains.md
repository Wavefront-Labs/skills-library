---
id: computing-software.devops-ci-cd.gradle.gradle-java-toolchains
name: gradle-java-toolchains
category: computing-software
field: devops-ci-cd
product: gradle
tags: [java-toolchains, language-version, foojay, jdk-auto-download, jvm-detection]
level: practitioner
status: docs-checked
description: "Pin the JDK a Gradle build uses with the toolchain spec, auto-provisioning, the Foojay resolver and JVM detection rules."
sources: ["https://docs.gradle.org/current/userguide/toolchains.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle java toolchains

Declare the toolchain:

```kotlin
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(11)
        vendor = JvmVendorSpec.ADOPTIUM
    }
}
```

Other options: `JvmVendorSpec.matching("customString")` (case-insensitive match on `java.vendor`), `implementation = JvmImplementation.J9`, and `nativeImageCapable = true`. A vendor or implementation requires `languageVersion`; invalid specs fail the build since Gradle 8.0.

Auto-provisioning: Gradle downloads a matching JDK only when no local toolchain matches and a download repository is configured. Downloads go to `/jdks` under Gradle User Home, only GA releases are fetched and existing JDKs are never updated. Turn it off with `org.gradle.java.installations.auto-download=false`. Add the Foojay resolver in settings:

```kotlin
plugins {
    id("org.gradle.toolchains.foojay-resolver-convention").version("1.0.0")
}
```

or declare `toolchainManagement { jvm { javaRepositories { repository("foojay") { resolverClass = org.gradle.toolchains.foojay.FoojayToolchainResolver::class.java } } } }`. Repositories are tried in declaration order.

Detection looks at OS-specific locations, `JAVA_HOME`, asdf-vm, Jabba, SDKMAN!, Maven toolchains and IntelliJ IDEA installs. Disable with `org.gradle.java.installations.auto-detect=false`. Extend with `org.gradle.java.installations.fromEnv=JDK8,JRE17` and `org.gradle.java.installations.paths=/custom/path/jdk1.8`.

By default Gradle prefers installed JDKs over JREs when both satisfy the requirements.

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: the match-sorting order (vendor ranking, major, minor, path), which is not on the page.
Method: documentation only; no commands were run.
