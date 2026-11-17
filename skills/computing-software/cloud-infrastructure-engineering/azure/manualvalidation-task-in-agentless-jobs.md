---
id: computing-software.cloud-infrastructure-engineering.azure.manualvalidation-task-in-agentless-jobs
name: manualvalidation-task-in-agentless-jobs
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, environments-approvals, manual-validation, agentless-jobs, approvals, server-jobs]
level: practitioner
status: docs-checked
description: "Pause a YAML pipeline for human sign-off with ManualValidation in an agentless job: notify users, set timeout and default action, and restrict approvers."
sources: ["https://learn.microsoft.com/azure/devops/pipelines/tasks/reference/manual-validation-v1", "https://learn.microsoft.com/azure/devops/pipelines/process/phases#server-jobs", "https://learn.microsoft.com/azure/devops/pipelines/process/approvals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ManualValidation in agentless jobs

**Goal:** a mid-pipeline human check (for example verify a migration dry-run output) without holding an agent.

## Use
```yaml
- stage: Prod
  jobs:
  - job: waitForValidation
    displayName: Wait for DBA sign-off
    pool: server                       # agentless job
    timeoutInMinutes: 4320             # job timeout; raise it above the 60-minute agentless default
    steps:
    - task: ManualValidation@1
      timeoutInMinutes: 1440           # 1 day
      inputs:
        notifyUsers: |
          dba-team@contoso.com
          [Contoso]\Release Approvers
        approvers: '[Contoso]\Release Approvers'
        allowApproversToApproveTheirOwnRuns: false
        instructions: 'Review the dry-run artifact, then Resume or Reject.'
        onTimeout: reject              # or resume
  - job: migrate
    dependsOn: waitForValidation
    steps: [ { script: ./migrate.sh } ]
```

## Behaviour
- Runs only in **agentless** (`pool: server`) jobs; costs no agent time while waiting.
- Approver clicks **Resume** or **Reject** on the run; reject fails the job.
- `approvers` lists who may act; `allowApproversToApproveTheirOwnRuns` is a task input.
- The task resumes or rejects on timeout (`onTimeout`, default reject) after the task timeout or 30 days, whichever is earlier; the maximum time for a server job is 30 days (default agentless job timeout is 60 minutes).

## ManualValidation vs environment approvals
| | ManualValidation | Environment approval check |
|---|---|---|
| Defined in | YAML (pipeline author controls) | Environment settings (resource owner controls) |
| Position | Anywhere between jobs | Before a deployment job targeting the environment |
| Tamper resistance | Author can remove it in a PR | Pipeline author cannot bypass |
Use environment approvals for compliance gates; ManualValidation for workflow pauses.

## Verify
- [ ] Run pauses with a "Waiting for validation" banner; reject stops the following job.

## Checked

2026-10-28. Confirmed on the ManualValidation@1 reference and server jobs pages: only in agentless jobs of YAML pipelines, onTimeout reject or resume with default reject, 30 day cap, 60 minute default agentless job timeout. Removed: the claim about who can resume without approvers. The environment-approval comparison table is design guidance.

Method: documentation only; no commands were run.
