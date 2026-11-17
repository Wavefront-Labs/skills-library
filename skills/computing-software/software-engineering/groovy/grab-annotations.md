---
id: computing-software.software-engineering.groovy.grab-annotations
name: grab-annotations
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, grab-annotations, groovy-grape]
level: practitioner
status: docs-checked
description: "Pull dependencies into a script with @Grab, coordinate forms, @GrabResolver, @GrabExclude and @GrabConfig."
sources:
  - https://groovy-lang.org/grape.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/grape.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @Grab and @Grapes
```groovy
@Grab('org.apache.commons:commons-lang3:3.14.0')   // version illustrative
import org.apache.commons.lang3.StringUtils
println StringUtils.capitalize('hi')
@Grab(group='org.yaml', module='snakeyaml', version='2.2')
```
- `@Grab` goes on an import or declaration; several can sit on the same node, and `@Grapes([@Grab(...), @Grab(...)])` is now purely optional.
- `@GrabResolver(name='r', root='https://repo.example/maven')` adds a repository; `@GrabExclude` excludes a dependency.
- `@GrabConfig(systemClassLoader=true)` attaches JDBC drivers to the system class loader.
- GrapeIvy (default) caches in `~/.groovy/grapes`; GrapeMaven uses `~/.groovy/grapesM2`.

## Gotchas
- With GrapeIvy, `@GrabConfig(autoDownload=false)` restricts resolution to the local cache (no network calls).
- A version of `'*'` resolves to the latest version, and ranges such as `[2.2.1,2.3.0)` are accepted, so pin exact versions for repeatable runs.

## Checked

2026-11-02. Confirmed against the Grape page (Quick start, Specifying additional repositories, Excluding, Dependency on JDBC drivers, Grape Implementations). Removed: the `+` range and supply-chain claims and the Ivy-needs-network claim.

Method: documentation only; no commands were run.

## Self-check
Run a script with one @Grab and confirm the jar appears under the local Grape cache.
