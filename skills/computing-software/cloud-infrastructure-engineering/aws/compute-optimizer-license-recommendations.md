---
id: computing-software.cloud-infrastructure-engineering.aws.compute-optimizer-license-recommendations
name: compute-optimizer-license-recommendations
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, compute-optimizer, license-recommendations, sql-server, license-optimization, byol, windows]
level: practitioner
status: draft
description: "Cut commercial licence cost with Compute Optimizer licence recommendations: SQL Server edition downgrades on EC2, the monitoring prerequisites, findings and safe validation."
sources: ["AWS Compute Optimizer User Guide - Commercial software license recommendations", "AWS Compute Optimizer API Reference - GetLicenseRecommendations", "Amazon CloudWatch Application Insights User Guide - Monitoring SQL Server"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compute Optimizer licence recommendations

**Goal:** stop paying Enterprise prices for databases that only use Standard features, and spot
over-licensed instances.

## What it covers
- Microsoft SQL Server on EC2 (licence-included and BYOL): recommends moving from **Enterprise** to
  **Standard** edition when Enterprise-only features are not in use and resources fit Standard's limits.
- Findings: `Optimized`, `NotOptimized` (savings available), `InsufficientMetrics` (monitoring missing).

## Prerequisites
- Compute Optimizer enrollment.
- **CloudWatch Application Insights** monitoring the SQL Server instance (it collects the SQL Server
  metrics and feature usage signals Compute Optimizer needs), with the CloudWatch agent and permissions; otherwise findings stay InsufficientMetrics.
- Enough history (a couple of weeks or more).

## Read
```bash
aws compute-optimizer get-license-recommendations \
  --query 'licenseRecommendations[].{arn:resourceArn,finding:finding,edition:currentLicenseConfiguration.licenseEdition,options:licenseRecommendationOptions[0]}'
```
Console: Compute Optimizer > Licenses. Options include target edition, estimated monthly savings and the reasons.

## Validate before downgrading
- Check feature usage yourself: `SELECT * FROM sys.dm_db_persisted_sku_features;` per database lists Enterprise features in use (partitioning, compression, TDE on older versions, etc.).
- Check limits for Standard (cores and memory caps for the version); bigger instances may need to shrink to fit.
- Availability Groups: Standard supports Basic AGs only (one database per AG, no readable secondaries).

## Change
- Licence-included EC2: edition comes from the AMI, so migrate to a Standard-edition AMI/instance (backup/restore or log shipping), not an in-place switch.
- BYOL: in-place edition downgrade via SQL Server setup is possible for some paths; check Microsoft guidance.
- Consider RDS for SQL Server Standard, or Babelfish/Aurora PostgreSQL for bigger savings.

## Gotchas
- Recommendations reflect the observed window; quarterly jobs using Enterprise features may be missed.
- Licence mobility and BYOL terms depend on your Microsoft agreements (Software Assurance, dedicated hosts).

## Verify
- [ ] Application Insights enabled on SQL Server fleet; no InsufficientMetrics findings left.
- [ ] Downgrade candidates validated with DMV feature checks and signed off by the DBA.
