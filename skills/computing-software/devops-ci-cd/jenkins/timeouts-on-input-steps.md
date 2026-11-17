---
id: computing-software.devops-ci-cd.jenkins.timeouts-on-input-steps
name: timeouts-on-input-steps
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, input-step, input-timeout, timeout-step, approval-expiry, auto-abort, auto-proceed, flowinterruptedexception, stale-approvals, executor-release]
level: practitioner
status: docs-checked
description: "Expire Jenkins approval prompts with timeout around input: abort vs auto-proceed patterns, telling timeout from user abort, and keeping waiting builds from blocking executors."
sources: ["https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps/#timeout-enforce-time-limit", "https://www.jenkins.io/doc/pipeline/steps/pipeline-input-step/", "https://www.jenkins.io/doc/book/pipeline/syntax/#options"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timeouts on input

An unanswered `input` waits forever. Builds pile up as *Paused for Input*, stale
approvals get clicked days later deploying old artifacts, and if `input` sits inside
`node` it holds an executor.

## Declarative: stage options
```groovy
stage('Approve prod') {
  agent none
  options { timeout(time: 4, unit: 'HOURS') }    // covers the input AND the steps
  input { message 'Deploy?'; submitter 'release-managers' }
  steps { echo 'approved' }
}
```
Stage-level `options { timeout }` wraps the stage *including* its `input` block.

## Scripted: abort on timeout
```groovy
timeout(time: 30, unit: 'MINUTES') {
  input message: 'Promote to prod?', submitter: 'release-managers'
}
```
On expiry the step throws a `FlowInterruptedException`, which aborts the build unless it is caught.

## Auto-proceed (or auto-skip) on timeout
```groovy
def approved = true
try {
  timeout(time: 15, unit: 'MINUTES') { input message: 'Hold the canary? (auto-continues)' }
} catch (org.jenkinsci.plugins.workflow.steps.FlowInterruptedException e) {
  approved = false      // timeout (or a human Abort): take the default path
}
```
This catches a human Abort as well as the timeout. Simplest rule: treat any interruption as "not approved" and move on.

## Practice
- Choose a timeout matching the change window (e.g. same working day); after it, the
  pipeline should be rerun from a fresh build so the approver sees current state.
- Pair with `milestone` so a newer build waiting for approval supersedes older ones
  (see `computing-software.devops-ci-cd.jenkins.milestone-step-ordering`).
- Notify approvers when the prompt opens, else timeouts just become failures nobody saw.

## Verify
Set a short timeout, ignore the prompt: the build is aborted (or proceeds down the default path);
click Abort on another run and confirm it is treated as a rejection.

## Checked

2026-10-28. Confirmed in the Jenkins timeout step reference, Pipeline syntax and input step pages: timeout throws org.jenkinsci.plugins.workflow.steps.FlowInterruptedException which aborts the build unless caught, the stage input directive pauses after options are applied and before the stage agent, timeout in stage options, top-level agent is allocated before the timeout option applies. Removed: the exact abort message, the ExceededTimeout cause check, BUILD_URL/input, and the activity claim.
Method: documentation only; no commands were run.
