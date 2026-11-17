---
id: computing-software.cloud-infrastructure-engineering.aws.well-architected-framework-review
name: well-architected-framework-review
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, well-architected, well-architected-review, war, well-architected-tool, six-pillars, operational-excellence, security-pillar, reliability-pillar, performance-efficiency, cost-optimization, sustainability, lenses, high-risk-issues, hri, improvement-plan, milestones, architecture-review, custom-lens]
level: practitioner
status: docs-checked
description: "Run an AWS Well-Architected review that produces action: scope one workload, answer the six pillars in the WA Tool, triage high-risk issues, re-measure with milestones."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/wa-framework-review.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/define-workload.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/save-milestone.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/lens-catalog.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/definitions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Well-Architected review: a structured conversation that ends in a prioritised backlog

**Goal:** surface the high-risk issues (HRIs) across the six pillars for one workload, agree which to fix next, and
track the trend with milestones, using the AWS Well-Architected Tool (offered at no charge) so the record persists.
The Framework describes a review as a constructive conversation, not an audit.

## 1. The six pillars
Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization and Sustainability. Each
pillar has foundational questions with best-practice choices; the answers set the risk shown in the tool as a
**high risk issue (HRI)** or **medium risk issue (MRI)** (definitions on the glossary page). See the Reliability,
Security and Cost Optimization pillar skills for question-level checklists.

## 2. Preparation
- **Scope one workload**: a system with an owner, an architecture diagram, an environment list and the accounts and
  Regions it lives in. Not "the platform".
- Attendees: workload owner, lead engineer, operations or on-call, a security representative and a facilitator who is
  not the owner.
- Pull evidence beforehand so answers are factual: incident reviews, last DR test, quota alarms, deployment pipeline
  screenshots, cost reports, backup reports, security findings.
- Create the workload in the **WA Tool**:
  `aws wellarchitected create-workload --workload-name shop --environment PRODUCTION --aws-regions eu-west-1 --lenses wellarchitected --description "Shop" --review-owner owner@example.com`.
  The Framework lens is applied to all workloads by default. Share with the team (`create-workload-share`) and add
  lenses from the **Lens Catalog** (for example Serverless Applications, SaaS, Data Analytics, Machine Learning,
  Container Build, Financial Services Industry, Healthcare Industry, Government), or a **custom lens** from JSON.
  Run `aws wellarchitected list-lenses` for the current aliases.

## 3. Running the review
- Facilitator reads each question, the owner answers with evidence; select only practices that are in place and
  operating (a backup plan that has never been restored is not tested).
- Capture notes per question (`update-answer --notes`), including why a practice was skipped.
- The Trusted Advisor integration (Business and Enterprise Support customers; Framework lens only) can supply
  automated checks for some best practices when the workload's account and Regions or AppRegistry application are set.
- Cover all pillars even if the team cares about one; cross-pillar issues are common.

## 4. After: improvement plan
- The tool lists HRIs and MRIs with improvement plan text per practice (`list-lens-review-improvements`). Triage by
  impact and effort, pick a small number for the next quarter, assign owners and dates, link tickets in the notes.
  A **profile** marks which questions and risks are prioritised for your business.
- Save a **milestone** (`create-milestone --milestone-name "Q4 baseline"`); after fixes, re-answer and save another
  to compare risk counts. Milestone reports can be generated from the tool.
- Report to leadership: HRI counts by pillar, the top items with dates, and the trend since the last milestone.

## 5. Cadence and scale
- Set a cadence by workload tier (a team policy, not an AWS requirement) and review before go-live for new workloads.
- Share workloads, lenses, profiles and review templates with accounts, organisations or OUs; use the consolidated
  report (`get-consolidated-report`) to view risk across workloads. A custom lens can encode your own standards.
- AWS Well-Architected Partner program partners can help with reviews and improvements.

## Gotchas
- Answering to look good makes the tool useless; the facilitator challenges "yes" with "show me".
- A review without an owner for each HRI is a slide deck; book the follow-up in the same meeting.
- Lenses add many questions; pick the one or two that fit.
- The tool stores notes and answers only; put evidence links in the notes or they are lost.
- Do not redesign the architecture during the review; capture the HRI and move on.

## Verify
- [ ] Workload exists in the WA Tool with the right lenses, shared with the team, with no unanswered questions.
- [ ] HRI list exported; a limited set selected with owner and due date; the rest deferred with a note.
- [ ] Baseline milestone saved; a later milestone shows risk reduced.
- [ ] Evidence recorded for every "in place" practice in the security and reliability pillars.
- [ ] Next review date scheduled.

## Checked
Date: 2026-10-27. Documentation release: AWS Well-Architected Framework (published 6 November 2024), Well-Architected
Tool User Guide and API operation list, botocore wellarchitected 2020-03-31 model. Confirmed: six pillars, review
as conversation, no-charge Tool, default Framework lens, Lens Catalog names, HRI/MRI definitions, the commands
`create-workload` (required fields), `create-workload-share`, `update-answer`, `list-lens-review-improvements`,
`create-milestone`, `get-consolidated-report`, and the Trusted Advisor integration scope. Removed the "serverless"
lens alias (use `list-lenses`), question-count and timing claims, the Security Hub integration claim, and the claim
that Partner Program credits fund remediation. Replaced prose-title `sources` with real URLs.
Method: documentation only; no commands were run.
