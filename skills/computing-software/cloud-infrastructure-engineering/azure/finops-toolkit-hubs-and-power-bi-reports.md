---
id: computing-software.cloud-infrastructure-engineering.azure.finops-toolkit-hubs-and-power-bi-reports
name: finops-toolkit-hubs-and-power-bi-reports
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, cost-management, finops-toolkit, finops-hubs, focus, power-bi, optimization-workbook]
level: practitioner
status: docs-checked
description: "Stand up Microsoft's FinOps toolkit: deploy a FinOps hub, feed it Cost Management exports, and use the Power BI reports and workbooks."
sources: ["https://learn.microsoft.com/cloud-computing/finops/toolkit/finops-toolkit-overview", "https://learn.microsoft.com/cloud-computing/finops/toolkit/hubs/finops-hubs-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FinOps toolkit: hubs and reports

**Goal:** a scalable cost data platform with ready-made reports, instead of building pipelines from scratch.

## What is in the toolkit (open source, Microsoft)
- **FinOps hubs**: open, extensible, scalable cost reporting built on Cost Management exports, aligned to FOCUS.
- **Power BI reports**: starter kits, intended to be customised.
- **FinOps workbooks**: a cost optimisation workbook and a governance workbook.
- Also: Azure Optimization Engine, a PowerShell module, Bicep Registry modules and open data (pricing units, regions, resource types, services, sample exports).
- Monthly releases, tracked as GitHub milestones.

## What a hub contains
- Optional Azure Data Explorer (Kusto) or Microsoft Fabric Real-Time Intelligence as the analytics store.
- A Data Lake Storage Gen2 account as the ingestion staging area.
- A Data Factory instance for ingestion and cleanup.
- A Key Vault holding the Data Factory managed identity credentials.
- Estimated cost starts at $120 a month plus $10 a month per $1M of cost monitored (Data Explorer single node $120, or F2 Fabric capacity $300). Without Data Explorer or Fabric it is about $5 per $1M. Data volume is roughly 20 GB per $1M.

## Create a hub
1. Enable the CostManagementExports and EventGrid resource providers on the subscription.
2. Plan public or private network routing.
3. Optional: set up Fabric Real-Time Intelligence.
4. Deploy the FinOps hub template (Azure, Azure Gov, or 21Vianet for MCA only).
5. Create exports in Cost Management, or grant the hub access to the scopes.
6. Set up the Data Explorer dashboard or the Power BI reports.

## Working with the data
- Five Power BI reports ship in three sets: demo (sample data), KQL (connect to Data Explorer) and storage (connect to the storage account).
- Do not modify the built-in pipelines or the data in the `msexports` container. Custom Data Factory pipelines should watch the `ingestion` container and use a consistent name prefix.
- Prefer a new Bicep module that references `finops-hub/main.bicep` or `hub.bicep` over editing the template, so upgrades apply cleanly.
- Hubs 0.2 and later need FOCUS cost data from Cost Management exports, which pay-as-you-go (MOSA) subscriptions do not support; only hubs 0.1.1 support them.

## Permissions
- Configuring exports: Cost Management Contributor for subscriptions and resource groups; billing-scope roles for EA, MCA and MPA.
- Deploying the template: Contributor plus Role Based Access Control Administrator, or Owner.
- Power BI: Storage Blob Data Reader (or SAS token) for storage reports; Viewer on the Hub and Ingestion databases for KQL reports.
- CSP customers configure exports per subscription; management group exports are not supported for MCA or CSP subscriptions.

## Verify
- [ ] The ingestion container holds the expected history and report totals match Cost Management.

## Checked
Method: docs-checked 2026-11-09 against the FinOps toolkit overview and FinOps hubs overview pages (downloaded with curl as Learn markdown, read in full). Dropped the PowerShell deploy and export commands, backfill advice, the private-endpoint note and the GitHub repo source, which these pages do not confirm.
