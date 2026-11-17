---
id: computing-software.devops-ci-cd.jenkins.input-step-submitters-and-parameters
name: input-step-submitters-and-parameters
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, input-step, input-submitter, input-parameters, manual-approval, submitterparameter, approval-gate, declarative-input, choice-parameter, beforeinput, executor-release, separation-of-duties]
level: practitioner
status: docs-checked
description: "Build Jenkins manual approval gates with input: restrict submitters to users/groups, collect parameters, record who approved, and never hold an executor while waiting."
sources: ["https://www.jenkins.io/doc/pipeline/steps/pipeline-input-step/", "https://www.jenkins.io/doc/book/pipeline/syntax/#input", "https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# input: submitters and parameters

## Declarative stage-level input (preferred)
```groovy
stage('Deploy prod') {
  agent none                       // nothing allocated while waiting
  input {
    message 'Deploy to production?'
    ok 'Deploy'
    submitter 'release-managers,alice'   // user IDs or external group names, comma-separated
    submitterParameter 'APPROVER'        // environment variable set to the submitter's name
    parameters {
      choice(name: 'REGION', choices: ['eu-west-1', 'us-east-1'], description: 'Target region')
      booleanParam(name: 'RUN_MIGRATIONS', defaultValue: true)
    }
  }
  steps {
    node('deploy') {
      echo "Approved by ${APPROVER} for ${REGION}"
      sh './deploy.sh "$REGION"'
    }
  }
}
```
Stage-level `input` is evaluated before the stage's agent is allocated. Add
`when { beforeInput true; branch 'main' }` so the condition is checked before prompting
(no prompt at all on other branches).

## Scripted
```groovy
def answer = input(message: 'Promote?', ok: 'Promote', submitter: 'release-managers',
                   submitterParameter: 'approver',
                   parameters: [string(name: 'TICKET', description: 'Change ticket')])
// with parameters + submitterParameter, answer is a Map: answer.approver, answer.TICKET
// with exactly one parameter and no submitterParameter, answer is the bare value
```
Call `input` **outside** `node {}`; inside, it holds that node's executor while waiting.

## Submitter rules
- `submitter` takes user IDs and/or external group names separated by commas; spaces are trimmed. See the input step reference for how Overall/Administer and Job/cancel permissions interact.
- Without `submitter`, any user may approve (the default), including the person who pushed the change. For separation of duties, list a group excluding
  authors, and compare `APPROVER` with the change author in the next step.
- Archive `APPROVER` into release notes or a deploy record for audits.

## Gotchas
- Clicking Abort aborts the build.
- Each input has an `id` that is used in the generated URL to proceed or abort; set an explicit `id` if an external tool must answer it (see the input step reference).

## Verify
A user not in the submitter list cannot approve;
an approved run exposes the approver and the chosen parameters.

## Checked

2026-10-28. Confirmed in the Pipeline syntax input section and the input step reference: message, id, ok, submitter (comma-separated users or external groups, spaces trimmed, default any user), submitterParameter (environment variable in the directive; return value name in the step), parameters (one parameter returns its value, several return a map, none returns nothing), stage input evaluated before the agent, beforeInput true taking precedence over beforeAgent, parameters available in the stage environment, id used in the generated URL. The draft's `no spaces` rule was wrong. Removed: the proceedEmpty REST path, CHANGE_AUTHOR, log text, Overall/Administer behaviour, per-type value claims.
Method: documentation only; no commands were run.
