---
id: computing-software.data-engineering.databricks.compute-access-modes
name: compute-access-modes
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, access-mode, standard-access-mode, dedicated-access-mode, data-security-mode, lakeguard, unity-catalog, cluster-policies, shared-clusters]
level: practitioner
status: docs-checked
description: "Choose Databricks compute access modes: standard vs dedicated, what each allows and blocks, enforcing modes with policies, migrating legacy modes."
sources:
  - https://docs.databricks.com/aws/en/compute/access-mode-limitations
  - https://docs.databricks.com/aws/en/compute/configure#access-mode
  - https://docs.databricks.com/aws/en/compute/dedicated-overview
  - https://docs.databricks.com/aws/en/admin/clusters/policy-definition
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute access modes

**Goal:** pick the access mode that lets your code run while Unity Catalog stays enforced.

## 1. The modes
| UI name (API `data_security_mode`) | Users | Notes |
|---|---|---|
| **Standard** (`DATA_SECURITY_MODE_STANDARD`; legacy alias `USER_ISOLATION`) | many users, fully isolated from each other | Python, SQL, Scala; some languages, APIs and features limited |
| **Dedicated** (`DATA_SECURITY_MODE_DEDICATED`; legacy alias `SINGLE_USER`) | one user or one group | Python, SQL, Scala, R; RDD APIs, ML runtimes, GPUs |
| Auto (`DATA_SECURITY_MODE_AUTO`) | Databricks picks | UI default; Standard unless an ML runtime, a GPU instance type or a runtime below 14.3 is selected, then Dedicated |
The API enum also still lists `NONE` and deprecated `LEGACY_*` modes (for example `LEGACY_TABLE_ACL`, deprecated from Databricks Runtime 15.0).

## 2. What standard mode blocks (check the limitations page for your runtime)
- Databricks Runtime for ML and GPU-enabled compute; R; spark-submit job tasks (use a JAR task).
- RDD APIs and the Scala Spark Context (`sc`, `spark.sparkContext`, `sqlContext`), including `sc.parallelize`. Python `sc` is supported on runtime 14.0 and above.
- Hive UDFs (use Unity Catalog UDFs); instance profiles for Kafka or Kinesis streaming (use service credentials).
- Access to the instance metadata service, and DBUtils reads from cloud storage except through an external location.
- On Databricks Runtime 19 and above, setting restricted Spark configuration properties (for example `spark.jars.packages`, `spark.driver.extraJavaOptions`) fails cluster creation or edit.
If a job fails on a limitation, either refactor (DataFrame APIs instead of RDDs) or move that job to dedicated.

## 3. Dedicated mode details
- Assigned to a single user or (Public Preview) a single group. Only workspace admins can assign dedicated compute to another user; for job compute the rule is checked when the job is created or edited.
- Dedicated is the recommended choice for RDD APIs, GPUs, R and privileged machine access; other workloads should use standard for cost efficiency.
- Fine-grain access control on dedicated compute requires Databricks Runtime 15.4 LTS or above and serverless compute enablement.

## 4. Choosing
- Databricks recommends standard unless a required feature is unsupported there.
- Interactive SQL/Python work, shared team cluster, general data engineering → **standard**.
- ML runtime, GPU, R, RDD-based legacy code → **dedicated**.

## 5. Enforce with cluster policies
```json
{
  "data_security_mode": {"type": "allowlist", "values": ["USER_ISOLATION", "SINGLE_USER"]}
}
```
Users without the Unrestricted cluster creation entitlement can only create compute through policies they have been granted. Policy attribute names follow the cluster API (`data_security_mode`, `spark_version`), so check the accepted values on the policy definition page for your workspace.

## 6. Migrating from legacy modes
Find clusters using `NONE` or the deprecated `LEGACY_*` modes, test the workloads on standard compute, fix RDD and Spark-config limitations, then restrict the allowed modes in policies.

## Verify
- [ ] No compute still uses `NONE` or `LEGACY_*` modes.
- [ ] Cluster policies restrict allowed access modes.
- [ ] A table with a row filter is readable on your standard and dedicated job compute.

## Checked

2026-11-09: reviewed against the Databricks documentation fetched this batch.

Confirmed: Auto resolution rules, supported languages per mode, the dedicated-mode use cases and assignment rules, `data_security_mode` enum values and legacy aliases, standard-mode limitations (ML runtime, GPU, R, spark-submit, RDD, Scala sc, Hive UDFs, instance profiles for streaming, IMDS), runtime 19 Spark config restrictions, and the unrestricted-creation entitlement (compute configuration, standard and dedicated limitations pages, clusters API reference).

Removed or corrected: the "formerly Shared/Single user" names, the table of Unity Catalog support per mode, the metastore allowlist wording for init scripts and libraries, the "not whitelisted" error text, DBFS root and instance-profile bullets, the serverless equivalence line, the auto:latest-lts policy default and CAN_USE/policy family claims, and the system.compute.clusters inventory steps (not on the pages read).

Method: documentation only; no commands were run.
