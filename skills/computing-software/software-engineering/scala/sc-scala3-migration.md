---
id: computing-software.software-engineering.scala.sc-scala3-migration
name: sc-scala3-migration
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-migration, scala3-migration]
level: advanced
status: docs-checked
description: "Migrate a Scala 2.13 codebase to Scala 3 incrementally with the Scala 3 migration mode and cross-building."
sources: ["https://docs.scala-lang.org/scala3/guides/migration/migrating-to-3-3.html", "https://docs.scala-lang.org/scala3/guides/migration/incompatibilities.html", "https://docs.scala-lang.org/scala3/guides/migration/interoperability.html", "https://docs.scala-lang.org/scala3/guides/migration/incompat-dropped-features.html", "https://docs.scala-lang.org/scala3/guides/migration/macros.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-building and Scala 3 migration steps
- Add the Scala 3 version to `crossScalaVersions` of the module; in the sbt shell `++<version>` switches the module to that version.
- Compile on 2.13 with `-Xsource:3` to locate Scala 3 incompatibilities before switching compilers.
- `-source:3.0-migration -rewrite` rewrites some of the incompatibilities automatically; others are only warned about. The optional sbt-scala3-migrate plugin automates part of the work.
- A Scala 3 module uses a published 2.13 library with `.cross(CrossVersion.for3Use2_13)`; a 2.13 module uses a Scala 3 library with `.cross(CrossVersion.for2_13Use3)`.
- Scala 2.13 reads Scala 3 TASTy with the `-Ytasty-reader` option.
- The Scala 3 compiler cannot expand Scala 2.13 macros; macro libraries must be ported or replaced.
- Dropped features that break code: symbol literals, `do`-`while`, auto-application, early initializers, existential types, `@specialized`, procedure syntax, view bounds.
- The Scalafix rule `ExplicitResultTypes` can write missing type annotations on implicit definitions.
Verify: both Scala versions compile and tests pass in CI.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 migration guide pages (Migrating to Scala 3.3, Incompatibility Table, Interoperability, Dropped Features, Macro Libraries). Removed as not on those pages: `private[this]` and wildcard-import breakages, the `Xsource:3` easing claim, the scalafix-rules-in-general claim.

Method: documentation only; no commands were run.
