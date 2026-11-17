---
id: computing-software.cybersecurity-defensive.nessus.tenable-explore-views
name: tenable-explore-views
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [tenable-explore, tenable-vulnerability-management, findings, asset-tags, saved-filters, scan-results, nessus]
level: practitioner
status: draft
description: "Use Tenable Vulnerability Management Explore views: findings and assets workbenches, filters, saved views, grouping, tags and exports for triage and reporting."
sources: ["https://docs.tenable.com/vulnerability-management/Content/Explore/Explore.htm", "https://docs.tenable.com/vulnerability-management/Content/Explore/Findings/Findings.htm", "https://docs.tenable.com/vulnerability-management/Content/Explore/Assets/Assets.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Tenable VM Explore views

Explore (Tenable Vulnerability Management) replaced the legacy Workbenches for findings and assets.

## Findings
- Tabs: Vulnerabilities, Cloud Misconfigurations, Host Audits, Web Application Findings.
- Views: list or grouped (by plugin, asset, solution). Group by plugin to see blast radius; by
  asset for an owner's to-do list.
- Key filters: Severity, VPR, CVSSv3 base, `Exploit Available`, `CISA KEV`, State (Active, New,
  Resurfaced, Fixed), First Seen / Last Seen, Asset Tags, Source (Nessus scan, Agent, NNM),
  Plugin family, Accepted/Recast.
- Saved filters / saved views for each audience: "Criticals past SLA - Linux Ops".

## Assets
- Filters: Last Seen, Sources, Operating System, ACR (asset criticality), AES (exposure score),
  Licensed, Has Plugin Results, Authentication status ("Auth failure" assets need credential fixes).
- Asset details: findings, open ports, installed software, tags, merge history.

## Tags
Tag categories (`Owner`, `Environment`, `Location`) with dynamic rules (e.g. IP range, OS, cloud
tags). Use tags in filters, access groups (who can see what), and export scoping.

## Exports
Download CSV from a view, or schedule exports; for large datasets use the API export
(`/vulns/export`, `/assets/export`) or pytenable; UI CSV exports have row limits.

## Gotchas
- Default time filters (e.g. Last Seen within 30 days) hide stale assets; widen when auditing.
- Accepted/recast findings are hidden by default; include when reconciling counts.
- Explore query syntax and filter names change across releases; re-validate saved views after updates.

## Verify
A saved view's count matches the API export with the same filters; a scoped user sees only
assets within their access group.
