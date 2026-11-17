---
id: computing-software.devops-ci-cd.release-engineering.soc2-change-management-evidence
name: soc2-change-management-evidence
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, soc2-change-management, compliance-evidence, change-approval]
level: advanced
status: gated
description: "Satisfy SOC 2 change management (CC8.1) with pipeline evidence: peer review, tested before deploy, authorised deployers, emergency changes, and sampling-ready records."
sources: ["https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services", "https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SOC 2 change management evidence

SOC 2 Common Criteria **CC8.1**: changes to infrastructure and software are authorised, designed,
developed, configured, documented, tested, approved and implemented. (gated: unconfirmed, source is paywalled or blocked) Auditors sample changes in
the period and ask for evidence of each control.

## Controls that map cleanly to CI/CD
| Control | Evidence |
|---|---|
| Every production change is peer-reviewed | branch protection/rulesets requiring 1+ approval, no self-approval; PR records |
| Changes are tested before deployment | required status checks; pipeline logs/test reports linked from the deployment |
| Only authorised personnel deploy | environment protection, deploy via pipeline only, no direct prod access (IAM) |
| Separation of duties | author cannot approve own PR; deploy approvals by a different person where required |
| Emergency changes documented and reviewed after | hotfix label + retroactive review ticket within N days |
| Infrastructure changes follow same process | Terraform via PR + plan in pipeline |

## Make sampling painless
- Deployment record per production deploy: commit SHA, PR link, approvers, pipeline run, who
  triggered, timestamp. Export monthly.
- Population report: list of all prod deployments in the audit period; auditors sample from it.
- Exceptions report: bypasses of branch protection, admin merges.

## Gotchas
- Admin bypasses and force-pushes break the control; restrict and log them.
- Bots merging dependency updates count as changes: document the automated-approval policy.

## Verify
- [ ] For any random prod deployment you can produce PR, approval, tests and deployer within 5 minutes.

## Checked

2026-10-28. The CC8.1 wording is from the AICPA Trust Services Criteria, which sit behind a download form: gated: unconfirmed, source is paywalled or blocked. Removed: the named export sources (GitHub deployments API, GitLab audit events, Argo CD history) and the rulesets bypass log reference.

Method: documentation only; no commands were run.
