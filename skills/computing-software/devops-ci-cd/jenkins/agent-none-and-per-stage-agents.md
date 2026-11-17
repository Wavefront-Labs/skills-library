---
id: computing-software.devops-ci-cd.jenkins.agent-none-and-per-stage-agents
name: agent-none-and-per-stage-agents
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, agent-none, per-stage-agent, declarative-pipeline]
level: practitioner
status: docs-checked
description: "Use agent none with per-stage agents in declarative Jenkins pipelines to avoid holding executors, mix labels/containers per stage, and handle workspace and stash."
sources: ["https://www.jenkins.io/doc/book/pipeline/syntax/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# agent none and per-stage agents

```groovy
pipeline {
  agent none
  options { timeout(time: 1, unit: 'HOURS') }
  stages {
    stage('Build') {
      agent { docker { image 'maven:3.9-eclipse-temurin-21'; label 'linux' } }
      steps { sh 'mvn -B package'; stash name: 'jar', includes: 'target/*.jar' }
    }
    stage('Windows test') {
      agent { label 'windows' }
      steps { unstash 'jar'; bat 'run-tests.cmd' }
    }
    stage('Approve') {
      steps { input message: 'Deploy?' }          // runs without any executor
    }
    stage('Deploy') {
      agent { label 'deploy' }
      options { skipDefaultCheckout() }
      steps { unstash 'jar'; sh './deploy.sh' }
    }
  }
}
```

## Why
- `agent any` at the top holds an executor for the whole run, including `input` waits.
- Each stage can pick its own label, docker image or Kubernetes pod.

## Consequences
- Every stage with an agent gets a **fresh workspace** on possibly another node. Pass files with
  `stash`/`unstash` (small files; stashes are cleared when the run completes unless `preserveStashes()` is set) or an artifact repository (large files).
- Implicit checkout happens per stage agent; use `skipDefaultCheckout()` where source is not needed.
- With `agent none` at the top, put `post` inside the stage that has the agent (stage-level `post` is
  supported), so its steps have a workspace.

## Verify
- [ ] Executors view is free while the run waits on input.
- [ ] Unstash succeeds on the second agent.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed in the Pipeline Syntax reference: `agent none` forces each stage to declare its own agent and avoids assigning an executor unnecessarily; `agent { docker { image ...; label ... } }`; stage-level `options { skipDefaultCheckout() }`; stage `when` `beforeAgent`; stash cleared on completion with `preserveStashes()` option. Removed unconfirmed claims about top-level `tools` and nested-stage agent inheritance.
Method: documentation only; no commands were run.
