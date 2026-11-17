---
id: computing-software.software-engineering.groovy.jenkinsfile-basics
name: jenkinsfile-basics
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, jenkinsfile-basics, groovy-jenkins]
level: intro
status: docs-checked
description: "Jenkinsfile structure: declarative pipeline blocks, scripted node blocks, and the CPS and @NonCPS rules for Groovy in pipelines."
sources:
  - https://www.jenkins.io/doc/book/pipeline/
  - https://www.jenkins.io/doc/book/pipeline/cps-method-mismatches/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declarative vs scripted Jenkinsfile
A `Jenkinsfile` can use Declarative or Scripted syntax. Declarative is designed to be easier to write and read and has richer syntax; Scripted is built on `node` blocks.

```groovy
pipeline {
  agent any
  stages {
    stage('Build') { steps { sh 'make' } }
    stage('Test')  { steps { sh 'make check'; junit 'reports/**/*.xml' } }
  }
}
```
- Declarative: `pipeline` holds everything; `agent` allocates an executor and workspace; `stage` and `steps` structure the work.
- Scripted equivalent: `node { stage('Build') { sh 'make' } }`. `node` queues the steps for a free executor and creates a workspace; `stage` blocks are optional but give clearer UI visualisation.
- `sh` and `junit` are Pipeline steps supplied by plugins, not Groovy methods.

## CPS: Pipeline Groovy is not plain Groovy
Jenkins runs pipeline scripts through a continuation-passing-style (CPS) transform so state can be saved to `program.dat` and survive a restart. Some Groovy constructs do not work as a result.
- CPS-transformed code may call non-CPS code, but non-CPS code may not call CPS-transformed code.
- A method marked `@NonCPS` bypasses the transform, so it must not call Pipeline steps such as `node` or `sh`.
- Passing a pipeline closure to a non-CPS method (for example `Iterable.toSorted`) does not work as intended; wrap the call in a `@NonCPS` method.
- Object construction with `new` cannot be CPS-transformed, so a constructor must not call Pipeline steps or CPS methods; use a static factory method instead.
- Overrides of non-CPS methods (such as `toString` called from `StringBuilder.append`) need `@NonCPS` and no steps inside.
- GString closures are CPS-transformed, which also causes surprises.

## Self-check
A `@NonCPS` method that calls `sh` fails with an error about expecting one method but catching `node` or `sh`; move the step call out into CPS code.

## Checked
Read the Jenkins Pipeline overview page (declarative vs scripted syntax, example Jenkinsfile) and the CPS method mismatches page. Removed: the `post { always { } }` block, the `script { }` block advice, the Pipeline Syntax snippet generator note, linter and security advice, and the reference to a jenkins-cps-nonCPS skill (none on pages read or not verifiable).

Method: docs-checked 2026-11-09 against the Jenkins Pipeline overview and CPS method mismatches pages.
