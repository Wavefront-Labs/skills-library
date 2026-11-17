---
id: computing-software.software-engineering.groovy.jenkins-cps-noncps
name: jenkins-cps-noncps
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, jenkins-cps-noncps]
level: advanced
status: docs-checked
description: "Why Jenkins Pipeline Groovy differs: CPS transform, what is and is not transformed, @NonCPS rules and the common CPS method mismatches."
sources:
  - https://www.jenkins.io/doc/book/pipeline/cps-method-mismatches/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPS and @NonCPS
- Pipeline runs scripts with the Groovy CPS library: a continuation-passing-style transform lets the interpreter save its state to disk (a file called `program.dat` in the build directory) and keep running after Jenkins restarts.
- CPS-transformed: almost all Pipeline script you write (including libraries) and most steps, including all that take a block.
- Not CPS-transformed: compiled Java bytecode (Java platform, Jenkins core and plugins, the Groovy runtime), constructor bodies in your script, any method marked `@NonCPS`, and a few block-less instantaneous steps such as `echo` or `properties`.
- Rule: CPS code may call non-CPS or CPS code; non-CPS code may call non-CPS code but must not call CPS code. Breaking it gives incorrect and often confusing results.

## Common mismatches
- Steps inside `@NonCPS`: `node` or `sh` inside a `@NonCPS` method is illegal. Log warning: `expected to call WorkflowScript.compileOnPlatforms but wound up catching node`. Fix: remove the annotation.
- Non-CPS method given a CPS closure: e.g. `Iterable.toSorted { a, b -> ... }` returns the closure's first return value. Fix: wrap the call in a `@NonCPS` method, or define a class for the closure with all its methods `@NonCPS`.
- Constructors: `new` cannot be CPS-transformed, so a constructor calling a CPS method fails (`expected to call Test.<init> but wound up catching Test.setX`). Fix: mark methods called from a constructor `@NonCPS` and call no steps there; or move the logic into a static factory method.
- Overriding non-CPS methods (e.g. `toString` used by `StringBuilder.append`): annotate the override `@NonCPS` and use no CPS code in it.
- Closures inside a GString (`"x = ${-> x}"`) do not work. Use a closure that returns a GString built from a normal expression, and call it.
- Some expressions trigger the warning although they run correctly; the page asks for an issue against workflow-cps-plugin.

## Gotchas
- `@NonCPS` is also used to bypass CPS limits in the Groovy language or for speed (the interpreter has substantial overhead), but the body must not call Pipeline steps.

## Verify
Reproduce a warning from the list above in a test pipeline and confirm the stated fix removes it.

## Checked
2026-11-09. Read the Jenkins "Pipeline CPS Method Mismatches" page in full and rewrote the skill from it. Removed claims the page does not state: Serializable/NotSerializableException advice, `each`/`collect` behaviour, Script Security sandbox and `@Library` trust notes, and the approval advice. The first cited source (pipeline index) was not read and is dropped.
Method: documentation only; no commands were run.
