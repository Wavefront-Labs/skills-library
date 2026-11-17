---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.runaway-spend-protection
name: runaway-spend-protection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, anomaly-management, runaway-spend-protection, budget-actions, spending-caps, service-quotas, guardrails, automation]
level: advanced
status: draft
description: "Automate protection against runaway spend: budget actions, quota limits, policy guardrails, auto-stop for sandboxes and kill switches, scoped so production is not harmed."
sources: ["https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-controls.html", "https://cloud.google.com/billing/docs/how-to/notify", "https://learn.microsoft.com/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending", "https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automated protection against runaway spend

Alerts tell people; automation acts at 3 a.m. Use layered controls, with the strongest ones only
where stopping things is safe (sandboxes, dev, training accounts).

## Layers
1. **Preventive limits**: service quotas (EC2 vCPU, GPU instance quotas, Lambda concurrency),
   SCP / Azure Policy / Org Policy denying expensive SKUs or regions, max instance counts in
   autoscaling groups and node pools, BigQuery `maximum_bytes_billed` and custom query quotas.
2. **Budget-triggered actions**:
   - AWS Budgets actions: attach an IAM policy or SCP that denies new provisioning, or stop specific
     EC2/RDS instances, automatically or after approval.
   - Google Cloud: budget -> Pub/Sub -> Cloud Function that stops resources or, for sandboxes,
     detaches billing from the project (documented "cap costs" pattern; disabling billing stops
     services and can delete resources, so never on production).
   - Azure: budget alert -> action group -> Automation runbook / Logic App / Function to stop VMs or
     scale down; spending limits exist only on credit-based subscriptions.
3. **Usage-metric alarms** for fast signals (billing data lags hours): request rate, concurrency,
   egress bytes, log ingestion, GPU instance count; alarm actions scale down or page.
4. **Time-based auto-stop**: sandboxes and dev stop nightly; TTL tags with a reaper job.
5. **Kill switch**: a runbook and permission to disable an API key, stop a pipeline or set
   concurrency to 0 within minutes.

## Steps
1. Classify accounts: sandbox (hard actions), dev (stop + notify), production (alert + human).
2. Implement quotas and policies first; they never fire falsely on bills.
3. Add budget actions per class; test with a low threshold in a test account.
4. Add usage alarms for the known runaway paths (recursive functions, queue loops, log floods,
   public egress).
5. Document who can override and how.

## Gotchas
- Billing-based actions fire hours after the spike; combine with metric alarms.
- Detaching billing in GCP can lead to resource deletion after a grace period; use only where data
  loss is acceptable.
- Leaked credentials mining crypto will hit quota limits first: keep GPU quotas low by default.

## Verify
- [ ] Each sandbox account has a tested hard stop.
- [ ] Production has alerting, not destructive automation.
- [ ] Quotas for GPU and large instance families are set to need, not defaults raised on request.
