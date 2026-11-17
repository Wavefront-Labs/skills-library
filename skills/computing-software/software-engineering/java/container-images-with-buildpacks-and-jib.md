---
id: computing-software.software-engineering.java.container-images-with-buildpacks-and-jib
name: container-images-with-buildpacks-and-jib
category: computing-software
field: software-engineering
product: java
tags: [java, java-deployment, boot-buildpacks, jib, layered-jars, oci-image, spring-boot-build-image]
level: practitioner
status: docs-checked
description: "Build OCI images for Java apps without a Dockerfile using the Spring Boot Maven build-image goal (buildpacks) or Jib: layering, builder, reproducibility, publish."
sources: ["https://docs.spring.io/spring-boot/maven-plugin/build-image.html", "https://github.com/GoogleContainerTools/jib", "https://docs.spring.io/spring-boot/reference/packaging/container-images/efficient-images.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Buildpacks and Jib

## Spring Boot buildpacks (Cloud Native Buildpacks)
```bash
mvn spring-boot:build-image -Dspring-boot.build-image.imageName=registry.example.com/acme/orders:1.4.2
mvn spring-boot:build-image -Dspring-boot.build-image.imageName=registry.example.com/acme/orders:1.4.2 -Dspring-boot.build-image.publish=true
```
- Needs access to a Docker daemon (current Docker CLI context, `DOCKER_HOST`, or `docker.host` in the plugin configuration; podman and Colima setups are shown on the page).
- Images build and run as a non-root user. The default builder is `paketobuildpacks/builder-noble-java-tiny:latest`; change it with `<image><builder>` or `-Dspring-boot.build-image.builder=`. `pullPolicy` defaults to `ALWAYS`, so pin the builder tag/digest for repeatable builds.
- The plugin detects the project's Java target and tells the default Paketo buildpacks to install the same Java version. Override with builder env: `<image><env><BP_JVM_VERSION>...</BP_JVM_VERSION></env></image>`.
- Paketo Java buildpacks set `JAVA_TOOL_OPTIONS`; persist additions with `BPE_APPEND_JAVA_TOOL_OPTIONS` (plus `BPE_DELIM_JAVA_TOOL_OPTIONS` for the separator).
- Bind to the lifecycle with the `build-image-no-fork` goal (the plain goal forks the lifecycle and is for the command line).
- Publish: `publish` is `false` by default; the target registry comes from the image name. Credentials go in `docker.publishRegistry` (`username`/`password` or `token`); pass them from CI secrets as properties rather than hard-coding. If none are given the plugin reads the Docker config file (credential helpers, credential store, static `auths`).
- Reproducibility: `createdDate` defaults to a fixed date so identical contents produce the same image; set `now` only if you want a real timestamp.
- Build and launch caches are named volumes derived from the image name, so a tag that changes every build (such as the project version) invalidates them; name the volumes explicitly with `buildCache` and `launchCache`.
- The Gradle plugin has its own documentation page; this skill covers the Maven plugin only.

## Layered jars (for your own Dockerfile)
Spring Boot can add `layers.idx` to the jar. The default layers, in order, are `dependencies`, `spring-boot-loader`, `snapshot-dependencies` and `application`, so that code that changes often sits in the last layer and Docker can reuse the cached ones below it. Running the uber jar unpacked avoids the overhead of running it as-is.

## Jib (no Docker daemon)
Jib builds optimized Docker and OCI images for Java apps without a Docker daemon, as Maven and Gradle plugins, a Java library (Jib Core) and a CLI. It splits the application into layers (dependencies separate from classes) so a code change rebuilds only the changed layer, and it aims for reproducible images. The base is an OpenJDK image by default; a custom base image can be configured. Plugin goals and configuration live in the jib-maven-plugin and jib-gradle-plugin documentation, which this skill did not read.

## Which
Buildpacks: least configuration, a Docker daemon is required. Jib: no daemon, no Dockerfile. A hand-written Dockerfile over the layered jar is the third option when you need OS packages.

## Gotchas
- Do not bake secrets into images or environment.
- Pin the builder or base image, and rescan images regularly.

## Verify
Run the image and confirm the process is not root; check that dependency layers are separate and that a second build after a code-only change reuses them.

## Checked

Date: 2026-11-08

Read in full: the Spring Boot Maven plugin Packaging OCI Images page, the Efficient Container Images page and the Jib README. Confirmed: build-image and build-image-no-fork behaviour, daemon requirement, non-root note, default builder and pull policy, Java version detection, env examples including BP_JVM_VERSION and the JAVA_TOOL_OPTIONS variables, publish settings and credential sources, createdDate default, cache naming, default layer names, and Jib's daemonless layered, reproducible design. Removed because the cited pages do not state them: Gradle bootBuildImage syntax, native image and SBOM support, memory calculation, Jib goals and XML, user and JVM flag settings, and the jarmode extract command.

Method: documentation only; no commands were run.
