---
id: computing-software.devops-ci-cd.gradle.gradle-wrapper-generation-and-upgrade
name: gradle-wrapper-generation-and-upgrade
category: computing-software
field: devops-ci-cd
product: gradle
tags: [gradle-wrapper, distribution-url, checksum, gradlew, wrapper-properties]
level: practitioner
status: docs-checked
description: "Generate, pin, verify and upgrade the Gradle Wrapper and know which files to commit."
sources: ["https://docs.gradle.org/current/userguide/gradle_wrapper.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle wrapper generation and upgrade

Generate or upgrade from the project root:

```bash
gradle :wrapper
gradle :wrapper --gradle-version 9.8.2 --distribution-type all
./gradlew :wrapper --gradle-version latest
./gradlew --version
```

`--gradle-version` accepts an exact `X.Y.Z`, a major or minor for Gradle 9 and later (for example `9` or `9.1`, resolving to the latest matching release), or a label such as `latest`. `--distribution-type` is `bin` (default, recommended for most builds) or `all`. Other flags: `--network-timeout` (ms, default 10000), `--gradle-distribution-sha256-sum`, `--retries` (default 0), `--retry-back-off-ms` (default 500), and `--validate-url` (on by default; `--no-validate-url` turns it off; https URLs get a HEAD request).

`gradle/wrapper/gradle-wrapper.properties` keys:

```properties
distributionUrl=https\://services.gradle.org/distributions/gradle-9.8.2-bin.zip
distributionSha256Sum=<sha256 of the distribution>
retries=3
retryBackOffMs=1000
```

`distributionSha256Sum` is checked only if the distribution is not already downloaded; a mismatch fails the build.

Upgrading: prefer running `:wrapper` with the target version. Running it once updates only the properties file; run it a second time to refresh `gradle-wrapper.jar`, `gradlew` and `gradlew.bat`. Editing `distributionUrl` by hand works, but since Gradle 9.0.0 the version there must be `X.Y.Z`.

Commit `gradle/wrapper/gradle-wrapper.jar`, `gradle/wrapper/gradle-wrapper.properties`, `gradlew` and `gradlew.bat`; the JAR is small and committing it is expected.

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: nothing; clarified that major or minor only versions apply to Gradle 9 and later.
Method: documentation only; no commands were run.
