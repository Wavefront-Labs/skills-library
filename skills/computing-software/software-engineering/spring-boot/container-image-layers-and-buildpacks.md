---
id: computing-software.software-engineering.spring-boot.container-image-layers-and-buildpacks
name: container-image-layers-and-buildpacks
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, container-images, layers-idx, buildpacks, cloud-native-buildpacks, paketo, docker]
level: practitioner
status: docs-checked
description: "Why layered Spring Boot images beat the uber jar, the four default layers in layers.idx, and building images with Cloud Native Buildpacks from Maven or Gradle."
sources:
  - https://docs.spring.io/spring-boot/reference/packaging/container-images/efficient-images.html
  - https://docs.spring.io/spring-boot/reference/packaging/container-images/cloud-native-buildpacks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Uber jar downsides: running it without unpacking has overhead that can be noticeable in containers, and one layer with code plus all dependencies is not optimal. You recompile code more often than you upgrade Boot, so put jar files in layers before application classes; Docker often only needs to change the very bottom layer and caches the rest.

Layer index: Boot supports a `layers.idx` file in the jar (and war) listing layers and the parts of the jar in each, ordered by the order layers should be added to the image. Default layers:
- `dependencies` (regular released dependencies)
- `spring-boot-loader` (everything under `org/springframework/boot/loader`)
- `snapshot-dependencies`
- `application` (application classes and resources)
```yaml
- "dependencies":
  - BOOT-INF/lib/library1.jar
  - BOOT-INF/lib/library2.jar
- "spring-boot-loader":
  - org/springframework/boot/loader/launch/JarLauncher.class
- "snapshot-dependencies":
  - BOOT-INF/lib/library3-SNAPSHOT.jar
- "application":
  - META-INF/MANIFEST.MF
  - BOOT-INF/classes/a/b/C.class
```
Layers separate code by how likely it is to change between builds. Adding the index is documented in the Maven plugin "packaging layered jar or war" section and the Gradle plugin equivalent.

Buildpacks: Docker images can be built directly from the Maven or Gradle plugin using Cloud Native Buildpacks, producing Docker-compatible images with one command into the local Docker daemon (see the plugins' build-image / packaging-oci-image documentation). The Paketo Spring Boot buildpack supports `layers.idx`, so layer customizations are reflected in the image.

Reproducible builds: buildpacks may manipulate resource metadata such as "last modified"; make sure the app does not rely on it at runtime. Boot may use it when serving static resources; disable with `spring.web.resources.cache.use-last-modified`.

## Checked

2026-11-07

Read efficient-images.adoc and cloud-native-buildpacks.adoc (docs-repo sources of the two cited pages) in full; both are short. The Maven and Gradle plugin pages they link to were not read, so the skill only points to them.
Confirmed: uber-jar overhead and single-layer downsides, and the recompile-more-than-upgrade reasoning; layers.idx as a layer index ordered by the order layers are added, supported for jars and wars; the four out-of-the-box layers with their descriptions; the example layers.idx content; layering separates code by likelihood of change; Cloud Native Buildpacks from the Maven or Gradle plugin giving Docker-compatible images from one command into the local Docker daemon; Paketo Spring Boot buildpack supporting layers.idx; the reproducible-builds NOTE with spring.web.resources.cache.use-last-modified.
Trimmed: awkward "unpacked-less" and "usually changes only the bottom layer" reworded to the page's wording ("without unpacking", "often only needs to change the very bottom layer").

Method: documentation only; no commands were run.
