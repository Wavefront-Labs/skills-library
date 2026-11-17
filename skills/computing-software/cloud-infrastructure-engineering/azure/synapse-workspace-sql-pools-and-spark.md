---
id: computing-software.cloud-infrastructure-engineering.azure.synapse-workspace-sql-pools-and-spark
name: synapse-workspace-sql-pools-and-spark
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, synapse, synapse-workspace, dedicated-sql-pool, serverless-sql, spark-pools, adls-gen2, managed-vnet, data-exfiltration-protection, openrowset, distribution, workload-management, pause-resume]
level: practitioner
status: docs-checked
description: "Stand up Azure Synapse: workspace on ADLS Gen2 with managed VNet, serverless SQL over the lake, dedicated SQL pool distribution and pause/resume, Spark pools and access control."
sources: ["https://learn.microsoft.com/en-us/azure/synapse-analytics/quickstart-create-workspace-cli", "https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/on-demand-workspace-overview", "https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-tables-distribute", "https://learn.microsoft.com/en-us/azure/synapse-analytics/security/synapse-workspace-managed-vnet"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Synapse workspace — SQL pools and Spark

**Goal:** an analytics workspace over a data lake with the right engine per job: serverless SQL
for ad-hoc lake queries, dedicated SQL pool for a governed warehouse, Spark for engineering.

## 1. Workspace
```bash
az storage account create -g rg-ana -n stlakeprod --sku <sku> --kind StorageV2 --hns true
az synapse workspace create -g rg-ana -n syn-prod -l uksouth --storage-account stlakeprod --file-system synapse \
  --sql-admin-login-user sqladminuser --sql-admin-login-password "$SQL_ADMIN_PASSWORD" \
  --enable-managed-virtual-network true --prevent-data-exfiltration true
az role assignment create --assignee <workspace-msi-objectid> --role "Storage Blob Data Contributor" --scope <stlakeprod-id>
```
- **Managed VNet** must be chosen at creation (the workspace can't be reconfigured to add or remove it later; choose data exfiltration protection at creation too);
  outbound then only via **managed private endpoints** you approve.
- Access: Azure RBAC for the resource, **Synapse RBAC** roles (see the Synapse RBAC article for the current list), plus storage data-plane RBAC/ACLs for the lake.

## 2. Serverless SQL (built-in, billed on data processed by queries)
```sql
SELECT TOP 100 * FROM OPENROWSET(BULK 'https://stlakeprod.dfs.core.windows.net/raw/sales/year=2026/*.parquet', FORMAT='PARQUET') AS r;
CREATE EXTERNAL DATA SOURCE lake WITH (LOCATION='https://stlakeprod.dfs.core.windows.net/curated', CREDENTIAL=<credential-name>);
CREATE VIEW dbo.sales AS SELECT * FROM OPENROWSET(BULK 'sales/**', DATA_SOURCE='lake', FORMAT='DELTA') AS s;
```
Parquet/Delta with partition folders + `filepath()` pruning keeps scans (and bills) small.

## 3. Dedicated SQL pool (provisioned MPP warehouse)
```bash
az synapse sql pool create -g rg-ana --workspace-name syn-prod -n dw --performance-level <DWxxxc-level>
az synapse sql pool pause  -g rg-ana --workspace-name syn-prod -n dw    # stop compute billing; storage still billed
az synapse sql pool resume -g rg-ana --workspace-name syn-prod -n dw
```
- Distribution: large facts `HASH(high-cardinality join key)`, small dims `REPLICATE`, staging tables `ROUND_ROBIN` (round-robin helps loading speed but joins on it usually need data movement).
- Load with `COPY INTO` from the lake rather than row-by-row inserts.
- Check skew: `DBCC PDW_SHOWSPACEUSED('dbo.FactSales')` — rows per distribution (60 distributions) can vary up to 10% without noticeable impact; more than that suggests a poor distribution key.

## 4. Spark pools
`az synapse spark pool create --workspace-name syn-prod -g rg-ana -n sparkeng --spark-version <supported-version> --node-size Medium --enable-auto-scale true --min-node-count 3 --max-node-count 10 --enable-auto-pause true --delay 15`
Libraries via workspace packages / `requirements.txt`; notebooks in Git (Synapse Git integration with Azure DevOps/GitHub) and deployed via the workspace deployment task.

## Gotchas
- Serverless SQL is billed on data processed by queries, with no charge for reserved resources; CETAS (`CREATE EXTERNAL TABLE AS SELECT`) is available there, but it is not a dedicated warehouse.
- A workspace created with a managed VNet cannot be reconfigured to add or remove it; with data exfiltration protection, outbound traffic goes only to approved managed private endpoints.

## Verify
- [ ] Workspace has managed VNet/DEP as required; managed private endpoints approved on the lake.
- [ ] Serverless view over Delta returns rows.
- [ ] Dedicated pool tables show balanced distribution and pause/resume schedule is automated.

## Checked
Date: 2026-10-31. Checked against Microsoft Learn: managed workspace VNet, serverless SQL pool overview, dedicated SQL pool table distribution, and the Synapse CLI quickstart; `az synapse` commands and flags checked against the CLI reference.
- Confirmed: managed VNet and exfiltration protection fixed at creation, managed private endpoints, serverless billing on data processed, Parquet/Delta, `filepath()`, CETAS, 60 distributions, hash/round-robin/replicated guidance, `DBCC PDW_SHOWSPACEUSED`, 10 % skew guidance, CLI flags.
- Removed as unconfirmed: Fabric advice, SQL local-auth advice, `WorkspaceIdentity` credential, SKU and performance-level literals, COPY INTO speed claim, workload-management and statistics advice, restore-point and Spark-retirement notes, 403 gotcha.
Method: documentation only; no commands were run.
