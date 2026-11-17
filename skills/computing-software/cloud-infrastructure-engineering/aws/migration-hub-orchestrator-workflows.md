---
id: computing-software.cloud-infrastructure-engineering.aws.migration-hub-orchestrator-workflows
name: migration-hub-orchestrator-workflows
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, migration, migration-hub, migration-hub-orchestrator, migration-journeys, migration-workflow, workflow-templates, sap-migration, sql-server-rehost, mgn-rehost, migration-automation, aws-transform]
level: advanced
status: docs-checked
description: "Template and automate migration runs with Migration Hub Orchestrator: predefined and custom templates, steps and plugins, tracking, and a Step Functions fallback."
sources: ["https://docs.aws.amazon.com/migrationhub-orchestrator/latest/userguide/what-is-migrationhub-orchestrator.html", "https://docs.aws.amazon.com/migrationhub-orchestrator/latest/userguide/templates.html", "https://docs.aws.amazon.com/migrationhub-orchestrator/latest/userguide/migration-workflows.html", "https://docs.aws.amazon.com/migrationhub-orchestrator/latest/userguide/custom-templates.html", "https://docs.aws.amazon.com/migrationhub-orchestrator/latest/userguide/migrationhub-availability-change.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migration Hub Orchestrator workflows

**Goal:** every server or application in a wave is migrated with the same sequence of
steps, automated where possible and with manual steps where not, and progress is visible per workflow.

## 0. Availability
AWS Migration Hub stopped accepting new customers on November 7, 2025. Existing customers can continue to use it to
complete ongoing migration projects (including Orchestrator), no new features are being added, and AWS recommends
AWS Transform, which includes the Migration Hub capabilities. For a new project, start in AWS Transform.

## 1. Concepts
- **Template**: the predefined templates are: migrate SAP NetWeaver applications, rehost applications on EC2 (using
  Application Migration Service), rehost SQL Server on EC2 (native backup and restore), replatform SQL Server to
  Amazon RDS, replatform applications to Amazon ECS, and import VM images as AMIs; **custom templates** are made by
  modifying an AWS template and saving it.
- **Workflow**: created from a template; a template is one or more step groups with steps. Predefined templates can
  orchestrate source readiness validation, target provisioning, database and application migration, post-migration
  validation and cutover.
- **Plugin**: configured on-premises; it communicates with the source and target environments. Setup is required for
  the SAP, EC2 rehost, SQL Server rehost and SQL Server-to-RDS templates, optional for VM image import, and not needed
  for the ECS replatform template.

## 2. Run a workflow
```bash
aws migrationhub-orchestrator list-templates
aws migrationhub-orchestrator get-template --id <TEMPLATE_ID>       # inputs required
aws migrationhub-orchestrator create-workflow --name billing-app-wave3 --template-id <TEMPLATE_ID> \
  --application-configuration-id <APP_ID> --input-parameters file://inputs.json \
  --step-targets <SOURCE_SERVER_ID>
aws migrationhub-orchestrator start-workflow --id <WORKFLOW_ID>
aws migrationhub-orchestrator list-workflow-steps --workflow-id <WORKFLOW_ID> --step-group-id <GROUP_ID>
aws migrationhub-orchestrator update-workflow-step --id <STEP_ID> --step-group-id <GROUP_ID> \
  --workflow-id <WORKFLOW_ID> --status COMPLETED          # mark a manual step done
```
- Custom templates: you must first create a workflow from an AWS-provided template; then modify its steps and save the
  changes as a template for reuse. A step added without a script location is a **Manual** step that needs user
  intervention: update its status to complete for the workflow to continue. You cannot add a step to a step group whose
  status is Completed.
- A workflow can be deleted only when its status is Not started, Paused or Failed.
- Step statuses include `READY`, `IN_PROGRESS`, `COMPLETED`, `FAILED`, `PAUSED` and `USER_ATTENTION_REQUIRED`.

## Gotchas
- Orchestrator sequences migration tools such as MGN; it does not replace their setup.
- Orchestrator itself has no additional charge; you pay for the resources you provision for migrations.

## Verify
- [ ] A pilot application's workflow runs end to end in a test wave.
- [ ] Custom template saved and reused for a second application.

## Checked

2026-10-28. Confirmed against the Migration Hub Orchestrator User Guide pages what-is, templates, migration-workflows, custom-templates and the Migration Hub availability-change page (closed to new customers 7 November 2025, AWS Transform recommended), and the botocore migrationhuborchestrator StepStatus enum.
Removed: "AWS has been moving orchestration into AWS Transform" wording, the Step Functions/MGN/SSM fallback design, script-step languages (Python/PowerShell), the idempotent-step and approval advice, MAP tagging, plugin outbound HTTPS and home-Region claims, and the "failed steps are retried" claim.
Method: documentation only; no commands were run.
