---
id: computing-software.data-engineering.data-warehouse-architecture.serverless-vs-provisioned-warehouse-compute
name: serverless-vs-provisioned-warehouse-compute
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, serverless-vs-provisioned, serverless-compute, provisioned-capacity, bigquery-editions, redshift-serverless, workload-isolation]
level: practitioner
status: docs-checked
description: "Choose serverless or provisioned compute for warehouses and lakehouses: billing models, workload fit, cold starts, cost crossover analysis and guardrails."
sources:
  - https://cloud.google.com/bigquery/pricing
  - https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-billing.html
  - https://docs.databricks.com/en/compute/sql-warehouse/warehouse-types.html
  - https://docs.snowflake.com/en/user-guide/cost-understanding-compute
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Serverless vs provisioned compute

## The models
| Platform | Pay-as-you-go / serverless | Reserved / committed |
|---|---|---|
| BigQuery | on-demand (default): pay per TiB processed, first 1 TiB per month free; up to roughly 2,000 concurrent slots shared per project | capacity pricing per slot-hour with BigQuery editions: autoscaler (billed per second, one-minute minimum by default, opt-in fluid scaling for no minimum) and optional 1- or 3-year slot commitments (50-slot minimum, increments of 50) |
| Redshift Serverless | on-demand: RPU usage, minimum charge 60 seconds metered per second | reservations: discount for a preset amount of compute for a period; reservations and on-demand can be combined |
| Databricks SQL | serverless warehouses (Databricks-managed compute) | pro and classic warehouses, with compute in your AWS account |
| Snowflake | virtual warehouses bill credits per second with a 60-second minimum while running; suspended warehouses use none; serverless features bill compute-hours on Snowflake-managed compute | capacity pricing is on Snowflake's pricing pages; not checked here |

Always check the current prices; this skill states structure, not rates.

## Fit by workload
| Workload | Lean towards |
|---|---|
| Spiky, unpredictable, many idle hours | pay-as-you-go/serverless (Redshift states on-demand suits unknown usage patterns) |
| Steady, forecastable usage | reservations/commitments (Redshift states reservations suit steady, forecastable capacity) |
| Interactive BI needing fast first query | Databricks serverless (typical start 2 to 6 seconds, versus about 4 minutes for pro and classic) |
| Large scans by inexperienced users | consider capacity pricing: BigQuery on-demand bills bytes processed, with a 10 MB minimum per table referenced |

## Cost crossover
1. Pull 30-90 days of usage (bytes processed, slot time, RPU hours, warehouse credits by hour).
2. Price it both ways: on-demand rate x volume against required capacity x hours x committed rate, at your peak concurrency.
3. Find the utilisation at which commitment breaks even for your prices; there is no universal threshold.
4. Mixed: reservation for the steady base plus autoscaling or on-demand for peaks (BigQuery editions and Redshift both allow mixing).

## Operational considerations
- Start-up: Databricks serverless typically starts in 2 to 6 seconds and scales up and down quickly; pro and classic take several minutes to start. In Snowflake, warehouse auto-suspend trades idle cost against resume latency.
- Redshift Serverless billing traps: open transactions keep using RPUs; cancelled queries are still billed; RPU capacity can stay high after load falls; connection-pool health checks count as billable activity. Set maximum RPU hours in the console and use SESSION TIMEOUT (defaults of 1 hour idle session, 6 hours idle open transaction).
- Snowflake: cloud services usage is billed only above 10% of daily warehouse credits.
- Isolation: separate compute per workload (ELT, BI, data science) so one cannot starve another.

## Verify
- [ ] Decision backed by a usage-based cost model for both options, revisited when usage changes.
- [ ] Spend guardrails configured for every pay-per-use workload (for example Redshift maximum RPU hours).

## Checked
Date: 2026-11-09. Confirmed from the four cited pages: BigQuery pricing models, free tier, slot commitments and billing minimums; Redshift Serverless billing; Databricks warehouse types and start times; Snowflake credit billing. Removed as unconfirmed: the Synapse/Fabric row, Redshift provisioned RA3 and reserved nodes, the 40-60% utilisation rule, BigQuery custom quotas and maximum_bytes_billed, Snowflake resource monitors, quarterly review. The BigQuery pricing page is long and was searched by keyword rather than read in full.
Method: documentation only; no commands were run.
