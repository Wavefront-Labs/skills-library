---
id: computing-software.cloud-infrastructure-engineering.aws.athena-for-apache-spark
name: athena-for-apache-spark
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, athena, spark, pyspark, notebooks, dpu, iceberg, athena-spark]
level: practitioner
status: docs-checked
description: "Run interactive PySpark on Athena: Spark-enabled workgroups, notebooks and sessions, DPU sizing, table formats and API-driven calculations."
sources: ["https://docs.aws.amazon.com/athena/latest/ug/notebooks-spark.html", "https://docs.aws.amazon.com/athena/latest/ug/notebooks-spark-getting-started.html", "https://docs.aws.amazon.com/athena/latest/ug/notebooks-spark-considerations-and-limitations.html", "https://docs.aws.amazon.com/athena/latest/ug/notebooks-spark-table-formats-apache-iceberg.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Athena for Apache Spark

**Use:** interactive PySpark over data in S3 and the catalog, without managing a cluster.

## Set up
- Create a Spark-enabled workgroup, switch to it in the notebook explorer, then create or open a notebook; opening a notebook starts a session for it automatically.
- Check the Athena User Guide for the execution role and result-location settings the workgroup needs.

## Sessions
- A DPU is 4 vCPUs and 16 GB of memory.
- Edit a session (Session menu, Edit session) for the table format (Delta Lake, Hudi, Iceberg or Custom), encryption, idle timeout and maximum concurrent DPUs.
- Default session: 20 maximum DPUs. Max concurrent DPUs: default 20, minimum 3, maximum 60.
- Idle timeout: 1 to 480 minutes, default 20; set it short.
- Coordinator and executor size: 1 DPU each (the only possible value at the time of the docs).
- Closing a notebook tab does not end the session: use Session, Terminate.

```python
df = spark.sql("SELECT * FROM curated.orders WHERE order_date >= '2026-10-01'")
df.groupBy("country").count().show()
```

## API
```bash
aws athena start-session --work-group spark-wg \
  --engine-configuration CoordinatorDpuSize=1,MaxConcurrentDpus=20,DefaultExecutorDpuSize=1
aws athena start-calculation-execution --session-id "$SID" --code-block 'print(spark.range(10).count())'
aws athena get-calculation-execution --calculation-execution-id "$CID"
aws athena terminate-session --session-id "$SID"
```

## Limits
- One active session per notebook.
- `pip install` is not supported in sessions; MLlib and `pyspark.ml` are not supported. See the preinstalled library list.
- Users who open an existing session in a workgroup share that notebook: only open sessions you created.

## Verify
- [ ] The session has an idle timeout and DPU cap you chose.
- [ ] A notebook reads a catalog table (and an Iceberg table when that format is selected).

## Checked
2026-10-28. Confirmed in the Athena User Guide pages in `sources` (Get started, considerations and limitations) and the botocore model for `StartSession`; commands checked with check_commands.
Removed (not confirmed on the fetched pages): the one-second startup claim, billing wording, the Glue/Lake Formation/KMS role details, `.ipynb` import, zipped library handling, the engine-choice table, and region-availability remarks.
Method: documentation only; no commands were run.
