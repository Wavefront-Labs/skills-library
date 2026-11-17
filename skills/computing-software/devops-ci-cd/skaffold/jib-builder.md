---
id: computing-software.devops-ci-cd.skaffold.jib-builder
name: jib-builder
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [jib, maven, gradle, java]
level: practitioner
status: docs-checked
description: "Build Java images without a Dockerfile using the jib builder with Maven or Gradle."
sources:
  - "https://skaffold.dev/docs/builders/builder-types/jib/"
  - "https://skaffold.dev/docs/filesync/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `jib` builder builds Java container images through the Jib plugins for Maven and Gradle, without a Docker daemon. Skaffold requires Jib v1.4.0 or later, and your project must already be configured to use Jib. It works locally and on Google Cloud Build (not in-cluster).

```yaml
build:
  artifacts:
  - image: my-registry/java-app
    context: .
    jib:
      project: module-a
      args: ["-DskipTests"]
      type: maven
```

Options (schema `JibArtifact`):

- `type`: `maven` or `gradle`; normally determined automatically. Skaffold chooses from files in the artifact `context`: Maven for `pom.xml` or a `.mvn` directory; Gradle for `build.gradle`, `gradle.properties`, `settings.gradle` or the wrapper (`gradlew`, `gradlew.bat`, `gradlew.cmd`).
- `project`: selects the sub-project in a multi-module build.
- `args`: additional arguments for the Maven or Gradle command line (for example `--no-daemon` for Gradle).
- `fromImage`: overrides the configured Jib base image. `requires` can make another artifact the `fromImage`.

Multi-module projects: create one Skaffold artifact per module that produces an image, set `context` to the root project location, and set `project` to the Maven `:artifactId`, `groupId:artifactId` or relative path of the module, or to the Gradle sub-project name. With Jib 1.4.0 and later, binding a Jib `build` or `dockerBuild` goal to the Maven `package` phase is no longer required and should be removed.

Jib supports file sync auto mode in `skaffold dev` (default exploded build mode, non-WAR applications only), so class and resource changes can reach the container without a rebuild. See the file sync skills.

The `jib` builder normally invokes the Maven `prepare-package` goal rather than `package`. If a plugin needs `package`, the page suggests using the `custom` builder with a `buildCommand` that runs `jib:build` or `jib:dockerBuild`.

## Checked

2026-11-04. Read the Skaffold Jib Build page, the File Sync page (Jib section) and the `JibArtifact` definition in the v4beta14 schema. Confirmed all options, build-file detection, multi-module steps, the Jib 1.4.0 minimum and the custom builder workaround. Removed: the example `gcr.io/distroless/java17` base image, the tip to detect the type with `skaffold diagnose`, and the claim of a version error on old plugins (none of these appear on the pages).
Method: documentation only; no commands were run.
