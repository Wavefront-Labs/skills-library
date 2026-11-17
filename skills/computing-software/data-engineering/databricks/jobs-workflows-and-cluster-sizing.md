---
id: computing-software.data-engineering.databricks.jobs-workflows-and-cluster-sizing
name: jobs-workflows-and-cluster-sizing
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-jobs, databricks-workflows, job-clusters, all-purpose-cluster, photon, cluster-policies, autoscaling, spot-instances, serverless-compute, dbt-task, delta-live-tables, task-dependencies]
status: docs-checked
level: practitioner
description: "Orchestrate Databricks Jobs/Workflows (multi-task, job clusters vs all-purpose) and size clusters/Photon correctly for cost and reliability."
sources:
  - https://docs.databricks.com/en/jobs/index.html
  - https://docs.databricks.com/en/compute/photon.html
  - https://docs.databricks.com/aws/en/jobs/compute
  - https://docs.databricks.com/aws/en/jobs/task-values
  - https://docs.databricks.com/aws/en/compute/configure
  - https://docs.databricks.com/aws/en/compute/cluster-config-best-practices
  - https://docs.databricks.com/aws/en/admin/clusters/policies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Databricks Jobs/Workflows orchestration and cluster cost control

**Goal:** run multi-step pipelines reliably on Databricks without the most common expensive mistake, running unattended production jobs on all-purpose compute. Databricks now calls Workflows "Lakeflow Jobs".

## 1. Choosing compute for a job
Per the "Configure compute for jobs" page, each task gets its own compute, and several tasks in one job can share one compute resource. Serverless compute for jobs is the default for every task that supports it, and is the recommended compute for notebook, Python script and Python wheel tasks. Classic jobs compute is recommended for JAR and Spark Submit tasks; SQL and dbt tasks run on a SQL warehouse. Classic all-purpose compute is an optional, supported choice, but "Databricks does not recommend this configuration for production jobs". Pricing is tied to the compute used: check the Databricks pricing page for rates instead of assuming a ratio.
- Serverless limits to know: continuous scheduling supports only bounded Structured Streaming triggers such as Trigger.AvailableNow, and default or time-based interval triggers are not supported.
- **Sharing compute across tasks** can cut start-up latency. A shared job cluster is scoped to one job run (not shared with other jobs or runs), starts when the first task using it begins, ends after the last, and stays idle while tasks not using it run. Libraries cannot be declared in a shared job cluster configuration. Tasks sharing compute run on the same driver JVM, so Scala singletons and companion-object state persist across tasks; if parallel tasks need isolation, use separate compute, add dependencies so they run sequentially, or pass parameters explicitly.
- Instance pools reserve cloud compute to decrease cluster start time (cluster best-practices page).

## 2. Multi-task jobs
A job is made of one or more tasks whose dependencies form a DAG (shown in the Graph view); tasks support branching (if/else) and looping (for each). Task types include notebook, pipeline and Python script, among others. Each task can use its own compute, so a light task can run small while a heavy Spark task runs large.
- Pass small values between tasks with task values: `dbutils.jobs.taskValues.set()` in a Python notebook, key-value pairs where the JSON representation of a value cannot exceed 48 KiB. Databricks recommends referencing them with the dynamic value reference `{{tasks.<task_name>.values.<value_name>}}` in task parameters rather than `taskValues.get()`. Pass larger data through storage and hand over the path.
- Documented limits (Lakeflow Jobs page): 2000 concurrent task runs per workspace (429 returned when a run cannot start), 10000 jobs created per hour, 12000 saved jobs, 1000 tasks per job.
- When a pipeline spans Databricks and non-Databricks systems, decide explicitly whether Lakeflow Jobs or an external orchestrator owns scheduling. Databricks documents orchestrating jobs with Apache Airflow; whichever you choose, avoid scheduling logic scattered redundantly across both.

## 3. Photon
Photon is the Databricks-native vectorized (C++) query engine for SQL, DataFrame, ETL and stateless streaming workloads, with no code changes needed. It is on by default for classic all-purpose compute, jobs compute and classic pipelines (the Use Photon Acceleration checkbox), but if you create them through the Clusters API or Jobs API you must set `runtime_engine` to `PHOTON`. Photon instances consume DBUs at a different rate than the same instance type without Photon.
- Benefit is greatest for long-running queries over large data; queries that normally finish in under two seconds see no meaningful gain.
- Not supported: UDFs, RDD APIs, Dataset APIs, and stateful streaming. Unsupported operations fall back to the Spark runtime transparently.
- Check it engaged: in the Spark UI SQL/DataFrame tab Photon operators appear orange; in the query profile, Execution Details shows the percentage of task time in Photon.

## 4. Autoscaling, spot instances, and compute policies
- **Autoscaling** takes a minimum and maximum number of workers; without it you give a fixed worker count. It can reduce cost versus static sizing, is not available for spark-submit jobs, and has limitations scaling down Structured Streaming clusters (Databricks points streaming workloads to pipelines with enhanced autoscaling). Do not enable Spark Dynamic Allocation (`spark.dynamicAllocation.enabled`) alongside Databricks autoscaling.
- **Spot instances**: Databricks recommends them for workloads with lax latency requirements. Do not use a pool with spot instances as the driver type; pick an on-demand driver so it is not reclaimed.
- **Compute policies** are rules workspace admins define to limit users' compute creation: prescribed settings, a cap on the number of clusters, per-cluster maximum cost via limits on price-driving attributes, and custom tag rules.

## Verify
- [ ] Every scheduled production job runs on serverless or classic jobs compute, not all-purpose compute.
- [ ] Photon's effect was checked in the Spark UI or query profile for a representative job before enabling it everywhere.
- [ ] Autoscaling min/max bounds are set deliberately per job.
- [ ] A compute policy limits instance types and sizes available to non-admin job authors.

## Checked
Date: 2026-11-09. Confirmed against the Databricks pages in sources: Lakeflow Jobs overview (concepts and limits), Configure compute for jobs, task values page (48 KiB, dynamic value reference), Photon page (defaults, runtime_engine, limitations, monitoring), Compute configuration reference (autoscaling, pools and spot driver), cluster best-practices, and the compute policies page. Removed: the claim that job clusters cost a lower DBU rate than all-purpose clusters and "multiples" cost figures, the claim that pools keep job-cluster pricing, the claim that Photon always costs a higher rate, the claim that fixed sizing is sometimes faster or cheaper than autoscale, the XCom comparison. Not read: the cluster policy definition reference and the serverless limitations page.
Method: documentation only; no commands were run.
