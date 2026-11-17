---
id: computing-software.devops-ci-cd.jenkins.input-without-holding-an-executor
name: input-without-holding-an-executor
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, input-outside-agent, input-step, agent-none]
level: practitioner
status: docs-checked
description: "Wait for human approval in Jenkins without blocking an executor: stage-level input directive, agent none, timeouts and milestones so stale approvals cannot deploy."
sources: ["https://www.jenkins.io/doc/book/pipeline/syntax/#input", "https://www.jenkins.io/doc/pipeline/steps/pipeline-input-step/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Waiting for input without holding an executor

An `input` step inside `node {}` or under a top-level `agent` keeps the executor (and a Kubernetes
pod) busy for hours. Move approval outside any agent.

## Declarative: stage-level input directive
```groovy
pipeline {
  agent none
  stages {
    stage('Build') { agent { label 'linux' }; steps { sh 'make dist'; stash 'dist' } }
    stage('Deploy prod') {
      input {
        message 'Deploy to production?'
        ok 'Deploy'
        submitter 'release-managers'
        parameters { string(name: 'CHANGE_ID', description: 'Change ticket') }
      }
      options { timeout(time: 4, unit: 'HOURS') }   // covers the input wait too
      agent { label 'deploy' }                    // allocated only after approval
      steps { unstash 'dist'; sh "./deploy.sh --change ${CHANGE_ID}" }
    }
  }
}
```
The `input` directive pauses after the stage options are applied and **before** the stage agent block is entered.

## Scripted
```groovy
node('linux') { sh 'make dist'; stash 'dist' }
stage('Approve') { timeout(time: 4, unit: 'HOURS') { input message: 'Deploy?', submitter: 'release-managers' } }
node('deploy') { unstash 'dist'; sh './deploy.sh' }
```

## Supersede stale runs
Add `milestone()` before and after the approval so an older run approved later cannot deploy over a
newer one; `disableConcurrentBuilds(abortPrevious: true)` is a documented option that aborts the running build when a new one starts.

## Gotchas
- With `agent any` at pipeline level, the directive still holds that executor; use `agent none`.
- Stashes are cleared when the build completes, so a long wait keeps them around.
- Timeout expiry aborts the build; add a `post` block to notify.

## Verify
- [ ] While paused, the build executor list shows no executor for this run.

## Checked

2026-10-28. Confirmed in the Pipeline syntax page and the input step reference: the stage input directive pauses after options and before the agent block, options timeout around the stage, disableConcurrentBuilds(abortPrevious: true), top-level agents are allocated before the timeout option, milestone semantics, stash cleared when the build completes. Corrected the draft's `unless beforeInput false` remark (beforeInput controls when conditions, not agent allocation). Removed: controller-disk and ABORTED-status claims.
Method: documentation only; no commands were run.
