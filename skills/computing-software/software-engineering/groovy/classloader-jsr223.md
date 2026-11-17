---
id: computing-software.software-engineering.groovy.classloader-jsr223
name: classloader-jsr223
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, classloader-jsr223]
level: advanced
status: docs-checked
description: "Load classes at runtime with GroovyClassLoader and use Groovy via javax.script, with JAR dependency notes."
sources:
  - https://groovy-lang.org/integrating.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/guide-integrating.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GroovyClassLoader and JSR-223
- `new GroovyClassLoader().parseClass(source)` returns a `Class`; instantiate it and call methods on the instance.
- A `GroovyClassLoader` keeps a reference to every class it created, so it is easy to leak memory; parsing the same source `String` twice gives two distinct classes.
- Given a `File`, the loader can cache the generated class.
- JSR-223 is covered in the Integrating chapter's JSR-223 subproject section (not checked here).

## Gotchas
- The two-`parseClass` result is not the same class; keep the `Class` if you need one instance type.

## Checked

2026-11-02. Confirmed against the Integrating Groovy chapter (GroovyClassLoader section). Removed: `ScriptEngineManager`/`groovy-jsr223` details, `close()` per-tenant loaders, parent loader, `Invocable` and untrusted-code claims (the JSR-223 chapter lives in a subproject not read here).

Method: documentation only; no commands were run.

## Self-check
Parse a class implementing `Runnable` from a string and run it.
