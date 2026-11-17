---
id: computing-software.cybersecurity-defensive.splunk.sentinel-workspace-design-and-lighthouse
name: sentinel-workspace-design-and-lighthouse
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [microsoft-sentinel, sentinel-workspace-design, log-analytics-workspace, azure-lighthouse, multi-tenant, rbac, data-residency]
level: advanced
status: draft
description: "Design Microsoft Sentinel workspaces: single vs multiple workspaces, data residency, table-level RBAC, and multi-tenant management with Azure Lighthouse."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/design-your-workspace-architecture", "https://learn.microsoft.com/en-us/azure/sentinel/multiple-tenants-service-providers", "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/manage-access"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sentinel workspace design and Lighthouse

## Default: one workspace
Single Log Analytics workspace per tenant gives cross-source correlation without cross-workspace
queries and simplest cost/commitment tiers. Split only for a concrete reason:
- **Data residency/sovereignty**: data must stay in a region -> workspace per region.
- **Separate tenants** (subsidiaries, MSSP clients) -> workspace per tenant, managed via Lighthouse.
- **Billing separation** where chargeback cannot use table/resource tags.
- **Operational data** (perf, app logs) heavy and non-security -> separate workspace so Sentinel
  pricing does not apply.

## Access control inside one workspace
- Resource-context RBAC: users see logs of resources they have access to.
- Table-level RBAC via custom roles with `Microsoft.OperationalInsights/workspaces/query/<Table>/read`
  (or granular RBAC in newer Log Analytics) to hide e.g. HR app logs.
- Sentinel roles: Reader, Responder, Contributor, Automation Contributor, Playbook Operator.

## Multi-workspace / multi-tenant
- Cross-workspace KQL: `union workspace("ws-eu").SecurityEvent, workspace("ws-us").SecurityEvent`
  (max 100 workspaces per query; slow). Analytics rules can query across workspaces too.
- **Azure Lighthouse**: client tenants delegate resource groups/subscriptions to the provider
  tenant's groups with defined roles (onboarding via ARM template or Marketplace offer). The SOC
  sees all client workspaces in its own portal; access is revocable by the client.
- Content consistency: deploy rules/playbooks from a repository (Sentinel Repositories per
  workspace or CI pipeline) so every tenant runs the same versioned content.
- Unified SecOps portal supports multi-workspace views; check current limits per tenant.

## Gotchas
- Logic App playbooks run in the client tenant; their managed identity needs permissions there.
- Commitment tiers apply per workspace (or cluster); small workspaces lose discounts; consider a
  dedicated cluster when combined ingestion is large.
- Lighthouse cannot delegate Entra ID roles; Entra admin tasks still need guest accounts or GDAP.

## Verify
Analyst in provider tenant can see a client incident and run a playbook; a client user cannot see
other clients; cross-workspace query returns data from each intended workspace.
