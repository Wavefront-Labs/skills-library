---
id: computing-software.cloud-infrastructure-engineering.azure.defender-governance-rules-and-remediation-owners
name: defender-governance-rules-and-remediation-owners
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, defender-for-cloud, governance-rules, remediation-owners, due-dates, grace-period, security-recommendations]
level: practitioner
status: docs-checked
description: "Assign owners and due dates to Defender for Cloud recommendations with governance rules (by tag/scope/severity), weekly owner emails, grace periods and progress reporting."
sources: ["https://learn.microsoft.com/azure/defender-for-cloud/governance-rules", "https://learn.microsoft.com/azure/defender-for-cloud/review-security-recommendations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Governance rules and remediation owners

**Goal:** every unhealthy recommendation has a named owner and a due date, owners are reminded
automatically, and security can report overdue items per team.

## Create a rule
Defender for Cloud → Environment settings → (MG/subscription/connector) → **Governance rules** → Create:
- **Priority** 1 (highest) to 1000; the highest-priority matching rule assigns the owner and due date.
- **Scope**: MG, subscriptions, connectors (AWS/GCP); exclusions.
- **Conditions**: by recommendation severity (e.g. High), by specific recommendations, or by risk level (CSPM).
- **Owner**: *By resource tag* (e.g. tag `Owner` → email) or a fixed email.
- **Remediation timeframe**: 7/14/30/90 days; **grace period** (for recommendations from the Microsoft cloud security benchmark, resources do not affect Secure Score until overdue) on/off.
- **Notifications**: weekly email to owners of open/overdue items; weekly digest to owners' managers.

## Pattern
| Rule | Condition | Owner | Due |
|---|---|---|---|
| 1 | Risk level Critical (attack paths) | tag `Owner` | 7 days, no grace |
| 2 | Severity High | tag `Owner` | 30 days |
| 3 | Severity Medium | tag `Owner` | 90 days |
| 4 | Fallback (no Owner tag) | cloud-security@contoso.com | 30 days |
Requires an enforced `Owner` tag (Policy inherit from RG) — otherwise rule 4 catches everything.

## Apply to existing recommendations
For existing recommendations that match a new rule, the wizard lets you overwrite their owner and due date or leave them.

## Progress reporting
Use the recommendations page filters for owner and due date to list overdue items.

## Gotchas
- Grace period hides score impact; don't use it for Critical.
- Owner emails come from the tag value, so validate tag values (for example with Azure Policy).

## Verify
- [ ] Rules list shows priorities and scopes covering all production MGs.
- [ ] Overdue High items per owner are reviewed weekly.

## Checked

2026-10-28. Confirmed on the Defender for Cloud governance rules page: 7, 14, 30 or 90 day time frames, priority order (1 to 1000, highest first), grace period applies to Microsoft cloud security benchmark recommendations, weekly emails to owners and their managers by default, overwrite option for existing recommendations. Removed: the Resource Graph query and governance workbook (property names and workbook not found), the owner-can-change-due-date claim and a percentage target.

Method: documentation only; no commands were run.
