---
id: computing-software.software-engineering.scala.sc-scalajs-native
name: sc-scalajs-native
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-scalajs-native, scalajs-native]
level: advanced
status: draft
description: "Compile Scala to JavaScript or native binaries and manage cross-platform projects."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scala.js and Scala Native targets
- sbt-crossproject (`crossProject(JVMPlatform, JSPlatform, NativePlatform)`) shares sources in `shared/`; use `%%%` for dependencies.
- Scala.js: facade types via `@js.native` and `js.Dynamic`; `fastLinkJS` for dev, `fullLinkJS` for production size; run tests on Node or a headless browser.
- Scala Native: C interop with `@extern`; limited Java standard library coverage; check each dependency publishes a native artifact.
- Threads, reflection and some `java.*` APIs are unavailable or different.
Verify: run the shared test suite on each platform in CI.
