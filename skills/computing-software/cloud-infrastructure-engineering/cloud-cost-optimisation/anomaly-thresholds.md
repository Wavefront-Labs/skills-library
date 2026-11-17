---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.anomaly-thresholds
name: anomaly-thresholds
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-anomaly-detection, anomaly-thresholds, alert-routing, monitors, alert-fatigue, absolute-and-percentage-threshold, cost-monitor-design]
level: practitioner
status: docs-checked
description: "Tune cost anomaly monitors so alerts are actionable: monitor scope per owner, combined absolute and percentage thresholds, routing to the owning team, and fatigue reviews."
sources: ["https://www.finops.org/framework/capabilities/anomaly-management/", "https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html", "https://learn.microsoft.com/azure/cost-management-billing/understand/analyze-unexpected-charges"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anomaly thresholds and routing

## Steps
1. **Scope monitors to owners**: AWS Cost Anomaly Detection can evaluate all services independently
   or specific member accounts, cost allocation tags or cost categories, so use one monitor per team
   plus a catch-all service-level monitor for the whole org owned by FinOps.
2. **Combine thresholds**: alert when impact is above both an absolute amount and a percentage
   (illustrative values: $100/day and 20%; choose your own). The FinOps Anomaly Management page names
   percentage-of-spend-change and single-item spend ceilings as context-relevant thresholds and says to
   set them with stakeholders. Absolute alone tends to spam big teams; percentage alone tends to spam
   tiny accounts, so scale the absolute value with team spend.
3. **Route** to the owning team, not a central inbox (the FinOps page lists automatic routing to
   responsible teams as a more mature practice). Include: service, account, region, usage type, top
   resources, link to dashboard and runbook. AWS root-cause detail is ranked by dollar impact across
   service, account, Region and usage type; AWS alerts go to email or an SNS topic that can map to
   chat. Azure anomaly alerts are emails sent once at detection, limited to five alert rules per subscription.
4. **Frequency and personas**: the FinOps page says alert thresholds and notification frequency can differ for
   leadership, FinOps, engineering and finance; agree them with each group.
5. **Review regularly**: alerts fired, % actioned, false positives; the FinOps page asks teams to
   document false positives, and to update thresholds in line with service lifecycles.
   Target: most alerts lead to an action or a documented "expected".

## Expected events
Tell responders about planned launches, migrations and load tests in advance (the FinOps page lists
proactively alerting other personas to planned large spend such as a new environment launch).

## Gotchas
- ML monitors need history. AWS: a new monitor can take 24 hours to start detecting, a new service
  subscription needs 10 days of usage history, and detection can lag usage by up to 24 hours because it
  uses Cost Explorer data. Azure compares each day with a forecast from the last 60 days and runs 36 hours
  after the end of the day (UTC).
- Cost-based alerts are late by design; add usage-based alerts for fast spenders.
- AWS Cost Anomaly Detection does not monitor most AWS Marketplace products; use AWS Budgets for those.
- Thresholds set once and never revisited as spend grows.

## Verify
- [ ] Every team has a monitor routed to a channel they watch.
- [ ] Monthly alert review shows action rate.

## Checked
Date: 2026-11-08. Confirmed against the FinOps Anomaly Management capability page, the AWS Cost Anomaly Detection
overview and the Azure Cost Management anomaly article. Corrected the AWS history claim (10 days applies to a new
service subscription, 24 hours to a new monitor) and removed the unsupported immediate-versus-digest frequency
advice. The AWS alert-preferences sub-pages were not read.
Method: documentation only; no commands were run.

Related: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-anomaly-detection
