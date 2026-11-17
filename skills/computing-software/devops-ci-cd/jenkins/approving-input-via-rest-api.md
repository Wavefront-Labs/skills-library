---
id: computing-software.devops-ci-cd.jenkins.approving-input-via-rest-api
name: approving-input-via-rest-api
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, input-rest-api, input-step, jenkins-cli]
level: advanced
status: docs-checked
description: "Approve or abort a paused Jenkins input step from ChatOps or scripts via the REST API: finding the input id, crumbs/API tokens, passing parameters and submitter checks."
sources: ["https://github.com/jenkinsci/pipeline-input-step-plugin", "https://github.com/jenkinsci/pipeline-stage-view-plugin/tree/master/rest-api", "https://www.jenkins.io/doc/book/security/csrf-protection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Approving input via the REST API

Give the input a stable id:
```groovy
input id: 'DeployProd', message: 'Deploy to prod?', submitter: 'release-bot,release-managers',
  parameters: [string(name: 'TICKET', defaultValue: '')]
```
The URL id is the id with the first letter capitalised: `DeployProd`.

## Discover pending inputs
```bash
curl -s -u "$USER:$API_TOKEN" "$JENKINS/job/app/job/main/42/wfapi/pendingInputActions"
```
Returns the pending inputs with id, message, `proceedUrl` and `abortUrl` (served by the Pipeline REST API plugin, part of Pipeline Stage View).

## Proceed / abort
```bash
# proceed without parameters
curl -s -X POST -u "$USER:$API_TOKEN" "$JENKINS/job/app/job/main/42/input/DeployProd/proceedEmpty"
# proceed with parameters
curl -s -X POST -u "$USER:$API_TOKEN" "$JENKINS/job/app/job/main/42/input/DeployProd/submit" \
  --data-urlencode 'json={"parameter":[{"name":"TICKET","value":"CHG-1234"}]}' \
  --data-urlencode 'proceed=Proceed'
# abort
curl -s -X POST -u "$USER:$API_TOKEN" "$JENKINS/job/app/job/main/42/input/DeployProd/abort"
```
Requests authenticated with an API token are exempt from CSRF protection; with a password you must send a crumb (from `/crumbIssuer/api/json`).

## Security
- The API user must be permitted by `submitter` (usernames and external group names, comma separated); Jenkins administrators may always respond.
- `submitterParameter: 'APPROVER'` records who approved, for audit.
- A ChatOps bot approving on behalf of humans should pass the human identity into a parameter and
  check authorisation itself; the Jenkins audit trail shows only the bot.

## Verify
- [ ] The build resumes after the call and the parameter value is available to later steps; with `submitterParameter` set, the approver name is recorded.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed: `id` is capitalised on the first letter (InputStep.java `setId`); `doProceedEmpty`, `doSubmit` (`proceed` parameter, `parameter` array of name/value read from the submitted `json` form), `doAbort` endpoints (InputStepExecution.java); `wfapi/pendingInputActions` with `proceedUrl`/`abortUrl` (pipeline-stage-view rest-api README); `submitter` and `submitterParameter` semantics (pipeline-input-step README); API-token requests exempt from CSRF protection (CSRF page).
Method: documentation only; no commands were run.
