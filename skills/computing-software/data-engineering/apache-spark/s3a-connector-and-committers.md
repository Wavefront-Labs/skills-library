---
id: computing-software.data-engineering.apache-spark.s3a-connector-and-committers
name: s3a-connector-and-committers
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, s3a-committer, s3a, hadoop-aws, magic-committer, directory-committer, object-storage, cloud-storage, file-output-committer]
level: advanced
status: docs-checked
description: "Configure Spark on S3 via hadoop-aws S3A: credentials, the S3A magic/staging committers instead of rename, connection tuning, and fixing slow or duplicate job output."
sources:
  - https://spark.apache.org/docs/latest/cloud-integration.html
  - https://hadoop.apache.org/docs/stable/hadoop-aws/tools/hadoop-aws/index.html
  - https://hadoop.apache.org/docs/stable/hadoop-aws/tools/hadoop-aws/committers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3A connector and output committers

**Goal:** Spark writes to S3 that are fast and correct. The default `FileOutputCommitter` relies on rename, which on S3 is copy+delete: slow and non-atomic.

Applies to open-source Spark (k8s, standalone, self-managed). EMR uses EMRFS and its own S3-optimized committer; Databricks uses DBIO. Table formats (Delta/Iceberg/Hudi) commit through their own log and do not need these committers.

## Dependencies
`hadoop-aws` must match the Hadoop version of your Spark build, plus the AWS SDK bundle it was built with (see the Spark cloud-integration page for the `spark-hadoop-cloud` module):
```bash
spark-submit --packages org.apache.hadoop:hadoop-aws:<HADOOP_VERSION> ...
```
Mismatched versions typically surface as class-loading errors on `S3AFileSystem`.

## Credentials (pick one)
```properties
spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.auth.IAMInstanceCredentialsProvider   # IAM credentials of the EC2 VM / container
# unset = default chain: Temporary, Simple, EnvironmentVariable, then IAMInstance providers
```
Never put access keys in code; per-bucket overrides: `spark.hadoop.fs.s3a.bucket.<bucket>.endpoint=...`.

## Committers
```properties
spark.hadoop.fs.s3a.committer.name=magic            # or directory / partitioned
spark.sql.sources.commitProtocolClass=org.apache.spark.internal.io.cloud.PathOutputCommitProtocol
spark.sql.parquet.output.committer.class=org.apache.spark.internal.io.cloud.BindingParquetOutputCommitter
```
Needs the `spark-hadoop-cloud` module on the classpath. Without `fs.s3a.committer.name` the classic committer is used. The magic committer has been enabled by default since Hadoop 3.3.1 (`fs.s3a.committer.magic.enabled`).
- **directory** (staging): tasks write to local disk, job commit uploads via multipart. Good default, needs local disk space.
- **partitioned**: like directory but conflict resolution per partition (`fs.s3a.committer.staging.conflict-mode=replace`), for dynamic partition overwrite style jobs.
- **magic**: writes multipart uploads directly to S3 under `__magic/`, completed at job commit. Least local disk; S3 is now consistent, so the S3Guard requirement in the original committer design no longer applies.

Check: a `_SUCCESS` file of 0 bytes means the classic FileOutputCommitter committed the job; the S3A committers write a non-empty JSON file whose `committer` field names the committer used.

## Throughput tuning
```properties
spark.hadoop.fs.s3a.connection.maximum=200
spark.hadoop.fs.s3a.threads.max=64
spark.hadoop.fs.s3a.fast.upload.buffer=disk     # or bytebuffer for small executors
spark.hadoop.fs.s3a.multipart.size=128M
spark.hadoop.fs.s3a.experimental.input.fadvise=random   # input policy; see the hadoop-aws fadvise section
```

## Gotchas
- Abandoned multipart uploads from failed jobs are billed as storage: add an S3 lifecycle rule to abort incomplete uploads (`fs.s3a.multipart.purge` is another option).
- `mode("overwrite")` with the classic committer deletes the target first: a failure leaves nothing.

## Verify
- [ ] `_SUCCESS` is non-empty JSON and its `committer` field names the committer you configured.
- [ ] Job commit time in driver log is seconds, not minutes of renames.

## Checked

2026-11-01. Confirmed against the Spark cloud-integration page (committer class settings, `spark-hadoop-cloud`) and the hadoop-aws index and committers pages (default credential chain, `IAMInstanceCredentialsProvider`, `fs.s3a.committer.name`, magic enabled by default since 3.3.1, `_SUCCESS` JSON, multipart purge, S3Guard note). Removed: the web-identity provider class, pinned 3.3.4 version, 503 SlowDown note, fadvise per-format advice, and the cost/consistency date claims not on those pages.

Method: documentation only; no commands were run.
