---
id: computing-software.cloud-infrastructure-engineering.aws.neptune-bulk-loader-and-analytics
name: neptune-bulk-loader-and-analytics
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, neptune, neptune-loader, bulk-load, neptune-analytics, graph-database, gremlin-csv, opencypher-csv, rdf, graph-algorithms, s3-vpc-endpoint, neptune-graph]
level: advanced
status: docs-checked
description: "Bulk-load graph data into Neptune from S3 (CSV, openCypher, RDF) with the loader API, debug load errors, and load or analyse graphs in Neptune Analytics with built-in algorithms."
sources: ["https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load.html", "https://docs.aws.amazon.com/neptune/latest/userguide/load-api-reference-load.html", "https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load-tutorial-format.html", "https://docs.aws.amazon.com/neptune-analytics/latest/userguide/what-is-neptune-analytics.html", "https://docs.aws.amazon.com/neptune-analytics/latest/userguide/bulk-import.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Neptune bulk loader and Neptune Analytics

**Goal:** large graphs get into Neptune with the bulk loader instead of single inserts, and graph-wide
analytics run in Neptune Analytics instead of exporting to another engine.

## 1. Prepare data in S3
- Property graph CSV (Gremlin format, `format` = `csv`): vertex files need `~id` (required) and optionally `~label`
  plus typed columns such as `name:String`, `age:Int`; edge files need `~id`, `~from`, `~to` (required) and optionally `~label`.
  Labels are case sensitive.
- openCypher CSV (`format` = `opencypher`): system columns `:ID`, `:LABEL`, `:START_ID`, `:END_ID`, `:TYPE` with typed properties.
- RDF: `ntriples`, `nquads`, `rdfxml`, `turtle`.
- The S3 bucket must be in the same Region as the cluster. The loader parses large files into chunks and loads
  them in parallel; a very large number of tiny files can slow the load.

## 2. Network and IAM
- The loader requires an Amazon S3 **VPC endpoint of type Gateway** (`com.amazonaws.<region>.s3`) in the cluster's VPC.
- Create an IAM role that Neptune can assume (the tutorial's `iam:PassRole` condition names `rds.amazonaws.com`) with read access to the
  bucket (`s3:GetObject`, `s3:ListBucket`) and associate it with the cluster:
  `aws neptune add-role-to-db-cluster --db-cluster-identifier g --role-arn <ROLE>`. SSE-S3 data loads directly; SSE-KMS data
  loads if the role has the needed KMS permissions (otherwise `LOAD_FAILED`); SSE-C is not currently supported.

## 3. Load
From a host inside the VPC. The User Guide shows an HTTP POST to the loader endpoint (and the equivalent
`aws neptunedata start-loader-job --endpoint-url https://<cluster-endpoint>:<port> --source ... --format csv --iam-role-arn ... --s3-bucket-region ...`);
if IAM database authentication is enabled the request must be SigV4-signed:
```bash
curl -X POST https://<cluster-endpoint>:<port>/loader -H 'Content-Type: application/json' -d '{
  "source": "s3://graph-load/2026-10-16/", "format": "csv",
  "iamRoleArn": "arn:aws:iam::<ACCOUNT_ID>:role/NeptuneLoad", "region": "us-east-1",
  "failOnError": "FALSE", "parallelism": "HIGH", "updateSingleCardinalityProperties": "FALSE",
  "queueRequest": "TRUE"}'
# -> {"payload":{"loadId":"..."}}
curl "https://<cluster-endpoint>:<port>/loader/<loadId>?details=true&errors=true&page=1&errorsPerPage=20"
```
- `parallelism`: `LOW`, `MEDIUM`, `HIGH` (default), `OVERSUBSCRIBE`, which use progressively more of the instance's threads;
  higher settings compete with query traffic, so load in a quiet window or on a dedicated cluster.
- Within one S3 prefix the loader loads vertex files first and edge files afterwards (it scans the files first; set
  `edgeOnlyLoad` to TRUE to skip that scan if you load only edges). Best practice from the User Guide: put nodes and edges
  in separate prefixes. Edges whose `~from`/`~to` vertex is missing report `FROM_OR_TO_VERTEX_ARE_MISSING`.
- `queueRequest` = `TRUE` lets you queue up to 64 job requests; `dependencies` chains jobs (an unmet dependency gives
  `LOAD_FAILED_BECAUSE_DEPENDENCY_NOT_SATISFIED`).
- Statuses include `LOAD_COMPLETED` and `LOAD_FAILED`; read per-record errors with `details=true&errors=true`.

## 4. Neptune Analytics
In-memory, memory-optimised analytics graph (the User Guide says it complements Neptune Database; you can load from a
Neptune Database graph or snapshot, or from S3).
```bash
aws neptune-graph create-graph-using-import-task --graph-name fraud-analytics \
  --source s3://graph-load/2026-10-16/ --format CSV --role-arn <ROLE> \
  --min-provisioned-memory 128 --max-provisioned-memory 256
aws neptune-graph list-import-tasks
```
`--format` accepts `CSV`, `OPEN_CYPHER`, `PARQUET` or `NTRIPLES`; provisioned memory ranges from 16 to 24576 in the API model.
Query with openCypher via `aws neptune-graph execute-query --graph-identifier <ID> --language open_cypher --query-string '...'`
(`open_cypher` is the only language value in the model). Neptune Analytics provides a library of graph algorithms and
vector search; use the algorithm reference in its User Guide for the exact procedure syntax.

## Gotchas
- Validate CSV headers before a multi-hour load; labels are case sensitive and an empty label (`""`) is an error.
- Rows with the same `~id` are applied to a single vertex (or edge); keep IDs unique unless you mean to merge.
- For vertex properties, multiple values load into a set by default, while edges always have single cardinality;
  `updateSingleCardinalityProperties` changes how single-cardinality values are replaced. Decide before loading.
- Neptune Analytics costs are not checked here; delete graphs you no longer need.

## Verify
- [ ] `GET /loader/<loadId>` reports `LOAD_COMPLETED` and `totalRecords` equals file row counts.
- [ ] `g.V().count()` / `MATCH (n) RETURN count(n)` matches expected vertex totals.
- [ ] Neptune Analytics import task finishes successfully (`list-import-tasks`) and a test query returns expected counts.
- [ ] Load errors (if any) reviewed and the bad lines fixed at source.

## Checked
Date: 2026-10-27. Sources: Neptune User Guide pages load-api-reference-load (parameters, parallelism, queueing,
encryption modes), load-api-reference-load-examples (`neptunedata start-loader-job`), bulk-load-tutorial-format-gremlin
and -opencypher (headers, cardinality, duplicate IDs), bulk-load-optimize (vertex-first loading,
`FROM_OR_TO_VERTEX_ARE_MISSING`), bulk-load-tutorial-vpc and -IAM (Gateway endpoint, PassRole), load-api-reference-status
(`LOAD_COMPLETED`, `LOAD_FAILED`); Neptune Analytics What is page; botocore `neptune-graph` model (import task
flags, format and language enums, memory range). Corrected: the loader supports SSE-KMS (SSE-C is unsupported), the
`LOAD_COMPLETED_WITH_ERRORS` status was not found, duplicate `~id` rows merge for edges as well as vertices.
Removed gzip, file size, `m-NCU`, PageRank procedure syntax, loader port and billing claims (not confirmed).
Method: documentation only; no commands were run.
