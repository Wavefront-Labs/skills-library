---
id: computing-software.data-engineering.apache-spark.spark-submit-and-deploy-modes
name: spark-submit-and-deploy-modes
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-submit, deploy-mode, cluster-mode, client-mode, py-files, packages, spark-conf, cluster-manager, pyspark]
level: practitioner
status: docs-checked
description: "Submit Spark apps with spark-submit: client vs cluster deploy mode, --master URLs, resource flags, shipping Python deps (--py-files, archives, venv) and --packages/--jars."
sources:
  - https://spark.apache.org/docs/latest/submitting-applications.html
  - https://spark.apache.org/docs/latest/running-on-yarn.html
  - https://spark.apache.org/docs/latest/spark-standalone.html
  - https://github.com/apache/spark/blob/master/python/docs/source/tutorial/python_packaging.rst
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# spark-submit and deploy modes

**Goal:** launch a Spark application reproducibly with the right master, deploy mode, resources and dependencies.

## Skeleton
```bash
spark-submit \
  --master yarn \                     # or k8s://https://<API>:6443, spark://<host>:7077, local[*]
  --deploy-mode cluster \             # driver on the cluster (prod); client = driver on this machine
  --name daily-orders \
  --driver-memory 4g --executor-memory 8g --executor-cores 4 \
  --num-executors 10 \                # or dynamic allocation instead
  --conf spark.sql.shuffle.partitions=400 \
  --conf spark.dynamicAllocation.enabled=true \
  --py-files deps.zip \
  --packages org.apache.spark:spark-sql-kafka-0-10_<SCALA_BINARY>:<SPARK_VERSION> \
  main.py --date 2026-10-15
```
Arguments after the application file go to your program, not to Spark.

## Client vs cluster mode
| | client | cluster |
|---|---|---|
| Driver runs | Where you ran spark-submit | Inside the cluster (YARN AM / K8s pod) |
| Use for | Gateway machines close to the workers; REPLs such as the Spark shell (input and output attached to the console) | Submitting from a machine far from the workers (minimises driver-executor latency) |
| Note | The driver is inside the `spark-submit` process | Logs live in the cluster (for example `yarn logs`) |

The standalone mode does not support cluster mode for Python applications.

## Config precedence
Values set on `SparkConf` take the highest precedence, then flags passed to `spark-submit`, then `spark-defaults.conf` (`--properties-file` replaces it unless `--load-spark-defaults` is passed; `--verbose` prints where options come from). Some settings (driver memory in client mode, `spark.executor.instances` once started) only take effect at launch: setting `spark.driver.memory` inside the code in client mode is too late because the JVM is already running.

## Shipping Python dependencies
- Pure-Python modules: `--py-files` accepts `.py`, `.zip` or `.egg` files (package multiple files into a `.zip` or `.egg`).
- Packages with native code: build a packed environment and ship it:
  ```bash
  python -m venv env && source env/bin/activate && pip install pandas pyarrow venv-pack
  venv-pack -o env.tar.gz
  export PYSPARK_DRIVER_PYTHON=python      # do not set in YARN or Kubernetes cluster mode
  export PYSPARK_PYTHON=./environment/bin/python
  spark-submit --archives env.tar.gz#environment main.py
  ```
  (`conda-pack` and PEX are the other documented options). `--archives` (or `spark.archives`, `spark.yarn.dist.archives` on YARN) unpacks the archive on executors; the `#environment` suffix is the directory name.
- JVM deps: `--packages` takes a comma-delimited list of Maven coordinates and handles transitive dependencies; `--repositories` adds resolvers; `--jars` ships local jars. Match the Scala suffix and Spark version to your Spark build.

## Gotchas
- A master set in code on `SparkConf` outranks the `--master` flag (SparkConf has the highest precedence); do not hard-code `local[*]` in production code.
- On YARN cluster mode, `spark.yarn.submit.waitAppCompletion` (default true) controls whether the client stays alive reporting status until the application completes; if false the client exits after submission.

## Verify
- [ ] The Spark UI Environment tab shows the intended configuration.
- [ ] The Executors tab shows the requested executor count, cores and memory.
- [ ] Job runs from a clean machine (no locally installed libs are being relied on).

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in submitting-applications.md: precedence (SparkConf, spark-submit flags, defaults file), --properties-file / --load-spark-defaults, --verbose, client vs cluster guidance, standalone Python cluster-mode limitation, --py-files file types, --packages / --repositories behaviour. Confirmed in python_packaging.rst: venv-pack, conda-pack and PEX, --archives with #environment, spark.archives / spark.yarn.dist.archives, PYSPARK_DRIVER_PYTHON not set in cluster modes. Confirmed in running-on-yarn.md: spark.yarn.submit.waitAppCompletion default true. Removed the pinned 3.5.1 coordinates, the exit-code and NoSuchMethodError claims.

Method: documentation only; no commands were run.
