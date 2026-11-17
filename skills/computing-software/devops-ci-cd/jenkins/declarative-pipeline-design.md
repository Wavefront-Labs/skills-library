---
id: computing-software.devops-ci-cd.jenkins.declarative-pipeline-design
name: declarative-pipeline-design
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jenkinsfile, declarative-pipeline, when, beforeagent, beforeinput, changeset, changerequest, matrix, axes, excludes, parallel, failfast, parallelsalwaysfailfast, stash, unstash, post, post-conditions, unstable, fixed, regression, environment, credentials-helper, parameters, options, skipdefaultcheckout, script-block, method-code-too-large, cps, groovy]
level: advanced
status: docs-checked
description: "Structure non-trivial declarative Jenkinsfiles: when + beforeAgent, matrix, parallel failFast, stash vs workspace, post conditions, parameters, and avoiding script-block sprawl and size limits."
sources: ["https://www.jenkins.io/doc/book/pipeline/syntax/", "https://github.com/jenkinsci/workflow-basic-steps-plugin", "https://github.com/jenkinsci/junit-plugin", "https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declarative pipeline design

**Goal:** a Jenkinsfile that stays readable at 15+ stages, allocates agents only when a
stage will really run, and reports the right status (green / unstable / red) every time.

(The baseline Jenkinsfile, credentials quoting and the `input` executor gotcha are in
`computing-software.devops-ci-cd.jenkins.declarative-pipelines-and-administration`.)

## 1. Skeleton with the directives that matter
```groovy
pipeline {
  agent none
  parameters {
    booleanParam(name: 'RUN_E2E', defaultValue: false, description: 'Run e2e suite')
    choice(name: 'TARGET', choices: ['staging', 'prod'], description: 'Deploy target')
  }
  environment {
    REGISTRY = 'registry.example.com/team'
    NEXUS    = credentials('nexus-user-pass')   // also sets NEXUS_USR / NEXUS_PSW
  }
  options {
    skipDefaultCheckout()        // each stage checks out on its own agent
    parallelsAlwaysFailFast()
    timeout(time: 45, unit: 'MINUTES')
  }
  stages { /* ... */ }
  post {
    failure    { slackSend channel: '#ci', message: "FAILED ${env.JOB_NAME} #${env.BUILD_NUMBER}" }
    fixed      { slackSend channel: '#ci', message: "Back to green: ${env.JOB_NAME}" }
    cleanup    { echo 'runs last, always' }
  }
}
```
- `post` order: `always`, `changed`, `fixed`, `regression`, `aborted`, `failure`,
  `success`, `unstable`, `unsuccessful`, then `cleanup` last.

## 2. `when` without wasting agents
```groovy
stage('E2E') {
  when {
    beforeAgent true                       // evaluate BEFORE allocating the agent
    allOf { branch 'main'; expression { params.RUN_E2E } }
  }
  agent { label 'e2e' }
  steps { sh './e2e.sh' }
}
```
- Without `beforeAgent true` Jenkins grabs (and may spin up) the agent, then skips the stage.
- Also: `beforeInput true` (evaluate before an `input`), `beforeOptions true`.
- Handy conditions: `changeRequest()` (PR builds in multibranch), `changeRequest target: 'main'`,
  `buildingTag()`, `tag pattern: 'v\\d+.*', comparator: 'REGEXP'`, `changeset 'docs/**'`
  (matches files in the build's SCM changeset), `triggeredBy 'TimerTrigger'`.

## 3. Parallel and matrix
```groovy
stage('Test matrix') {
  matrix {
    axes {
      axis { name 'JDK'; values '17', '21' }
      axis { name 'OS';  values 'linux', 'windows' }
    }
    excludes { exclude { axis { name 'JDK'; values '17' }; axis { name 'OS'; values 'windows' } } }
    agent { label "${OS}" }
    stages { stage('Test') { steps { sh "./gradlew test -PjavaVersion=${JDK}" } } }
  }
}
```
- `failFast true` on a `parallel` (or `parallelsAlwaysFailFast()` globally) aborts siblings on first failure; turn it off for test matrices where you want every result.
- Each parallel branch occupies its own executor; 20 branches = 20 executors.

## 4. Moving files between stages/agents
- `stash name: 'dist', includes: 'build/**'` / `unstash 'dist'` — is meant for small files.
- Large outputs: push to an artifact repository and pull by version.
- `archiveArtifacts` is for humans/downloads, not inter-stage transport.

## 5. Status semantics
- `junit` with failing tests sets **UNSTABLE**, not FAILURE — decide whether that should
  block deploy (`when { expression { currentBuild.currentResult == 'SUCCESS' } }`).
- `catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') { sh ... }` marks one stage red
  but keeps the build going — for non-blocking checks.

## 6. Keep logic out of the Jenkinsfile
- Every `script { }` block is a smell beyond a few lines. Move it to a shared-library step
  (`computing-software.devops-ci-cd.jenkins.shared-libraries`).
- Groovy runs CPS-transformed on the controller: loops with heavy string processing
  are slow and hold controller CPU. Do work in `sh`, on the agent.

## Verify
- [ ] Every conditional stage with an agent has `beforeAgent true`.
- [ ] Test failures produce UNSTABLE and the deploy gate handles that explicitly.
- [ ] `stash` only for small files; big outputs go to an artifact store.
- [ ] `script {}` blocks are a few lines at most; logic lives in a library.
- [ ] `post { fixed {} }` and `failure {}` notify; `cleanup {}` frees resources.
- [ ] Jenkinsfile passes the declarative linter before merge.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed in the Pipeline Syntax reference: `post` condition list and order, `when` options `beforeAgent`/`beforeInput`/`beforeOptions`, conditions `changeRequest`, `buildingTag`, `tag`, `changeset`, `triggeredBy`, `matrix` with `axes`/`excludes`, `parallelsAlwaysFailFast`, `failFast`; `catchError` `buildResult`/`stageResult` arguments (workflow-basic-steps help); `junit` marking the build unstable on test failures (junit plugin README); Groovy runs on the controller (best-practices guide). Removed the unconfirmed method-size limit, stash-size and first-run claims.
Method: documentation only; no commands were run.
