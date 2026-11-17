---
id: computing-software.software-engineering.groovy.groovyshell-binding
name: groovyshell-binding
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, groovyshell-binding, groovy-embedding]
level: practitioner
status: docs-checked
description: "Evaluate Groovy from Java or Groovy with GroovyShell, Binding, parse, GroovyScriptEngine and caching."
sources:
  - https://groovy-lang.org/integrating.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/guide-integrating.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GroovyShell, Binding and GroovyScriptEngine
```groovy
def b = new Binding(x: 2)
def sh = new GroovyShell(b)
assert sh.evaluate('x * 21') == 42
def script = sh.parse('x + 1'); assert script.run() == 3
```
- `Binding` holds script variables (undeclared `def`-less names go to the binding).
- The `Binding` passed to a `GroovyShell` is not thread-safe and is shared by all scripts; for threads, create a distinct `Script` instance per thread with `parse` and give each its own `Binding`.
- `GroovyScriptEngine` adds script dependency handling and reloading on top of `GroovyClassLoader`.

## Gotchas
- Variables declared with `def` inside the script are local, not visible via Binding.

## Checked

2026-11-02. Confirmed against the Integrating Groovy chapter (GroovyShell, sharing data with `Binding`, multithreaded warning, GroovyScriptEngine). Removed: the metaspace-growth claim.

Method: documentation only; no commands were run.

## Self-check
Run the snippet.
