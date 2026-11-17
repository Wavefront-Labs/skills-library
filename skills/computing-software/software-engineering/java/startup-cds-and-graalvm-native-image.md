---
id: computing-software.software-engineering.java.startup-cds-and-graalvm-native-image
name: startup-cds-and-graalvm-native-image
category: computing-software
field: software-engineering
product: java
tags: [java, jvm, graalvm-native-image, appcds, class-data-sharing, aot-cache, startup-time, spring-aot, crac, project-leyden, java-deployment]
level: advanced
status: docs-checked
description: "Cut JVM startup time with AppCDS / the JDK AOT cache or GraalVM native image, including reflection configuration, Spring AOT and the trade-offs of each."
sources: ["https://docs.oracle.com/en/java/javase/21/vm/class-data-sharing.html", "https://openjdk.org/jeps/483", "https://www.graalvm.org/latest/reference-manual/native-image/", "https://docs.spring.io/spring-boot/reference/packaging/native-image/index.html"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Startup: CDS, AOT cache and GraalVM native image

**Goal:** fast start and low memory for CLIs, serverless functions and autoscaled
services, choosing the least disruptive technique that meets the target.

## Option 1: AppCDS (low effort)
```bash
java -XX:ArchiveClassesAtExit=app.jsa -jar app.jar     # training run, exit normally
java -XX:SharedArchiveFile=app.jsa -jar app.jar        # production
```
A dynamic archive is created with `-XX:ArchiveClassesAtExit` and used through
`-XX:SharedArchiveFile`; a different JDK can make the archive unusable (Oracle CDS documentation).

## Option 2: JDK AOT cache (JDK 24+, Project Leyden, JEP 483)
```bash
java -XX:AOTMode=record -XX:AOTConfiguration=app.aotconf -jar app.jar
java -XX:AOTMode=create -XX:AOTConfiguration=app.aotconf -XX:AOTCache=app.aot -jar app.jar
java -XX:AOTCache=app.aot -jar app.jar
```
Caches loaded AND linked classes (JEP 483); still a normal JVM, so no closed-world
restrictions. JEP 514 adds `-XX:AOTCacheOutput=app.aot` to record and create in one step.

## Option 3: GraalVM native image (biggest gain, biggest cost)
```bash
native-image -jar app.jar -o app            # or: mvn -Pnative package (GraalVM Maven plugin profile)
```
- Native compilation is an extra build step; measure startup and RSS on your target.
- Closed-world: reflection, dynamic proxies, resources and JNI must be declared.
  See GraalVM's Reachability Metadata and Automatic Collection of Metadata pages.
- Some libraries need reachability metadata; check GraalVM's Reachability Metadata documentation.
- Test the native binary in CI; JVM tests passing does not prove native works.

## Choosing
| Need | Pick |
|---|---|
| Faster start, zero code change | AppCDS / AOT cache |
| Scale-to-zero, CLIs, tiny memory | Native image |
| Long-running high-throughput service | Standard JIT (+ CDS) |

## Verify
- [ ] Measure time-to-first-request and RSS before/after on the target hardware.
- [ ] Native build runs the full test suite (`./gradlew nativeTest` or `mvn -Pnative test`).
- [ ] The CDS archive is actually used. `-Xshare:on` makes the VM exit when it cannot be used; Oracle documents it as for testing only, not production.

## Checked
2026-10-28 Confirmed on the Oracle CDS page, JEP 483, JEP 514 and the GraalVM Native Image page: `-XX:ArchiveClassesAtExit`, `-XX:SharedArchiveFile`, `-XX:AOTMode=record|create`, `-XX:AOTConfiguration`, `-XX:AOTCache`, `-XX:AOTCacheOutput`, `-Pnative` Maven profile, `nativeTest`, Reachability Metadata, `-Xshare:on` caveat. Removed (not on the fetched pages): same-classpath requirement, tracing-agent command, startup-in-ms and PGO claims, no-runtime-class-loading claim, `-Xlog:cds`, the Spring `native:compile` goal and the JDK 25 label.
Method: documentation only; no commands were run.
