---
id: computing-software.cloud-infrastructure-engineering.azure.well-architected-review-assessment-tool
name: well-architected-review-assessment-tool
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, well-architected, waf-assessment, review-assessment, well-architected-review, azure-advisor, milestones, recommendations, pillars, reliability, security, cost-optimization, operational-excellence, performance-efficiency, azure-review-checklists]
level: practitioner
status: docs-checked
description: "Run an Azure Well-Architected Review assessment for a workload: scope, pillar questionnaire, milestones, prioritised recommendations and re-assessment."
sources: ["https://learn.microsoft.com/en-us/assessments/azure-architecture-review/", "https://learn.microsoft.com/en-us/azure/well-architected/", "https://learn.microsoft.com/en-us/azure/well-architected/design-guides/implementing-recommendations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run a Well-Architected Review assessment

**Goal:** an evidence-backed review of one workload against the five Well-Architected pillars (reliability, security,
cost optimization, operational excellence, performance efficiency) that ends in a prioritised backlog, not a slide deck,
and is repeated to show progress.

## 1. Scope before questions
- One assessment per **workload** (an app and its dependencies, one owner), not per subscription.
- Collect up front: architecture diagram, SLO/RTO/RPO targets, criticality, compliance scope, recent incidents, cost.
- Attendees: workload owner, lead dev, ops/SRE, security.

## 2. Run the tool
1. Open Microsoft Assessments, **Azure Well-Architected Review**, sign in so progress saves.
2. The assessment contains several sub-assessments: select **Core Well-Architected Review** to evaluate the full
   workload rather than one technology.
3. Answer each question by ticking the practices actually in place; be literal, "planned" is unticked.
4. Capture decisions periodically as **assessment milestones**; the first is your baseline.
5. Recommendations can be exported to CSV and imported into an Azure DevOps or GitHub organization as work items.

## 3. From findings to backlog
- Triage with the owner: accept or reject each recommendation with a reason; rejected means documented risk
  acceptance, not silence.
- Rank by risk and effort; address reliability and security gaps (single points of failure, untested backups,
  public endpoints, secrets in config) first.
- Use the per-service Well-Architected service guides for detail the questionnaire only summarises.
- Re-run after major change and compare milestones to show trend.

## Gotchas
- Answers are self-reported; verify claims ("we test restores") with evidence before ticking.
- Tools that read deployed resources will not flag design gaps such as a missing DR region.
- Over-scoping (whole estate) produces averages nobody owns; keep it to one workload.

## Verify
- [ ] A saved baseline milestone exists with all in-scope pillars answered.
- [ ] Every critical recommendation is a work item with an owner and date, or a recorded risk acceptance.
- [ ] A later milestone shows changed results tied to completed work items.

## Checked
2026-10-28. Confirmed (Learn: assessments/azure-architecture-review, well-architected/design-guides/implementing-recommendations):
Core Well-Architected Review selection, milestones, CSV import into Azure DevOps or GitHub, the five pillars. Removed
(unconfirmed): 0-100 scoring bands, workload variant list, Advisor linking steps, time estimates, quarterly cadence,
Azure Review Checklists, "lost when browser session ends". Dead source advisor-well-architected-framework (404) dropped.
Method: documentation only; no commands were run.
