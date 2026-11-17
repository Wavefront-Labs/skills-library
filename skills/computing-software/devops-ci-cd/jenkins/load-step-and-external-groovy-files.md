---
id: computing-software.devops-ci-cd.jenkins.load-step-and-external-groovy-files
name: load-step-and-external-groovy-files
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, load-step, scripted-pipeline, jenkinsfile]
level: practitioner
status: docs-checked
description: "Split a large Jenkinsfile with the load step: return this pattern, workspace requirement, path rules and when to switch to a shared library instead."
sources: ["https://www.jenkins.io/doc/pipeline/steps/workflow-cps/#load-evaluate-a-groovy-source-file-into-the-pipeline-script", "https://www.jenkins.io/doc/book/pipeline/shared-libraries/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# load step and external Groovy files

`load` evaluates a Groovy file from the **workspace** and returns its value.

```groovy
// ci/helpers.groovy
def buildImage(String name) {
  sh "docker build -t ${name} ."
}
def notify(String msg) { echo msg }
return this            // required: lets the caller call methods on the result
```
```groovy
// Jenkinsfile (declarative)
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        script {
          def h = load 'ci/helpers.groovy'
          h.buildImage('app')
        }
      }
    }
  }
}
```

## Behaviour
- The path is relative to the current directory (`pwd()`), so the file must already be in the workspace (check out first).
- The loaded file is versioned with the repository branch (good for per-branch logic, bad for org-wide reuse).
- The script file must end with `return this` so its functions can be called on the result.

## load vs shared library
| Need | Use |
|---|---|
| Helpers for one repo | `load` |
| Reuse across repos, versioning, trusted code, unit tests | shared library |
| Custom steps with `call()` | shared library `vars/` |

## Gotchas
- Forgetting `return this` leaves you without an object to call the helper methods on.
- Variables declared with `def` at script top-level in the loaded file are local to it; use
  methods or fields accessed via the returned object.

## Verify
- [ ] Pipeline runs with the helper.

## Checked

2026-10-28. Confirmed in the Pipeline Steps reference (workflow-cps, `load`): the path is relative to the current directory and the loaded script ends with `return this`; and in the Shared Libraries page that a shared library is the reuse mechanism. Removed (not found in the pages): sandbox behaviour, re-read on each load, Replay tabs, the exact error message, the `GIT_COMMIT` variable in the example.

Method: documentation only; no commands were run.
