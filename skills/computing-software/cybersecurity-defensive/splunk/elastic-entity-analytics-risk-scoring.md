---
id: computing-software.cybersecurity-defensive.splunk.elastic-entity-analytics-risk-scoring
name: elastic-entity-analytics-risk-scoring
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [elastic-security, entity-risk-scoring, entity-analytics, asset-criticality, risk-scoring, ueba]
level: practitioner
status: docs-checked
description: "Configure Elastic Security entity risk scoring: how scores and levels are computed, turning on the risk engine, and assigning asset criticality singly or by CSV import."
sources: ["https://www.elastic.co/guide/en/security/current/entity-risk-scoring.html", "https://www.elastic.co/guide/en/security/current/asset-criticality.html", "https://www.elastic.co/guide/en/security/current/turn-on-risk-engine.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Elastic entity analytics and risk scoring

## How scores are calculated (Elastic's docs)
- The risk scoring engine runs hourly and aggregates Open and Acknowledged alerts from the last 30 days, including building block alerts, up to 10,000 alerts per entity. Closed alerts and extra KQL filters are optional when you turn scoring on, as is a different date range.
- Alert risk scores (`kibana.alert.risk_score`) are aggregated per entity; higher-scoring alerts contribute more. The result is the Alerts category in the entity's risk summary.
- Asset criticality then adjusts the score using default risk weights: Low impact 0.5, Medium impact 1, High impact 1.5, Extreme impact 2. Without a criticality level the score equals the aggregated alert score. The page notes levels and weights are subject to change. Other inputs (privileged user status, or watchlist membership in newer versions) also apply depending on version.
- One score of 0-100 results, mapped to a level: Unknown below 20, Low 20-40, Moderate 40-70, High 70-90, Critical above 90.
- Every hourly calculation is retained and independent of earlier ones, so you can inspect an entity's score over time.
- Results go to the `risk-score.risk-score-<space-id>` data stream alias; the latest score per entity to `risk-score.risk-score-latest-<space-id>`. Alerts are read from `.alerts-security.alerts-<space-id>`, criticality from `.asset-criticality.asset-criticality-<space-id>`.
- In the newer docs only entities that exist in the entity store receive a score.
- Residual scores: if all of an entity's alerts are closed or fall outside the date range, the score resets to zero by default; tick "Retain last calculated risk scores" to keep it. In versions 9.1 and earlier residual scores are retained by default.

## Turn on
1. Open the Entity Analytics management page (Security solution view: Stack Management > Entity Analytics; Classic view: Manage > Entity Analytics).
2. Turn the toggle on (it activates risk scoring and the entity store), choose whether to retain last scores, optionally set a date range, whether to include closed alerts, and a KQL exclusion filter, for example `not user.asset.criticality: "low_impact"`.
- You can preview risky entities first (1000 sampled entities in the chosen time frame; limited to two risk scores per Kibana instance or serverless project).
- You need alerts in the environment to see data.
- Elastic does not recommend risk scoring plus the entity store on deployments under 4 GB of memory; it recommends at least 8 GB.
- Versions 9.4.0-9.4.5 and 9.5.0-9.5.1 enable both automatically in the default space; from 9.4.6 and 9.5.2 enable them in every space.
- Upgrading from the original risk modules to 9.0 or later: use the Start update prompt to install the latest engine; previous data is retained.

## Asset criticality
- Levels: Low, Medium, High, Extreme impact. Entities have no default level.
- Assign individually (host or user details page, entity details flyout, Timeline flyout), by the Asset criticality API, or by importing a CSV, TXT or TSV file (max 1 MB) with three columns per row: entity type (`host`, `user` or `service`), the `host.name` / `user.name` / `service.name`, and a level: `extreme_impact`, `high_impact`, `medium_impact`, `low_impact` or `unassigned`. Import overwrites levels for entities in the file; invalid lines are flagged and not assigned.
- Individual changes recalculate that entity's score immediately; file imports wait for the next hourly run unless you click Recalculate entity risk scores now.
- After assignment, later alerts for the entity are enriched with its criticality level; use it to prioritise triage. The entity flyout's risk score section shows criticality's contribution.

## Verify
Generate several alerts for a test user, wait one cycle (or recalculate), and confirm the score, level and contributing alerts, including the criticality contribution, appear in the entity flyout.

## Checked
Confirmed against Elastic's Entity risk scoring, Turn on risk scoring and Asset criticality pages. Removed because the pages do not state them: Platinum licence requirement, `host.risk.calculated_level` field names, threshold-rule recipe on risk indices, the closed-alert exclusion wording, naming-split gotcha and jump-box advice.
Method: docs-only read of cited pages, 2026-11-08
