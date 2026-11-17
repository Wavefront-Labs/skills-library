---
id: computing-software.qa-testing-engineering.test-case-design.jira-bug-workflow-configuration
name: jira-bug-workflow-configuration
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [jira-bug-workflow, jira, defect-workflow, defect-lifecycle, defect-management]
level: practitioner
status: draft
description: "Configure a Jira bug workflow: statuses and transitions, resolutions, required fields, screens, validators and automation rules for triage and retest."
sources:
  - https://support.atlassian.com/jira-cloud-administration/docs/manage-issue-workflows/
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configuring a Jira bug workflow and fields

**Goal:** a defect lifecycle that matches how the team works, captures what triage needs, and keeps metrics clean.

## Lean workflow
`Open -> Triaged -> In Progress -> In Review -> Ready for Test -> Closed`, with `Reopened` back to In Progress and a direct `Open -> Closed` for rejections.

- Use **resolutions** for why it closed: Fixed, Won't Fix, Duplicate, Cannot Reproduce, Not a Bug, Works as Designed. Do not create statuses for these; statuses are where work is, resolutions are outcome.
- Set the resolution via a transition screen or post function on transitions to Closed; clear it on Reopen (post function "Clear field value: Resolution"), otherwise reopened bugs still count as resolved.

## Fields
Required on create: summary, environment, affected version, steps, expected/actual, severity. Custom fields: Severity (separate from Priority), Found in phase/environment, Root cause category (set at close), Component.
Keep the create screen short; add fields on transition screens (root cause at Close).

## Validators and conditions
- Validator on "Ready for Test": Fix Version required.
- Validator on Close with resolution Duplicate: an "is duplicated by"/"duplicates" link must exist.
- Condition: only the reporter's group or QA can transition Ready for Test -> Closed.

## Automation (Jira Automation rules)
- When a PR merges with the issue key: transition to Ready for Test.
- Bug in Ready for Test for 3 days: notify QA channel.
- New bug with severity Critical: page on-call or post to incident channel.

## Admin path
Settings > Issues > Workflows (company-managed) or project settings > Workflows (team-managed); associate via the workflow scheme for issue type Bug.

## Verify
A test bug can go through every transition, resolutions set and clear correctly, validators block missing fields, and the Created vs Resolved report matches expectations.
