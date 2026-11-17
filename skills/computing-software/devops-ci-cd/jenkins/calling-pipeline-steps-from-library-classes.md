---
id: computing-software.devops-ci-cd.jenkins.calling-pipeline-steps-from-library-classes
name: calling-pipeline-steps-from-library-classes
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, library-steps-reference, src-classes, shared-libraries]
level: advanced
status: docs-checked
description: "Call sh, echo, withCredentials and env from shared library src classes by passing the script object, keeping classes Serializable and CPS-safe."
sources: ["https://www.jenkins.io/doc/book/pipeline/shared-libraries/", "https://www.jenkins.io/doc/book/pipeline/cps-method-mismatches/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calling pipeline steps from src classes

Classes under `src/` are plain Groovy; they do not see `sh`, `echo`, `env` or `currentBuild`.
Pass the pipeline script (`this` in the Jenkinsfile or in a `vars/` step) into the class.

```groovy
// src/org/acme/Docker.groovy
package org.acme
class Docker implements Serializable {
  private final def steps
  Docker(steps) { this.steps = steps }
  void build(String image) {
    steps.sh "docker build -t ${image} ."
    steps.echo "built ${image} on ${steps.env.NODE_NAME}"
  }
  void push(String image, String credId) {
    steps.withCredentials([steps.usernamePassword(credentialsId: credId,
        usernameVariable: 'U', passwordVariable: 'P')]) {
      steps.sh 'echo "$P" | docker login -u "$U" --password-stdin registry.example.com'
      steps.sh "docker push ${image}"
    }
  }
}
```
```groovy
// vars/dockerBuild.groovy
def call(String image) { new org.acme.Docker(this).build(image) }
// Jenkinsfile
@Library('acme@v3') _
node { dockerBuild('registry.example.com/app:1') }
```

## Rules
- `implements Serializable`: the Shared Libraries page says a class that saves state (such as the
  `steps` field) must implement `Serializable` so the Pipeline can suspend and resume.
- Credential bindings inside library code still use single-quoted `sh` strings so Groovy does not
  interpolate secrets.
- Static methods: pass `script` as the first argument (`static void info(script, msg) { script.echo msg }`).
- `@NonCPS` methods must not call steps (CPS method-mismatch guide).
- Libraries configured under *Global Trusted Pipeline Libraries* are trusted; see the Shared
  Libraries page for what that allows.

## Verify
- [ ] A real run on a test Jenkins prints the echo and the `docker` commands run on the expected node.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed in the Shared Libraries page: the `steps` constructor-injection pattern (`class Utilities implements Serializable { def steps; Utilities(steps) {...} }`), the Serializable requirement, `@Library('name') _`, and Global Trusted Pipeline Libraries; `@NonCPS` step restriction in the CPS method-mismatch guide. Removed the unconfirmed claim about script approval for non-whitelisted APIs and the unit-testing check.
Method: documentation only; no commands were run.
