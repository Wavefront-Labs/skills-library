---
id: computing-software.software-engineering.spring-boot.dockerfile-layered-jar-jarmode
name: dockerfile-layered-jar-jarmode
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, docker, dockerfile, jarmode, layers, aot-cache, cds, container-images]
level: practitioner
status: docs-checked
description: "Build optimized Dockerfiles with the jarmode tools extract command, plus the AOT cache (Java 25+) and CDS training-run variants and their ENTRYPOINT flags."
sources:
  - https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Using the layering feature gives a more optimized image than copying the uber jar. A jar containing the layers index file gets `spring-boot-jarmode-tools` as a dependency, enabling a mode where the bootstrap code runs something other than your application:
```shell
$ java -Djarmode=tools -jar my-app.jar
```
Commands: `extract` (extract contents from the jar), `list-layers` (list layers that can be extracted), `sbom` (print the SBOM from the jar), `help`.

The documented Dockerfile is multi-stage: the builder stage runs `extract` and each `COPY` in the final stage relates to a layer extracted by jarmode. It ends with:
```
ENTRYPOINT ["java", "-jar", "application.jar"]
```
This `application.jar` contains only application code and references to the extracted jar files; the layout is efficient to start and AOT cache (and CDS) friendly. Build with `docker build .` or `docker build --build-arg JAR_FILE=path/to/myapp.jar .`. A Dockerfile can be written without jarmode (`unzip` and `mv` per layer) but jarmode simplifies it.

AOT cache (Java 25+): after the same stages, run a training run, then start with the cache:
```
RUN java -XX:AOTCacheOutput=app.aot -Dspring.context.exit=onRefresh -jar application.jar
ENTRYPOINT ["java", "-XX:AOTCache=app.aot", "-jar", "application.jar"]
```
CDS (use AOT cache instead on Java 24 or later):
```
RUN java -XX:ArchiveClassesAtExit=application.jsa -Dspring.context.exit=onRefresh -jar application.jar
ENTRYPOINT ["java", "-XX:SharedArchiveFile=application.jsa", "-jar", "application.jar"]
```
The shared stages come from the docs partial: a builder stage that copies the jar to application.jar and runs `java -Djarmode=tools -jar application.jar extract --layers --destination extracted`, then a runtime stage with one COPY per extracted layer (dependencies, spring-boot-loader, snapshot-dependencies, application). The partial's base image is a BellSoft Liberica 25-cds image; substitute your own.

## Checked

2026-11-07

Read dockerfiles.adoc (docs-repo source of the cited Dockerfiles page) in full, plus the dockerfile partial it includes (reference partials/dockerfile). The linked AOT cache page (packaging/aot-cache.adoc) was not read.
Confirmed: layering feature and spring-boot-jarmode-tools added as a dependency when the layers index exists; java -Djarmode=tools -jar my-app.jar and the four listed commands (extract, list-layers, sbom, help); the ENTRYPOINT java -jar application.jar with the comment about application code only, efficient start-up and AOT cache/CDS friendliness; docker build . and --build-arg JAR_FILE=path/to/myapp.jar; multi-stage builder with COPY per layer; jarmode optional versus unzip and mv; AOT cache section for Java 25 or above (training run with -XX:AOTCacheOutput=app.aot -Dspring.context.exit=onRefresh, ENTRYPOINT with -XX:AOTCache=app.aot); CDS section (-XX:ArchiveClassesAtExit=application.jsa, -XX:SharedArchiveFile=application.jsa) and the NOTE to use AOT cache on Java 24 or later.
Trimmed: the unfinished "partial was not read" sentence, now replaced by what the partial actually contains.

Method: documentation only; no commands were run.
