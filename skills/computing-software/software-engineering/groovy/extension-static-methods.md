---
id: computing-software.software-engineering.groovy.extension-static-methods
name: extension-static-methods
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, extension-static-methods]
level: advanced
status: docs-checked
description: "Add static methods to existing classes via an extension module and how Groovy discovers modules at runtime."
sources:
  - https://groovy-lang.org/metaprogramming.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-metaprogramming.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static extension methods and discovery
- Static extension methods go in their own class, listed under `staticExtensionClasses`. The first parameter is the class being extended and is unused. Static and instance extension methods cannot share a class.
- An extension must be compiled and on the classpath before the code that uses it is compiled.

## Gotchas
- The descriptor file is `META-INF/groovy/org.codehaus.groovy.runtime.ExtensionModule`.

## Self-check
Build the module, put it on the classpath and call a static extension method on the extended class.

## Checked

2026-11-02. Confirmed against the Metaprogramming chapter (Extension modules: static methods, module descriptor, extension modules and classpath). Removed: classpath-scan and module-registry claims, GDK module list, shadowing claim.

Method: documentation only; no commands were run.
