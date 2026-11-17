---
id: computing-software.software-engineering.quarkus.quarkus-jib-image-customization
name: quarkus-jib-image-customization
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, jib, container-image, jvm-debug, entrypoint, layering]
level: practitioner
status: docs-checked
description: "Customize Quarkus Jib images: extra files via src/main/jib, JVM debug arguments, custom entrypoint, working directory and multi-module layering."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/container-image.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus Jib image customization

Prerequisite: the `quarkus-container-image-jib` extension and `-Dquarkus.container-image.build=true`.

## Extra files

Anything under `src/main/jib` is copied into the image, mirroring the Jib Maven/Gradle plugins. `src/main/jib/foo/bar` becomes `/foo/bar` in the container filesystem.

## Enable JVM debugging

With the default base image (`ubi10/openjdk-25-runtime` or `ubi10/openjdk-21-runtime`) use:

```properties
quarkus.jib.jvm-additional-arguments=-agentlib:jdwp=transport=dt_socket\\,server=y\\,suspend=n\\,address=*:5005
```

Note the escaped commas. Other base images may enable debugging through an environment variable set at launch.

## Custom entrypoint

`quarkus.jib.jvm-entrypoint` replaces the entry point entirely:

```properties
quarkus.jib.jvm-entrypoint=java,-Dcustom.param=custom_value,-jar,quarkus-run.jar
```

Or point to a script (better when parameters come from environment variables):

```properties
quarkus.jib.jvm-entrypoint=/bin/sh,run-java.sh
```

with the script stored as `run-java.sh` under `src/main/jib`, in a subfolder path that mirrors the jboss user home directory inside the image; the page's example script ends in `-jar quarkus-run.jar`.

Jib places the application, including `quarkus-run.jar`, in the jboss user home directory of the image and makes it the working directory. Change it with `quarkus.jib.working-directory`.

## Multi-module layering

To put supporting workspace modules in their own layer (they change more often than third-party dependencies), set `quarkus.bootstrap.workspace-discovery=true`. It must be a system property or build tool property (for example `-Dquarkus.bootstrap.workspace-discovery=true`); putting it in `application.properties` will not work because it is needed very early in the build.

## Other notes

- AOT/AppCDS caches in images are covered by the Quarkus AOT caching guide.

## Checked

2026-11-07. Read in full: container-image.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the claim that `quarkus.kubernetes.labels.<key>` labels are added to the Jib image (not on the cited page) and unconfirmed wording about the script location and image home directory.

Method: documentation only; no commands were run.
