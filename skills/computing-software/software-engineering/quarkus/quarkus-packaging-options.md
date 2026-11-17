---
id: computing-software.software-engineering.quarkus.quarkus-packaging-options
name: quarkus-packaging-options
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, packaging, fast-jar, uber-jar, aot, jlink, native-image]
level: intro
status: docs-checked
description: "Choose and build a Quarkus packaging type: fast JAR, uber-JAR, AOT cache, jlink image or native executable, with the commands and trade-offs from the packaging guide."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/packaging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus packaging options

Start with the default fast JAR and move on only for a concrete need; the same code runs in every mode.

## Fast JAR (default)

Produced by `./mvnw package` or `./gradlew build` as a `quarkus-app/` directory with an index mapping classes to dependency JARs (faster startup than a flat classpath).

```bash
java -jar target/quarkus-app/quarkus-run.jar
```

Deploy the whole `quarkus-app/` directory; a missing file means the app will not start or may misbehave.

## Uber-JAR

```properties
quarkus.package.jar.type=uber-jar
```

Output has a `-runner` suffix: `java -jar target/my-application-runner.jar`. Tune with `quarkus.package.jar.runner-suffix`, `quarkus.package.jar.add-runner-suffix=false` and `quarkus.package.ignored-entries` (comma-separated). Signature files from dependencies are excluded by default. Trade-offs: same-path resources across dependencies can clash, dependency JAR signatures are lost, and container builders like Jib cannot cache a dependency layer so every change rebuilds the whole layer.

## AOT caching (JDK 24+)

```bash
./mvnw verify -Dquarkus.package.jar.aot.enabled=true -DskipITs=false
cd target/quarkus-app
java -XX:AOTCache=app.aot -jar quarkus-run.jar
```

Keeps full JVM tooling (debuggers, profilers, JFR, JMX). Costs: roughly 40 MB extra for a small app, a slight throughput reduction at time of writing, and a training run (automated from integration tests).

## jlink image (experimental, Java 25+)

Add `quarkus-jlink` (`./mvnw quarkus:add-extension -Dextensions="quarkus-jlink"`), run `./mvnw package`, find the image in `target/jlink-output/image` and run its `bin/` launcher. It is platform-specific.

## Native executable

```bash
./mvnw package -Dnative
./target/my-application-runner
```

Best for serverless, scale-to-zero, CLI and memory-constrained hosts. Costs: lower peak throughput, 2-10 minute builds with 4-8 GB RAM, limited JVM tooling, and reflection/dynamic loading need explicit configuration.

Any option can be wrapped in a container image with `-Dquarkus.container-image.build=true` plus a container-image extension.

## Checked

2026-11-07. Matched against the text (with includes) of: packaging.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
