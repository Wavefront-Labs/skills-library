---
id: computing-software.devops-ci-cd.jenkins.error-handling-in-scripted-pipelines
name: error-handling-in-scripted-pipelines
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, scripted-pipeline, scripted-try-catch, error-step, try-catch-finally, catcherror, warnerror, unstable-step, currentbuild-result, flowinterruptedexception, abort-handling, retry-step, groovy]
level: practitioner
status: docs-checked
description: "Handle failures in scripted Jenkins pipelines: try/catch/finally, error and unstable steps, catchError/warnError, setting currentBuild.result, and not swallowing aborts."
sources: ["https://github.com/jenkinsci/workflow-basic-steps-plugin", "https://github.com/jenkinsci/workflow-step-api-plugin", "https://github.com/jenkinsci/workflow-durable-task-step-plugin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error handling in scripted pipelines

## 1. The canonical shape
```groovy
node('linux') {
  try {
    stage('Build') { sh 'make build' }
    stage('Test')  { sh 'make test' }
    currentBuild.result = 'SUCCESS'
  } catch (org.jenkinsci.plugins.workflow.steps.FlowInterruptedException e) {
    currentBuild.result = 'ABORTED'   // user abort / timeout / milestone superseded
    throw e                           // never swallow: let Jenkins finish aborting
  } catch (err) {
    currentBuild.result = 'FAILURE'
    echo "Build failed: ${err}"
    throw err                         // re-throw so the build is marked failed
  } finally {
    junit allowEmptyResults: true, testResults: '**/target/surefire-reports/*.xml'
    cleanWs()
  }
}
```
- `catch (err)` with no type catches everything, including build interruptions; handle
  `FlowInterruptedException` first (it is what `timeout` throws when the limit is reached).
- `finally` also runs when the build is aborted; keep it short.

## 2. Steps for failing on purpose
| Step | Effect |
|---|---|
| `error 'message'` | signals an error without printing a stack trace |
| `unstable 'message'` | prints the message and sets the build and stage result to UNSTABLE, continues |
| `catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') { sh '...' }` | if the body throws, sets the build and stage results and continues after the step |
| `warnError('lint failed') { sh '...' }` | equivalent to `catchError(message: ..., buildResult: 'UNSTABLE', stageResult: 'UNSTABLE')` |
| `retry(3) { sh '...' }` | re-runs the block up to N times on exception; a failure on the last attempt aborts the build unless caught; user aborts are not caught |

`catchError` is preferred over try/catch for "record failure but keep going" because it sets
a stage result that visualizations can display. Its `buildResult` can only make the build
result worse (it cannot change UNSTABLE to SUCCESS).

## 3. Exit codes without exceptions
```groovy
def rc = sh(script: 'terraform plan -detailed-exitcode', returnStatus: true)
if (rc == 1) { error 'plan failed' }
def hasChanges = (rc == 2)
```
With `returnStatus: true` the `sh` step returns the exit status instead of failing on non-zero; you must check `rc` yourself.

## 4. Gotchas
- Swallowing an exception without re-throwing marks the build green. Every catch must
  either re-throw, call `error`, or set `currentBuild.result` explicitly.
- `timeout(time: 10, unit: 'MINUTES')` throws FlowInterruptedException when the limit is reached; if you
  catch it as a generic failure, timeouts look like test failures.

## Verify
Force each path: `sh 'exit 1'` (FAILURE, finally ran), wrap in `catchError` (the next stage ran and the
result is the one you configured), click Abort (ABORTED, not FAILURE).

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed in workflow-basic-steps help texts and workflow-step-api source: `error`, `unstable`, `catchError` (`buildResult`, `stageResult`, build result can only get worse), `warnError` equivalence, `retry` semantics, `timeout` throwing `org.jenkinsci.plugins.workflow.steps.FlowInterruptedException`; `returnStatus` of `sh` (workflow-durable-task-step help). Removed unconfirmed claims about script approval, `currentBuild.result` monotonicity and exception class hierarchy.
Method: documentation only; no commands were run.
