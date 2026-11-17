---
id: computing-software.software-engineering.kotlin.kt-kotlin-version-migration
name: kt-kotlin-version-migration
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-tooling, kotlin-version-migration]
level: advanced
status: docs-checked
description: "Upgrade Kotlin versions: language/api version options, K2 compiler behaviour changes and the compatibility guides."
sources: ["https://kotlinlang.org/docs/k2-compiler-migration-guide.html", "https://kotlinlang.org/docs/compiler-reference.html", "https://kotlinlang.org/docs/compatibility-guide-22.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# K2 compiler and language version migration
- The K2 compiler is enabled by default starting with Kotlin 2.0.0; the K2 migration guide lists behaviour changes.
- Each release has a compatibility guide (for example the Kotlin 2.2 one) listing deprecations and incompatible changes; read it before upgrading.
- The language version and API version compiler options (`languageVersion`, `apiVersion`) control which language features and standard-library APIs your code can use; in most cases they should be the same.
- The K2 migration guide covers kapt and KSP (KSP2) support; check each compiler plugin and annotation processor you use.
Verify: a CI build with warnings as errors after each bump.

## Checked
2026-11-03. Confirmed on the K2 migration guide, compiler reference and the Kotlin 2.2 compatibility guide: K2 default from 2.0, languageVersion/apiVersion meaning, kapt and KSP notes.
Removed: "upgrade one minor version at a time", the WARNING-to-ERROR deprecation claim and the Compose compiler plugin mention (not on the pages).
Method: documentation only; no commands were run.
