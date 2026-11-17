---
id: computing-software.devops-ci-cd.gitlab-ci.compliance-frameworks
name: compliance-frameworks
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, compliance-framework, compliance-frameworks, framework-labels, policy-scope-frameworks]
level: advanced
status: gated
description: "Use GitLab compliance frameworks to label projects and scope policies and compliance reporting."
sources: ["https://docs.gitlab.com/user/compliance/compliance_center/compliance_frameworks_report/", "https://docs.gitlab.com/user/group/compliance_frameworks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compliance frameworks

A compliance framework is a label applied to projects (for example SOX, PCI, HIPAA), and policies and reports can select projects by it (gated: unconfirmed, source is paywalled or blocked).

## 1. Create and apply
Frameworks are managed in the Compliance center: from the group, select Secure > Compliance center, then the Frameworks tab, and use the create-framework option (see the compliance frameworks report page). The report is available on GitLab Premium and Ultimate.

## 2. Use as policy scope
Policies can be scoped to projects with a given framework through `policy_scope.compliance_frameworks` (gated: unconfirmed, source is paywalled or blocked). Check the policy documentation for each policy type.

## Verify
- [ ] The compliance frameworks report lists every in-scope project with the framework.
- [ ] A pipeline in a framework project contains the policy jobs.

## Checked
2026-10-28. Confirmed on the compliance frameworks report page: the Compliance center is reached via Secure > Compliance center with a Frameworks tab, and the report is a Premium and Ultimate feature.
Gated: the framework definition at group level, policy scoping by framework and the `policy_scope` key come from the main compliance frameworks page, which returned a sign-in redirect (403) and could not be read.
Removed (not confirmed): GraphQL mutation, pipeline execution policy YAML, requirements and controls text, the deprecated compliance pipeline remark, and the role and audit-event gotchas.

Method: documentation only; no commands were run.
