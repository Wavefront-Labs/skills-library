---
id: computing-software.devops-ci-cd.gradle.gradle-init-scripts
name: gradle-init-scripts
category: computing-software
field: devops-ci-cd
product: gradle
tags: [init-scripts, init-gradle, gradle-user-home, enterprise-repositories, build-listeners]
level: advanced
status: docs-checked
description: "Use Gradle init scripts for machine or organisation level configuration, with their locations, order and caveats."
sources: ["https://docs.gradle.org/current/userguide/init_scripts.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle init scripts

Init scripts run before `settings.gradle(.kts)` and project scripts. All that are found run, in this order:
1. `--init-script` / `-I path/to/init.gradle(.kts)` (repeatable)
2. `GRADLE_USER_HOME/init.gradle(.kts)`
3. `*.init.gradle(.kts)` in `GRADLE_USER_HOME/init.d/` (alphabetical)
4. `*.init.gradle(.kts)` in `GRADLE_HOME/init.d/` (alphabetical)

```bash
./gradlew --init-script init.gradle.kts -q showRepos
```

Use cases: enterprise repositories and plugin resolution rules, environment-specific configuration (dev versus CI), user-specific data such as credentials through providers, machine-specific JDK or SDK paths, and build listeners or custom loggers.

Configure projects with the normal APIs:

```kotlin
allprojects {
    repositories { mavenLocal() }
}
```

Script dependencies go in an `initscript {}` block (project dependencies are not allowed). An init plugin implements `Plugin<Gradle>` and can use callbacks such as `settingsEvaluated {}`, `projectsLoaded {}`, `beforeProject {}` and `afterProject {}`.

Caveats: init scripts affect every build they are attached to, so treat them like production code; they cannot access `buildSrc` classes of the target build; and `gradle.properties` values are available on `Settings` and `Project` but not on `Gradle`.

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: nothing.
Method: documentation only; no commands were run.
