---
id: computing-software.data-engineering.databricks.driver-logs-and-spark-ui-on-databricks
name: driver-logs-and-spark-ui-on-databricks
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-driver-logs, spark-ui, cluster-log-delivery, debugging]
level: practitioner
status: docs-checked
description: "Debug Databricks jobs with driver logs (stdout, stderr, log4j), the Spark UI, executor logs and compute log delivery, and how to keep logs after the compute stops."
sources:
  - https://docs.databricks.com/aws/en/compute/troubleshooting/debugging-spark-ui
  - https://docs.databricks.com/aws/en/compute/configure#compute-log-delivery
  - https://docs.databricks.com/aws/en/compute/clusters-manage#driver-logs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Driver logs and Spark UI on Databricks

**Goal:** find the real error and the slow stage quickly.

## Where to look
- **Job run output**: notebook cell error / task error message (first stop).
- **Driver logs** (Driver logs tab on the compute details page): stderr, stdout and log4j output are saved in the driver log, and direct print and log statements from notebooks, jobs and libraries go there. Click a log file name to download it.
- **Spark UI**: the Databricks page on debugging with the Spark UI walks through jobs, stages and tasks.
- **Executor logs**: from the task details page find the executor that ran the task, open the compute UI, click the node count, then the master; the master page lists the workers, and the worker page gives the log4j output.

## Keep logs after the cluster dies
When you create all-purpose or jobs compute you can specify a location for cluster logs, including logs from the Spark driver, worker nodes and events. Logs are delivered every five minutes and archived hourly in the chosen destination, and delivery continues until the compute is terminated. Job compute is terminated after the run, so set a delivery location if you need the logs later.

## Verify
Logs exist in the delivery location for a finished job compute; the failing stage and exception are identifiable from them.

## Checked
2026-11-01. Confirmed against the Databricks pages Manage compute (driver logs), Compute configuration (compute log delivery) and Debugging with the Spark UI (executor logs via the compute UI). Removed: the cluster_log_conf volumes example and folder layout, log level code, the serverless section and the common-signals table.
Method: documentation only; no commands were run.
