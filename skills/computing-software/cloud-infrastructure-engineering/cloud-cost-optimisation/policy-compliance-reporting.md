---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.policy-compliance-reporting
name: policy-compliance-reporting
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-policy-governance, finops-governance, policy-compliance-reporting, tag-compliance, policy-as-code]
level: practitioner
status: docs-checked
description: "Report compliance with cloud cost policies using the FinOps Framework KPIs: adherence, guardrail effectiveness, automation coverage, breach and false positive rates."
sources: ["https://www.finops.org/framework/capabilities/policy-governance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy compliance reporting

The FinOps Governance, Policy and Risk capability asks the FinOps practitioner to develop and
maintain KPIs for policy compliance and risk posture and to share them transparently. Its
outputs include compliance KPIs and governance dashboards shared across personas.

## KPIs the Framework names
- Policy Adherence Rate: proportion of total technology spend covered by compliant resources.
- Commitment Coverage: percentage of optimised usage covered by discounted commitments.
- Guardrail Effectiveness: volume and trend of policy exceptions, overrides and non-compliant
  provisioning events.
- Risk Register Currency: proportion of identified risk categories with documented, actively
  reviewed mitigation plans.
- Zero-Utilization Remediation Rate: percentage of flagged zero-utilisation resources
  remediated in the governance window.
- Governance Automation Coverage: proportion of policies enforced by automation versus manually.
- Time to Policy Response: average time from identifying a policy gap to implementing a control.
- Violations Prevented, with the exception rate.
- Breach Rate: percentage of deployments or changes violating policy at check time.
- False Positive Rate: share of flagged violations that were not real violations.
- Service Impact: rate at which enforcement actions disrupted a legitimate deployment.

## Steps
1. For each policy, choose the KPI above that measures it, and its data source.
2. Report spend-weighted adherence (the page's Policy Adherence Rate is spend-based).
3. Set a regular governance cadence and communicate results to Leadership and stakeholders.
4. At Run maturity, monitor compliance continuously through automated systems with trend
   analysis.
5. Feed compliance gaps back into policy design and training.

## Verify
- [ ] Each active policy maps to a KPI and a data source.
- [ ] Results are shared with personas on the governance cadence.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Governance, Policy and Risk capability page (read in full). The AWS Config and Azure Policy pages were not readable and were dropped. Removed unconfirmed: the control and data source table, provider commands and services, per-team scoring, and the gotchas on count versus spend weighting and untaggable resources.
