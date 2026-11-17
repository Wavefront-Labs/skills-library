---
id: computing-software.ai-ml-engineering.llm-application-engineering.ai-incident-response-and-logging
name: ai-incident-response-and-logging
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, ai-risk-management, ai-incident-response, incident-logging, manage-function, kill-switch, post-incident-review]
level: practitioner
status: docs-checked
description: "Prepare for and handle AI incidents (harmful outputs, data leaks, injection exploits, rogue agents): logging, detection, kill switches, rollback and post-incident review."
sources:
  - https://airc.nist.gov/AI_RMF_Knowledge_Base/Playbook/Manage
  - https://artificialintelligenceact.eu/article/73/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AI incident response and logging (NIST AI RMF Manage)

**Goal:** when an AI feature causes harm or misbehaves, detect it quickly, contain it, fix it, and learn - with the logs needed to understand what happened.

## What counts as an AI incident
Harmful or defamatory outputs at scale, leaks of personal/confidential data via outputs or tools, successful prompt-injection exploits, agents taking unintended actions, systematic bias discovered in decisions, major accuracy regressions after a model/provider change, copyright/IP complaints. Many are not outages - classic uptime monitoring won't catch them.

## Logging prerequisites
- Per request: timestamp, user/tenant (pseudonymised), route, model + version, prompt template version, retrieved document IDs, tool calls and results, final output, guardrail decisions, latency/cost. Traces make root-cause analysis possible.
- Retention balancing investigation needs against privacy rules; access-controlled.
- Ability to search by user, time window, prompt version, and output content.

## Detection
User reports (an in-product "report a problem" path), feedback spikes, guardrail-trigger rate changes, output classifiers on sampled traffic, tool-action anomaly alerts, monitoring of social/media mentions for public products.

## Response runbook
1. **Triage and severity** (who's affected, ongoing harm, legal/regulatory exposure).
2. **Contain:** feature flags/kill switch per AI feature; roll back prompt/model version (registry aliases make this fast); disable risky tools; tighten guardrails temporarily.
3. **Investigate** with traces: reproduce, find the triggering inputs and the failing control.
4. **Fix and verify:** add the case to the eval/red-team suites so it can't silently regress.
5. **Notify:** affected users, internal stakeholders, and regulators where required (e.g. EU AI Act Art. 73 requires providers of high-risk AI systems placed on the Union market to report serious incidents; check data protection law for personal data breaches).
6. **Post-incident review** (blameless), tracked actions, and updated risk register/impact assessment.

## Preparation
Assign an owner per AI feature, rehearse the kill switch and rollback, keep a public-facing contact path, and maintain an internal incident log.

## Verify
- [ ] Kill switch and version rollback tested for each AI feature.
- [ ] Logs sufficient to reconstruct a full request incl. retrieved context and tool calls.
- [ ] Every incident yields a new regression test case.

## Checked
2026-11-01. Confirmed: NIST AI RMF Playbook MANAGE page (contingency and deactivation processes for mission-critical AI systems, third-party monitoring); EU AI Act Art. 73 (serious-incident reporting by providers of high-risk systems). The rest is operational advice with no figures. Removed: NIST AI 600-1 and AI Incident Database sources (not read).
Method: documentation only; no commands were run.
