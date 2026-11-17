---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-dashboard-variables-and-cross-account-dashboards
name: cloudwatch-dashboard-variables-and-cross-account-dashboards
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch-dashboards, dashboard-variables, cross-account-dashboard, dashboard-as-code, oam]
level: practitioner
status: docs-checked
description: "Build reusable CloudWatch dashboards: property and pattern variables with dropdowns, dashboards as JSON in code, and cross-account cross-region widgets via observability links."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_dashboard_variables.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-dashboard-sharing.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Cross-Account-Cross-Region.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudWatch dashboard variables and cross-account dashboards

## Variables
One dashboard serves every instance/function/table instead of one dashboard per resource.
- **Property variable:** changes a dimension value in every widget (e.g. `FunctionName`).
- **Pattern variable:** replaces a string in widget JSON (e.g. a region or name prefix) via regex.
Dashboard body snippet:
```json
"variables": [{
  "type": "property", "property": "FunctionName", "inputType": "select",
  "id": "fn", "label": "Function", "defaultValue": "orders-api", "visible": true,
  "search": "{AWS/Lambda,FunctionName} MetricName=\"Invocations\"",
  "populateFrom": "FunctionName"}]
```
- `inputType`: `input` (free text), `select` (dropdown), `radio`.
- Values from a static list or a metric `search` so new resources appear automatically.
- People you share a dashboard with cannot change the variable values.

## Dashboards as code
```bash
aws cloudwatch get-dashboard --dashboard-name service --query DashboardBody --output text > service.json
aws cloudwatch put-dashboard --dashboard-name service --dashboard-body file://service.json
```
Keep the JSON in git; `put-dashboard` replaces the entire contents of an existing dashboard.

## Cross-account and cross-region
- AWS recommends **cross-account observability** (a sink in the monitoring account, links from sources) for cross-account metrics, logs and traces within a Region; widgets can carry an `accountId` field in each metric of the metrics array.
- The older cross-account cross-Region console feature uses sharing accounts and a monitoring account (with a `CloudWatch-CrossAccountSharingRole` in each sharing account); it gives no cross-account log visibility and cannot create alarms on metrics in other accounts or Regions.
- Region per widget: `"region": "us-east-1"` sets the Region of a widget's metrics.

## Sharing
- A dashboard can be shared publicly (anyone with the link), with specific people by email, or through single sign-on (integrated with Amazon Cognito). Sharing creates Amazon Cognito and IAM resources (Cognito resources in US East (N. Virginia)) that must not be modified, and a public link grants the permissions to everyone who has it, so review what metrics and log widgets expose.

## Gotchas
- A dashboard body holds 0 to 500 widget objects; large dashboards load slowly, so split by audience.

## Verify
- [ ] Switching the variable updates all widgets.
- [ ] A widget shows metrics from another account/region in the monitoring account.

## Checked
Checked 2026-10-27 against the live CloudWatch docs (current release).
- Dashboard variables page and the dashboard body structure reference: property and pattern variables, inputType input, select and radio, search and populateFrom, defaultValue, visible, 0 to 500 widgets, accountId and region fields; shared dashboards cannot switch variable values.
- Dashboard sharing page: public, email and SSO options, Cognito integration and resources in US East (N. Virginia). Cross-account cross-Region console page: sharing role, no log visibility, no cross-account alarms, recommendation of cross-account observability.
- botocore cloudwatch: get-dashboard and put-dashboard commands.
- PutDashboard API reference: an update replaces the entire dashboard contents.
- Removed unconfirmed claims: the var- URL parameter, the search result cap, the CDK Dashboard remark, the log widget cost remark, the us-east-1 metric examples.

Method: documentation only; no commands were run.
