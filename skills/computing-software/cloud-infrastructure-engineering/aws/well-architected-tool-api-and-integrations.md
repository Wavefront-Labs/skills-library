---
id: computing-software.cloud-infrastructure-engineering.aws.well-architected-tool-api-and-integrations
name: well-architected-tool-api-and-integrations
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, well-architected, wa-tool-api, wellarchitected-api, jira-integration, consolidated-report, trusted-advisor-integration]
level: practitioner
status: docs-checked
description: "Automate Well-Architected reviews with the WA Tool API: workloads, answers, improvements, milestones, consolidated reports, and Jira and Trusted Advisor links."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/APIReference/API_Operations.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/jira.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/configuring-jira.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/activate-integrations.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/activate-ta-for-workload.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/activate-appregistry.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Well-Architected Tool API and integrations

## Core API calls
```bash
aws wellarchitected create-workload --workload-name orders --environment PRODUCTION \
  --aws-regions eu-west-1 --lenses wellarchitected serverless --review-owner team@example.com \
  --description "Orders service" --account-ids <ACCOUNT_ID>
aws wellarchitected list-answers --workload-id "$WL" --lens-alias wellarchitected --pillar-id security \
  --query 'AnswerSummaries[?Risk==`HIGH`].[QuestionId,QuestionTitle]'
aws wellarchitected update-answer --workload-id "$WL" --lens-alias wellarchitected \
  --question-id <QUESTION_ID> --selected-choices <CHOICE_ID> --notes "Evidence: <link>"
aws wellarchitected list-lens-review-improvements --workload-id "$WL" --lens-alias wellarchitected
aws wellarchitected create-milestone --workload-id "$WL" --milestone-name "2026-Q4"
aws wellarchitected get-lens-review-report --workload-id "$WL" --lens-alias wellarchitected   # Base64String
aws wellarchitected get-consolidated-report --format JSON     # metrics across workloads
```
- Required on `create-workload`: `WorkloadName` (3-100 characters), `Description` (3-250), `Environment`
  (`PRODUCTION` or `PREPRODUCTION`), `Lenses`; the CLI generates the client request token.
- `Risk` on an answer summary is one of `UNANSWERED`, `HIGH`, `MEDIUM`, `NONE`, `NOT_APPLICABLE`. `list-answers`
  returns at most 50 per page and `QuestionPriority` can filter to `PRIORITIZED`.
- Question and choice ids are lens-specific; read them with `list-answers` or `get-answer` rather than guessing.
- `get-lens-review` returns `RiskCounts` per lens and per pillar (`PillarReviewSummaries`), plus
  `PrioritizedRiskCounts`; use it for dashboards. `get-consolidated-report` takes `PDF` or `JSON`, pages up to 15
  workloads per call, and `IncludeSharedResources`.
- Use cases: create workloads from a service catalogue, nightly export of risk counts to a dashboard, a pipeline
  gate on open high risks.
- Workload and lens shares are available through `create-workload-share` and `create-lens-share`.

## Integrations
| Integration | What it gives |
|---|---|
| **Jira** connector | syncs improvement items to Jira: Epic per workload, Task per question, Sub-task per best practice, Label per pillar; only scrum and kanban projects; automatic or manual sync, set at account level with a per-workload override |
| **Trusted Advisor** | per-workload, for Business and Enterprise Support customers; checks map to Well-Architected Framework best practices, and only for that lens, not other lenses |
| **AppRegistry** | an application ARN on the workload defines its resources |
```bash
aws wellarchitected update-workload --workload-id "$WL" \
  --discovery-config TrustedAdvisorIntegrationStatus=ENABLED,WorkloadResourceDefinition=WORKLOAD_METADATA,APP_REGISTRY \
  --applications <APP_REGISTRY_APPLICATION_ARN>
```
- `WorkloadResourceDefinition` values are `WORKLOAD_METADATA` and `APP_REGISTRY` (console: Workload Metadata,
  AppRegistry, All); a workload accepts at most one application.
- Jira settings are in `JiraConfiguration` on create/update: `IssueManagementStatus` (`ENABLED`, `DISABLED`,
  `INHERIT`), `IssueManagementType` (`AUTO`, `MANUAL`) and `JiraProjectKey`.
- The Trusted Advisor integration needs an IAM role created for the workload owner; owners of other associated
  accounts must create a role in IAM, or the tool shows an error for that account.

## Reporting pattern
1. A scheduled Lambda lists workloads and pulls `RiskCounts` per pillar and lens into S3.
2. Athena or QuickSight dashboard: high risks by business unit, trend by milestone.
3. The Jira integration keeps remediation in team backlogs.

## Gotchas
- Review templates and shares are Region-scoped: the user guide says a review template can be shared within the
  same AWS Region only.
- Reports contain sensitive weaknesses; restrict `wellarchitected:Get*` and S3 exports.

## Verify
- [ ] Nightly export job produces risk counts for all workloads.
- [ ] Jira shows improvement items linked to the workload.

## Checked
Date: 2026-10-27. Documentation release: AWS Well-Architected Tool User Guide and API Reference (latest) and
botocore wellarchitected 2020-03-31 model. Confirmed: required `CreateWorkload` fields and limits, environment enum,
`Risk` enum, `ListAnswers` paging, `DiscoveryConfig` shape and `DefinitionType` values, Jira configuration
enums and structure, Trusted Advisor support-plan and lens restriction, consolidated report parameters, and the
operations list. Replaced made-up question and choice ids with placeholders, removed the unverified "Security
Hub / other" integration row, and replaced prose-title `sources` with real URLs.
Method: documentation only; no commands were run.
