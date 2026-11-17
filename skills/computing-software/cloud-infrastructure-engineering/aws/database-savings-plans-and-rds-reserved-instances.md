---
id: computing-software.cloud-infrastructure-engineering.aws.database-savings-plans-and-rds-reserved-instances
name: database-savings-plans-and-rds-reserved-instances
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds, database-savings-plans, rds-reserved-instances, cost-optimization, commitments]
level: practitioner
status: docs-checked
description: "Commit database spend with RDS reserved DB instances (matching rules, size flexibility, offering types, Multi-AZ clusters) or Database Savings Plans, and know what they cover."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithReservedDBInstances.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithReservedDBInstances.WorkingWith.html", "https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html", "https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database Savings Plans and RDS reserved instances

## 1. Reserved DB instances
A reserved DB instance is a billing discount applied to matching on-demand DB instances, not a physical instance. It is
tied to instance type and Region, for a one- or three-year term, and cannot be cancelled (you can delete the DB
instance and launch another compatible one under the same reservation).
```bash
aws rds describe-reserved-db-instances-offerings --db-instance-class <DB_INSTANCE_CLASS> \
  --product-description postgresql --duration 31536000 --offering-type "No Upfront" --multi-az
aws rds purchase-reserved-db-instances-offering --reserved-db-instances-offering-id <OFFERING_ID> \
  --reserved-db-instance-id <YOUR_RESERVATION_ID> --db-instance-count 2
```
- To be billed at the discount, the DB instance must match the reservation's Region, DB engine (version need not match),
  DB instance type, and for Db2, SQL Server and Oracle License Included the instance size, plus edition and license type
  (license-included vs bring-your-own-license). Otherwise it is billed on demand.
- Offering types: No Upfront (one-year only, per the page), Partial Upfront, All Upfront. Not every instance class offers
  every type; confirm with `describe-reserved-db-instances-offerings` or the console.
- **Size flexibility** applies within the same Region, engine and instance class type for RDS for Db2, MariaDB, MySQL,
  Oracle (BYOL) and PostgreSQL; not for SQL Server or Oracle License Included. A `db.r6i.large` reservation can cover
  `db.r6i.xlarge`, but not `db.r6id.large` or `db.r7g.large`, which are different class types, so a family change
  (for example a Graviton move) means the reservation no longer applies to the new class.
  Compare usage in normalized units per hour (the page tabulates them: Single-AZ large = 4, xlarge = 8; Multi-AZ doubles them).
- Multi-AZ and Single-AZ both benefit: you can move between them within the same class type.
- A Multi-AZ DB **cluster** (one writer, two standbys) is covered by three Single-AZ reservations, or one Multi-AZ plus
  one Single-AZ; fewer leaves the cluster partially reserved. Size-flexible larger reservations can cover several smaller instances.
- The discount covers hourly instance usage only, not storage, backups or I/O.
- With consolidated billing every account in the organization is treated as one for the reservation benefit.
- Reservations are Region-specific and cannot be transferred between Regions. Aurora has its own page ("Reserved DB
  instances for Aurora"), which was not read; check it before buying for Aurora.

## 2. Database Savings Plans
Per the Savings Plans "types" page, Database Savings Plans apply automatically to the latest provisioned instance
generations regardless of engine, instance family, size, AZ or Region, and also to serverless usage, across Aurora, RDS,
DynamoDB, ElastiCache, DocumentDB, Timestream, Neptune, Keyspaces, DMS and Amazon OpenSearch Service. The commitment
terms cannot be changed after purchase; you can buy additional plans as usage changes. Terms are one year (365 days) or
three years (1,095 days), and payment can be All, Partial or No upfront. See the pricing and Savings Plans pages for
current discount levels rather than quoting them.

## 3. Sizing
Use the Savings Plans recommendations in AWS Cost Explorer (view, refresh, customise, purchase); the page says these
show the recommended commitment level. Plan for engine or instance-family changes before committing to a long term;
reserved DB instances are narrower than Database Savings Plans for that reason.

## Verify
- [ ] The reservation appears under Reserved instances in the RDS console (or `describe-reserved-db-instances`) in the intended Region.
- [ ] A matching DB instance is billed at the reserved rate.

## Checked
Date: 2026-11-07. Read in full: RDS "Reserved DB instances for Amazon RDS" (overview, offering types, size flexibility
and the normalized-units table, billing example, Multi-AZ clusters, deleting), "Purchasing reserved DB instances"
(console steps and the first CLI example), Savings Plans "What are Savings Plans?" and "Savings Plans types". CLI
flags were checked with check_commands. Not read: the Aurora reserved-instance page, the rest of the purchasing page
(output samples), and the pricing pages (no prices or discount percentages kept).
Removed because no page read states them: "1 or 3 years for every offering type", the Aurora Serverless v2 ACU claim,
the 30/60-day lookback and "commit to the floor" advice, Budgets utilization alarms at 90%, and the coverage and
utilization targets in Verify.
Method: documentation only; no commands were run.
