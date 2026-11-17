---
id: computing-software.data-engineering.apache-spark.spark-connect-client
name: spark-connect-client
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-connect, pyspark-connect, sc-remote, grpc, databricks-connect, thin-client, spark-4]
level: practitioner
status: docs-checked
description: "Use Spark Connect: start the server, connect with sc:// from a thin PySpark client, what APIs are unsupported (RDD, SparkContext), and session/auth gotchas."
sources:
  - https://spark.apache.org/docs/latest/spark-connect-overview.html
  - https://spark.apache.org/docs/latest/spark-connect-gotchas.html
  - https://github.com/apache/spark/blob/master/sql/connect/docs/client-connection-string.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spark Connect: thin clients over gRPC

**Goal:** run DataFrame code from a laptop, IDE, or service against a remote Spark cluster without shipping a full Spark/JVM driver locally.

Spark Connect splits the driver: the client builds unresolved logical plans, encoded with protocol buffers, and sends them over gRPC (the local default server port is 15002); the server translates them into Spark's logical plan and executes them with the standard Spark process.

## Server
```bash
./sbin/start-connect-server.sh
```
`./bin/spark-connect-shell` instead starts an interactive Scala shell that hosts the Connect server in the shell process. Use the same package version as your Spark version.

## Client
```bash
pip install pyspark-client==<SPARK_VERSION>      # the Python client package named in the Spark Connect guide
```
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.remote("sc://<HOST>:15002").getOrCreate()
# TLS/auth via connection-string parameters, e.g. sc://host:443/;use_ssl=true;token=<TOKEN>
df = spark.read.table("sales.orders").groupBy("country").count()
df.show()
```
Or `export SPARK_REMOTE=sc://<HOST>:15002` and use `SparkSession.builder.getOrCreate()`.

## What changes
- The protocol does not support all execution APIs, most importantly RDDs; the client has no access to the static Spark configuration or the SparkContext, and cannot reach private JVM-backed fields such as `df._jdf`. Rewrite with DataFrame APIs.
- Operations that reference user-defined code (UDFs, `filter`, `map`) need their classes or artifacts uploaded to the server; for JVM clients register a `ClassFinder` and use `SparkSession#addArtifact` for jars.
- Analysis is deferred: errors, and dependent session state such as UDFs, temp views and configs, are evaluated when the plan executes, unlike Spark Classic's eager analysis (see the Spark Connect gotchas guide).
- The client is session-based: session-local state such as temp views and runtime SQL configurations belongs to the Connect session.

## Gotchas
- Use the same version for the client package and the Spark server.
- Connection strings are documented in the Spark Connect client-connection-string reference; `use_ssl=true` verifies the server certificate against the system's trusted CA store.

## Verify
- [ ] `spark.version` from the client returns the server's version.
- [ ] A query from the client shows up in the server's monitoring (see the Connect endpoints under `/applications/<id>/connect/` in the REST API).

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in spark-connect-overview.md and spark-connect-gotchas.md: gRPC with protobuf-encoded unresolved logical plans, default port 15002, start-connect-server.sh and spark-connect-shell, pyspark-client install, SPARK_REMOTE, connection-string use_ssl and token parameters, no RDD / SparkContext / static config access, UDF class and JAR artifact upload, deferred analysis and session-state semantics; monitoring.md lists /applications/[app-id]/connect/sessions and /operations. Removed the unconfirmed version history, Databricks Connect section, exception class names, schema round-trip tip, gRPC size-limit and no-auth claims, and the pinned 3.5.1 versions.

Method: documentation only; no commands were run.
