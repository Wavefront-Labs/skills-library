---
id: computing-software.software-engineering.groovy.grape-config-cli
name: grape-config-cli
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, grape-config-cli]
level: advanced
status: docs-checked
description: "grapeConfig.xml, proxy and repository settings, and the grape command line (install, list, resolve)."
sources:
  - https://groovy-lang.org/grape.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/grape.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grape configuration and grape command
- GrapeIvy (the default engine) reads Ivy settings from `~/.groovy/grapeConfig.xml`; the file is not used by GrapeMaven, which takes extra repositories from `@GrabResolver` or `Grape.addResolver`.
- Commands: `grape install [-hv] <group> <module> [<version>] [<classifier>]`, `grape list`, `grape resolve [-adhisv] (<groupId> <artifactId> <version>)+`, `grape uninstall [-hv] <group> <module> <version>` (removes the jar non-transitively).
- Proxy: `-Dhttp.proxyHost=... -Dhttp.proxyPort=...` on the command line or in `JAVA_OPTS`.
- Cache root defaults to `~/.groovy`; change with `-Dgrape.root=<dir>`. GrapeIvy uses `~/.groovy/grapes`, GrapeMaven `~/.groovy/grapesM2`.

## Gotchas
- Without a `grapeConfig.xml`, Grape uses its built-in default Ivy settings (`defaultGrapeConfig.xml` in the Groovy sources).

## Checked

2026-11-02. Confirmed against the Grape page (Command Line Tool, Repository Directory, Customize Ivy settings, Proxy settings). Removed: the `https.proxyHost` flag, private-repository credential advice and the cache-deletion tip.

Method: documentation only; no commands were run.

## Self-check
`grape list` before and after installing a module.
