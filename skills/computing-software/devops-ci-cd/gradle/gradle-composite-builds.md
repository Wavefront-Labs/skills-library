---
id: computing-software.devops-ci-cd.gradle.gradle-composite-builds
name: gradle-composite-builds
category: computing-software
field: devops-ci-cd
product: gradle
tags: [composite-builds, include-build, dependency-substitution, build-logic, buildsrc]
level: advanced
status: docs-checked
description: "Combine builds with includeBuild, control dependency substitution and prefer included builds for shared build logic."
sources: ["https://docs.gradle.org/current/userguide/composite_builds.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle composite builds

Add an included build in `settings.gradle(.kts)`:

```kotlin
includeBuild("my-utils")
```

Relative paths resolve from the settings file; absolute paths are heavily discouraged.

Substitution: by default Gradle replaces any external dependency matching `${project.group}:${project.name}` with the matching project of an included build. Declare it explicitly with:

```kotlin
includeBuild("anonymous-library") {
    dependencySubstitution {
        substitute(module("org.sample:number-utils")).using(project(":"))
    }
}
```

Substitutions apply only to the declaring build and are not transitive across builds. Set `resolutionStrategy.useGlobalDependencySubstitutionRules = false` on a configuration to resolve published versions instead.

Build logic: `buildSrc` is essentially an included build that Gradle manages automatically; a `build-logic` build added with `includeBuild()` is the same idea made explicit. For plugins used in build scripts: `pluginManagement { includeBuild("my-plugin") }`; settings plugins also need the include inside `pluginManagement {}`.

Command line: `./gradlew --include-build ../my-utils run`, but this can be unreliable for plugins applied via the `plugins {}` block, so prefer settings.

Run tasks with qualified paths: `./gradlew :included-build:subproject-a:compileJava`, exclude with `--exclude-task :my-app:app:test`, or depend on them with `dependsOn(gradle.includedBuild("my-app").task(":app:run"))`.

Limitations: odd publications, conflicts when several composites include the same build in parallel, default substitution forcing full configuration of the included build (explicit rules avoid this under configuration-on-demand), and `project(":other-build:module")` throwing `UnknownProjectException` across builds.

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: the 'Gradle recommends build-logic over buildSrc' wording, replaced by what the page states.
Method: documentation only; no commands were run.
