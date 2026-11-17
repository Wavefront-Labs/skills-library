---
id: computing-software.devops-ci-cd.gradle.gradle-upgrading-between-versions
name: gradle-upgrading-between-versions
category: computing-software
field: devops-ci-cd
product: gradle
tags: [upgrade, deprecations, warning-mode, wrapper, build-scan]
level: practitioner
status: docs-checked
description: "Upgrade a Gradle build safely by surfacing deprecations first, updating plugins and then the wrapper."
sources: ["https://docs.gradle.org/current/userguide/upgrading_version_8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle upgrading between versions

The Gradle 8.x upgrade guide gives this order of work.

1. Find deprecations. Run `gradle help --scan` and use the deprecations view in the Build Scan, or `gradle help --warning-mode=all` for console warnings with less detail.
2. Update your plugins first. Plugins using internal or removed APIs may break, and the warnings from step 1 help identify them.
3. Update the wrapper: `gradle :wrapper --gradle-version 8.14.5` (run it twice so the scripts and JAR update as well as the properties file).
4. Run the build and use the Troubleshooting Guide for errors.

Treat deprecation warnings as upcoming work: the 8.x notes list features deprecated for removal in Gradle 9.0.0.

Related habits:
- `--warning-mode` takes `all`, `fail`, `none` or `summary` (the default).
- Since Gradle 9.0.0 the wrapper `distributionUrl` version must be in `X.Y.Z` format.

The page cited here is the Gradle 8.x guide (8.14.5); other major versions have their own upgrade pages.

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: the removal-in-Gradle-10 claim, the per-version reading advice, the CI warning-mode advice, the Java/Kotlin/Groovy compatibility advice and the 'guide in this repository' line (none are on the page).
Method: documentation only; no commands were run.
