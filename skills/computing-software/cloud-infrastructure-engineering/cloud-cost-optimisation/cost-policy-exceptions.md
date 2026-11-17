---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-policy-exceptions
name: cost-policy-exceptions
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-governance, cost-policy-exceptions, policy-waivers, exemptions]
level: practitioner
status: docs-checked
description: "Handle cost policy exceptions: documented justification and approval, a defined exception pathway, exception records and guardrail effectiveness measures."
sources: ["https://www.finops.org/framework/capabilities/policy-governance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost policy exceptions

The FinOps Governance, Policy and Risk capability treats a defined exception pathway as a
hallmark of effective governance, and lists escalation paths and exception management processes
among the capability's outputs.

## What the Framework says
- Its example governance rule: at the end of each month, teams are told of resources with zero
  utilisation, which are decommissioned automatically the following Tuesday unless a documented
  retention justification is submitted. That combines automated detection, transparent
  communication, a default action aligned to policy, and an exception pathway.
- Its example zero-utilisation policy allows an exception when a documented business
  justification is reviewed and approved by the appropriate stakeholder personas.
- At Run maturity, runtime thresholds, escalation paths and exception records feed back into the
  next design cycle.

## Steps
1. Require a documented justification for each exception and an approver from the relevant
   personas.
2. Record every exception so it is visible to automation and audit.
3. Define who escalates changes that exceed agreed thresholds.
4. Report exception volume and trend: the Guardrail Effectiveness KPI measures policy
   exceptions, overrides and non-compliant provisioning events, and Violations Prevented
   includes the exception rate.
5. Use frequent exceptions to a policy as input to revising the policy (a reasonable
   reading, not stated by the page).

## Verify
- [ ] Every exception has a justification, an approver and a record.
- [ ] Exception counts are reported to the governance forum.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Governance, Policy and Risk capability page (read in full). The Azure Policy exemption structure page and Cloud Custodian docs were not read. Removed unconfirmed: the list of valid reasons, request fields, cost-threshold approvals, exemption tag names and expiry dates, 14-day reminders, Azure `expiresOn`, Cloud Custodian tag handling and the gotchas.
