---
id: computing-software.software-engineering.scala.sc-sbt-assembly-publish
name: sc-sbt-assembly-publish
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-build-sbt, sbt-assembly-publish]
level: advanced
status: draft
description: "Build fat jars and publish artifacts with sbt-assembly, sbt-native-packager and publishing settings."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Packaging, assembly and publishing
- `sbt assembly` (sbt-assembly) needs a `assemblyMergeStrategy` for duplicate META-INF files.
- `sbt-native-packager` builds Docker images, zips and Debian/RPM packages (`Docker / publishLocal`).
- `publishTo`, `credentials`, `versionScheme := Some("early-semver")` (sbt 1.5 or newer) for published libraries; `sbt-ci-release` automates Sonatype releases.
- Keep credentials out of `build.sbt`; read them from environment variables.
Verify: run the assembled jar with `java -jar`.
