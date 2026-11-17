---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.runbooks
name: runbooks
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, operational-excellence, runbooks, playbooks, runbook-automation, incident-response]
level: practitioner
status: docs-checked
description: "Write alert-linked playbooks and runbooks, keep them current as the system changes, and turn deterministic command lists into automation such as AWS Systems Manager Automation."
sources: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html", "https://sre.google/workbook/on-call/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runbooks and playbooks

The Google SRE workbook (chapter on on-call) describes playbooks as high-level instructions on
how to respond to automated alerts: they explain the alert's severity and impact and include
debugging suggestions and possible actions to mitigate and resolve. In SRE, whenever an alert is
created, a corresponding playbook entry is usually created; the book says these guides reduce
stress, mean time to repair (MTTR) and the risk of human error.

## Practices
- **Every alert gets a playbook entry**; new alerts are reviewed like new code, and paging alerts
  should link to relevant monitoring consoles.
- **Decide what a playbook must contain.** The workbook calls content a contentious topic: some SREs
  keep entries general (one entry for all "RPC Errors High" alerts, read alongside an architecture
  diagram) so they change slowly; others write step-by-step guides to reduce human variability and
  MTTR. Agree minimal structured details with the team and notice when entries accumulate much
  more.
- **Keep them current.** Details go out of date at the rate the production environment changes
  (for daily releases, on any given day). The on-call engineer should update the entry with fresh
  information when the corresponding page fires.
- **Automate deterministic lists.** If a playbook is a deterministic list of commands run every
  time an alert fires, the workbook recommends implementing automation. Turn hard-won production
  knowledge into automation or monitoring consoles.

## Automation with AWS Systems Manager
In Systems Manager, an Automation runbook defines the actions performed on managed nodes and AWS
resources. Runbooks use YAML or JSON, with steps and parameters; steps run in sequence. Pre-defined
runbooks exist (for example restarting instances or creating an AMI) and you can write custom ones.
Useful features named on the page:
- Rate controls: a concurrency value and an error threshold for running across a fleet.
- Approvals: for example the AWS-UpdateCloudFormationStackWithApproval runbook.
- Input constraints in custom runbooks via allowedPattern and allowedValues.
- Script steps (aws:executeScript runs Python or PowerShell), with output sendable to CloudWatch Logs.
- Access control through IAM policies; EventBridge rules can trigger runbooks.
- Quotas stated on the page: 100 simultaneous automations per account, 5,000 queued; 25
  simultaneous rate control automations, 1,000 queued. Check the page for current values.

## Gotchas
- Playbooks drift from the production environment; assign owners and update after each use.
- Mixing diagnosis, deterministic commands and tribal knowledge in prose; split deterministic
  steps out into automation.

## Verify
- [ ] Every paging alert has a playbook entry linked from the alert.
- [ ] The on-call engineer updates the entry when it is used.

## Checked
2026-11-08. Confirmed against the Google SRE workbook on-call chapter (playbook purpose, one entry
per alert, maintenance debate, automation recommendation; read the playbook passages, not the
whole 67k page) and the AWS Systems Manager Automation page (runbook definition, features and
quotas). Removed: the AWS Well-Architected "use runbooks" page and its runbook-versus-playbook
distinction (the page returned empty), the 15-minute escalation, 6-month retest and 100%-coverage
figures, and the Azure Automation comparison (no source).
Method: documentation only; no commands were run.
