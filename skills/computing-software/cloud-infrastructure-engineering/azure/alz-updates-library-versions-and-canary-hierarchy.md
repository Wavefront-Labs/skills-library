---
id: computing-software.cloud-infrastructure-engineering.azure.alz-updates-library-versions-and-canary-hierarchy
name: alz-updates-library-versions-and-canary-hierarchy
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, landing-zone, alz-update, alz-policy-refresh, canary-environment, alz-library, policy-as-code]
level: advanced
status: docs-checked
description: "Keep an Azure landing zone current: test platform policy and RBAC changes in a canary management group hierarchy, then promote with what-if review."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/enterprise-scale/testing-approach", "https://azure.github.io/Azure-Landing-Zones/", "https://github.com/Azure/Azure-Landing-Zones-Library", "https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-what-if"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keeping ALZ current

**Goal:** absorb changes to the landing zone platform (policy, RBAC, management groups) by testing them first, never by surprise.

## Where the reference lives
- The reference management group and policy structure for Azure landing zone is published in the Azure Landing Zones Library (GitHub repo `Azure/Azure-Landing-Zones-Library`, MIT licence, documentation on GitHub Pages).
- Read the library's release information before you take a new version into your IaC; pin the version your pipeline uses.

## Canary hierarchy (Microsoft's testing approach)
- The whole production management group hierarchy is duplicated under the Tenant Root Group. The canary name is appended to the management group display names and IDs. IDs must be unique across the Microsoft Entra tenant.
- It is for platform-level tests only: management groups, subscription placement, RBAC roles and assignments, and Azure Policy definitions, initiatives and assignments. It is not for workload dev/test environments.
- Microsoft states this is not a common pattern and is not mandatory.
- Alternative without a canary hierarchy: test in a sandbox subscription (Owner on that subscription). It cannot test inheritance from the management group hierarchy.
- If you deploy by portal, canary and production drift apart often; move to infrastructure as code.

## Implementation guidance from the page
- Use separate service principals or managed identities for the canary and production hierarchies (least privilege).
- Keep separate folders, branches or repos for canary and production IaC; apply the same branch policies, but you may reduce approvers on canary to fail fast.
- Reuse one pipeline, switching hierarchy by environment variables, or clone pipelines.
- Keep a set of canary subscriptions under a separate billing account that can be moved around the canary hierarchy.
- Keep example workload architectures to deploy into canary subscriptions and test policy/RBAC changes against.
- Send activity logs of all subscriptions, canary included, to the production Log Analytics workspace.
- Adding a canary to an existing landing zone: clone the production deployment and rename resources with the canary naming scheme.

## Promote
1. Test the change in canary.
2. Preview with what-if before each deployment; what-if supports management group deployments (`az deployment mg what-if`).
3. Promote to production using policy assignment enforcement mode, as in the Adopt policy-driven guardrails guidance.

```bash
az deployment mg what-if --template-file main.bicep
```
Add the management group, location and parameter arguments from the `az deployment mg what-if` reference.

## Gotchas
- what-if can report properties as deleted that are only defaults set during deployment ("noise").
- Use a current Azure CLI: older versions silently skip diagnostics when what-if cannot analyze part of a deployment (the page names 2.75.0 or later for the diagnostics).

## Verify
- [ ] Canary deploys clean, example workloads still deploy, production what-if reviewed, version recorded in the repo changelog.

## Checked

Method: docs-checked 2026-11-09 against the Learn testing-approach page, azure.github.io Azure-Landing-Zones, the Azure-Landing-Zones-Library repo page and the Bicep what-if page. Removed unconfirmed library_references/alz provider names, monthly What's new cadence, trigger-scan, remediation advice and the --management-group-id/--location flags on what-if.
