---
id: computing-software.devops-ci-cd.jenkins.restarting-from-a-stage
name: restarting-from-a-stage
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, restart-stage, restart-from-stage, preserve-stashes, declarative-pipeline, stash, unstash, failed-deploy-retry, top-level-stages, pipeline-durability]
level: practitioner
status: docs-checked
description: "Restart a Declarative Jenkins pipeline from a failed top-level stage: what is skipped, preserveStashes so later stages get earlier outputs, CLI/REST use and limitations."
sources: ["https://www.jenkins.io/doc/book/pipeline/running-pipelines/#restart-from-a-stage", "https://www.jenkins.io/doc/book/pipeline/syntax/#options"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restart from a stage

For a completed Declarative build, *Restart from Stage* (the build's side panel in the classic UI, or the Restart button in the Pipeline Graph View plugin) starts a **new build** (new build number) that skips every top-level stage before the
chosen one and runs from it onwards, with the same inputs: SCM information, build parameters and stash contents.

## Make later stages work: preserve stashes
Skipped stages don't run, so their workspace files don't exist (new build, maybe new
agent). Hand data forward with `stash`, and keep stashes from completed builds:
```groovy
pipeline {
  agent none
  options { preserveStashes(buildCount: 5) }      // keep stashes of the last 5 builds
  stages {
    stage('Build') {
      agent { label 'linux' }
      steps { sh 'make dist'; stash name: 'dist', includes: 'dist/**' }
    }
    stage('Deploy staging') {
      agent { label 'deploy' }
      steps { unstash 'dist'; sh './deploy.sh staging' }
    }
    stage('Deploy prod') {
      agent { label 'deploy' }
      steps { unstash 'dist'; sh './deploy.sh prod' }
    }
  }
}
```
Without `preserveStashes`, the stash is cleared when the Pipeline completes, so a restarted run cannot `unstash` it. `preserveStashes()` keeps the most recent completed build (`buildCount` default 1);
`buildCount` must be between 1 and 50 or the Pipeline fails validation.
Prefer pushing real artifacts (registry image digest, artifact repo URL) and passing the
reference; stashes are for small, short-lived files.

## Limits
- **Declarative only**, **top-level stages only**: you can't restart from a stage nested
  in `parallel` or `stages {}` inside a stage; restart from the parent.
- Only completed builds (succeeded or failed) can be restarted.
- Stages skipped because of an earlier failure cannot be chosen; stages skipped by a `when` condition can.
- The parent of parallel stages or of nested sequential stages cannot be chosen: only top-level stages.
- No Jenkinsfile configuration is needed to allow restarting.

## Verify
Fail `Deploy prod`, restart from it: the new build shows Build and Deploy staging as
skipped, `unstash 'dist'` succeeds, and only prod deploy runs.

## Checked

2026-10-28. Confirmed in the Jenkins running pipelines page and Pipeline syntax options section: restart any completed Declarative Pipeline from a top-level stage, new build number, same SCM information, parameters and stashes, classic UI side panel and Pipeline Graph View, skipped-stage rules, parent stages of parallel or nested groups not available, stash cleared on completion, preserveStashes() and preserveStashes(buildCount: 5), default 1, range 1 to 50 with a validation error. Removed: Blue Ocean wording, the exact unstash error text, environment-variable and Job/Build permission claims, and the automation/POST form paragraph.
Method: documentation only; no commands were run.
