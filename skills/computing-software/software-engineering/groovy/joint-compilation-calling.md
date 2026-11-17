---
id: computing-software.software-engineering.groovy.joint-compilation-calling
name: joint-compilation-calling
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, joint-compilation-calling]
level: advanced
status: docs-checked
description: "Joint compilation, calling Groovy from Java, generics, and dependency on groovy jar at runtime."
sources:
  - https://groovy-lang.org/differences.html
  - https://groovy-lang.org/integrating.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/tools-groovyc.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calling between Java and Groovy
- Joint compile: `groovyc -j A.groovy B.java`. The Groovy compiler parses the Groovy sources, creates stubs, has the Java compiler compile stubs plus Java sources, then continues normally. `-J` and `-F` pass properties and flags to `javac`.
- Maven: GMavenPlus handles Groovy compilation; its joint compilation uses stubs.

## Gotchas
- Without `-j`, Java sources given to `groovyc` are compiled as if they were Groovy, which may differ in semantics.

## Checked

2026-11-02. Confirmed against the groovyc page (`-j`, `-J`, `-F`, Joint compilation, GMavenPlus). Removed: Gradle layout, Maven plugin coordinates, Groovy artifact coordinates, closure, runtime-jar, property and version-conflict claims.

Method: documentation only; no commands were run.

## Self-check
Joint-compile a Java class calling a Groovy class and run it.
