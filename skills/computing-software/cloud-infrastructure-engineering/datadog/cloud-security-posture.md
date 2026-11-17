---
id: computing-software.cloud-infrastructure-engineering.datadog.cloud-security-posture
name: cloud-security-posture
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, cspm, misconfigurations, compliance-frameworks, cloud-security]
level: practitioner
status: docs-checked
description: "Review compliance findings and misconfigurations with Datadog Cloud Security, then triage and remediate."
sources: ["https://docs.datadoghq.com/security/cloud_security_management/misconfigurations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Security misconfigurations
Goal: find insecure cloud configuration.

Workflow in the Datadog UI:

```
Overview page            -> posture summary
Misconfigurations Findings page -> resource detail, applied rules, tags, history
Compliance reports       -> pass/fail per control in a framework
Notification rules       -> Slack, email, PagerDuty, webhooks and more
```

- Resources are evaluated in increments between 15 minutes and 4 hours depending on type. New misconfigurations are generated when a scan completes, and history is kept for the past 15 months.
- More than 1,000 out-of-the-box compliance rules map to controls in frameworks and benchmarks such as PCI and SOC2. New default rules are imported automatically; you can customise rules and create custom rules.
- Compliance reports show resources with the most failed misconfigurations, pass/fail counts per resource and the top three high-severity rule failures.
- Notification rules can use template variables and Markdown, and trigger by severity and rule type.
- A finding shows resource configuration, the compliance rules applied and tags about owner and location. An accepted risk can be muted for a period up to indefinite.
- Remediation options: create a ticket and assign a team; use Workflow Automation for automated remediation (with or without a human); for supported Terraform resources, locate the file and line, find code owners and generate a GitHub pull request with the fix.

Gotcha: muting can last indefinitely, so a mute with no end hides the finding; choose the mute period deliberately.

## Verify
- A known misconfigured resource appears on the Findings page after the next evaluation interval for its resource type.

## Checked
2026-11-09. Confirmed against the Cloud Security Misconfigurations overview (evaluation interval range, 15-month history, rule count and frameworks, custom rules, reports, notification channels and customisation, mute, remediation options). Removed: the filter string `severity:high status:fail resource_type:aws_s3_bucket` and grouping/Mute-with-reason menu details, the `Security > Cloud Security > Misconfigurations` path, the CIS framework name, the integration and resource-collection prerequisite claim, "use auto-remediation only after review", and the tag-based owner, time-to-remediate, re-scan and public-bucket test advice.
Method: documentation only; no commands were run.
