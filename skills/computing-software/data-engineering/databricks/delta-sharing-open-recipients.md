---
id: computing-software.data-engineering.databricks.delta-sharing-open-recipients
name: delta-sharing-open-recipients
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, delta-sharing, open-sharing, recipients, bearer-token, credential-file, share-partitions, delta-sharing-connector, external-data-sharing]
level: practitioner
status: docs-checked
description: "Share Delta tables with non-Databricks recipients via open sharing: shares, recipients, activation links, partition filters, history sharing and client access."
sources:
  - https://docs.databricks.com/aws/en/delta-sharing/create-recipient
  - https://docs.databricks.com/aws/en/delta-sharing/create-share
  - https://docs.databricks.com/aws/en/delta-sharing/read-data-open
  - https://github.com/delta-io/delta-sharing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delta Sharing: open sharing recipients

**Goal:** give an external partner live read access to specific tables without copying data, using any client (pandas, Spark, Power BI, Tableau), and keep control of credentials.

## 1. Databricks-to-Databricks vs open
- Recipient on Databricks Unity Catalog → use Databricks-to-Databricks sharing (recipient's sharing identifier, no tokens to manage).
- Anyone else → **open sharing**: token-based authentication (a bearer token in a credential file, or OAuth federation).

## 2. Create the share
```sql
CREATE SHARE partner_x_share COMMENT 'Orders for Partner X';
ALTER SHARE partner_x_share ADD TABLE prod.sales.orders
  PARTITION (region = 'EU')                 -- share only some partitions
  AS sales.orders_eu;                       -- alias the name the recipient sees
ALTER SHARE partner_x_share ADD TABLE prod.sales.products WITH HISTORY;   -- allow time travel / CDF reads
```
Share views or filtered tables if columns must be hidden — sharing exposes every column of a shared table.

## 3. Create the open recipient
Create the recipient and add it to the share as described on the create-recipient page (open sharing is a recipient without a Databricks sharing identifier).
- OpenSharing emails the recipient a secure activation link when you add them to a share; the recipient downloads the credential file from it. Share the credential file only over a secure channel.
- Look up token lifetime, rotation and IP access list options on the create-recipient page before relying on them.

## 4. Rotate and revoke
Revoke access by removing the recipient from the share or dropping the recipient (see the Databricks Delta Sharing documentation for the exact statements).

## 5. Recipient side
```python
import delta_sharing
profile = "config.share"                                      # the credential file
delta_sharing.load_as_pandas(f"{profile}#partner_x_share.sales.orders_eu")
spark.read.format("deltaSharing").load(f"{profile}#partner_x_share.sales.orders_eu")
```

## 6. Monitor
Use the Unity Catalog audit logs to review recipient activity.

## Verify
- [ ] Recipient sees only the aliased tables and permitted partitions.
- [ ] Token expiry is set and rotation tested.
- [ ] Recipient access appears in the audit log.

## Checked

- 2026-10-28: confirmed on the create-share page (`ALTER SHARE ... ADD TABLE` with `PARTITION`, `AS` alias, `WITH HISTORY`/`WITHOUT HISTORY`, CDF must be enabled to share history), the create-recipient page (open sharing uses bearer tokens or OAuth federation, activation link emailed) and the read-data page (`deltaSharing` Spark format).
- Removed: `SHOW ALL IN SHARE`, recipient property and `CURRENT_RECIPIENT` filtering, one-time download claim, metastore token lifetime, IP list, `ROTATE TOKEN`, Power BI/Tableau connector claim and audit table filter names (not found in the fetched pages).

Method: documentation only; no commands were run.
