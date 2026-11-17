---
id: computing-software.data-science-and-analytics.bi-tools.pbi-refresh-gateway
name: pbi-refresh-gateway
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [scheduled-refresh, on-premises-gateway, incremental-refresh]
level: practitioner
status: docs-checked
description: "Configure scheduled and incremental refresh, gateway data sources and credentials, and diagnose refresh failures."
sources:
  - https://learn.microsoft.com/power-bi/connect-data/refresh-data
  - https://learn.microsoft.com/power-bi/connect-data/incremental-refresh-configure
  - https://learn.microsoft.com/data-integration/gateway/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refresh
- Semantic model settings: gateway connection, data source credentials, refresh schedule (time slots) and failure notifications. Refresh now runs an on-demand refresh that does not affect the next scheduled time.
- A source Power BI cannot reach over a direct network connection needs a gateway connection configured before a schedule or on-demand refresh works. Use an enterprise gateway with a matching data source definition (only gateway admins can add data sources, and your account must be on the data source's user list), or a personal gateway if you manage models alone. A semantic model can use only one gateway connection.
- Cloud sources reachable directly (such as Azure SQL DB) need no gateway; manage them under Data source credentials. Each user has one set of credentials per data source across the models they own; use Take over to change credentials on a model you do not own.
- Incremental refresh: create case-sensitive Date/Time parameters named RangeStart and RangeEnd, filter the date column with them (an equal-to on only one of the two, to avoid duplicate rows), then define the policy (Incrementally refresh this table). The policy applies after publishing and a refresh. Folding matters: a slow load usually means the query is not folding.
## Gotchas
- Refresh limits: up to 8 scheduled time slots per day on shared capacity, up to 48 on Premium, PPU or Fabric capacity. Refresh must finish within 2 hours on shared capacity; Premium maximum is 5 hours (XMLA refresh can bypass it).
- Failure emails go to recipients in your Microsoft Entra tenant only (no external users); on-demand and programmatic refreshes do not send them. Check refresh history and the warning icon on the workspace list; an expired credential fixed by a gateway admin shows in history.
- Use separate gateways for Import models and DirectQuery/live connection models, so scheduled imports do not slow interactive reports.
## Verify
- [ ] Refresh history shows success and the report timestamp advanced.

## Checked
Confirmed on the refresh page: gateway requirement and one-connection rule, personal versus enterprise gateway, credentials per user and Take over, time slots (8 shared, 48 Premium), 2-hour and 5-hour limits, notification limits, refresh history, gateway separation advice. Confirmed on the incremental refresh configure page: RangeStart and RangeEnd names, case sensitivity, Date/Time type, equal-to rule, policy applied after publish. Removed: "use a service/managed account, not a person's credentials", "store N years, refresh last N days" wording, and the gateway landing page claims (only the landing page was cited, so nothing was taken from it).
Method: docs-checked 2026-11-09 against the Microsoft Learn Power BI refresh page (grep and selected sections read) and the incremental refresh configure page (read in full).
