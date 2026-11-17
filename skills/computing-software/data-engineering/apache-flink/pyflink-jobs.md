---
id: computing-software.data-engineering.apache-flink.pyflink-jobs
name: pyflink-jobs
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, pyflink, python, table-api, datastream-api, python-udf, flink-sql]
level: practitioner
status: docs-checked
description: "Write and deploy PyFlink Table API and DataStream jobs: environment setup, connector jars, Python UDFs (general vs pandas), dependency shipping, and performance limits."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/dev/python/overview/
  - https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/dev/python/dependency_management/
  - https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/dev/python/faq/
  - https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/dev/python/table/udfs/vectorized_python_udfs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PyFlink DataStream and Table jobs

PyFlink (the `apache-flink` package; match the cluster's Flink version) wraps the Java APIs. Operators written in SQL/Table API run in the JVM; Python UDFs run in separate Python UDF worker processes. Python UDF execution needs Python 3.9, 3.10, 3.11 or 3.12 with PyFlink installed on both the client and the cluster (2.1 docs).

## Table API job
```python
from pyflink.table import EnvironmentSettings, TableEnvironment
t_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())
t_env.get_config().set("pipeline.jars", "file:///opt/flink/lib/flink-sql-connector-kafka-3.3.0-1.20.jar")
t_env.execute_sql("""
  CREATE TABLE clicks (user_id STRING, url STRING, ts TIMESTAMP_LTZ(3),
    WATERMARK FOR ts AS ts - INTERVAL '5' SECOND)
  WITH ('connector'='kafka','topic'='clicks','properties.bootstrap.servers'='b1:9092',
        'scan.startup.mode'='latest-offset','format'='json')""")
from pyflink.table.udf import udf
@udf(result_type="STRING")
def domain(url: str) -> str:
    from urllib.parse import urlparse
    return urlparse(url).netloc
t_env.create_temporary_function("domain", domain)
t_env.execute_sql("INSERT INTO sink SELECT user_id, domain(url) FROM clicks")
```
## DataStream job
```python
from pyflink.datastream import StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars("file:///opt/flink/lib/flink-sql-connector-kafka.jar")
ds = env.from_source(kafka_source, watermark_strategy, "clicks")
ds.key_by(lambda r: r[0]).map(lambda r: (r[0], 1)).print()
env.execute("clicks")
```
Keyed state, timers (`KeyedProcessFunction`) and windows are available in Python.

## Performance
- Push as much as possible into SQL; Python UDFs add serialisation per row.
- Vectorised UDFs: add `func_type="pandas"` to `udf`/`udaf`; batches move between JVM and Python in Arrow columnar format and are usually much faster. A pandas UDAF does not support partial aggregation and loads a whole group or window into memory.
- Batching knobs: `python.fn-execution.bundle.size` and `python.fn-execution.arrow.batch.size` (see the Python configuration page).

## Dependencies and deployment
- `python.files`/`add_python_file` for your modules, `python.requirements` (`set_python_requirements("requirements.txt")`) or `python.archives` with a packed venv (`venv.zip#venv` + `python.executable=venv/bin/python`) for third-party libs. The FAQ page shows a virtual-env zip added with `add_python_archive("venv.zip")` and `set_python_executable("venv.zip/venv/bin/python")`.
- Command-line equivalents: `-pyfs` / `--pyFiles` for Python files; see the Flink CLI page for the other `-py*` flags.
- Python version on TaskManagers must be a supported one and have the same packages.

## Verify
- [ ] Job runs locally (`python job.py` uses a mini cluster) and on the cluster with identical output.
- [ ] Python UDF operator busy-time is not the bottleneck (Flink UI backpressure).

## Checked
2026-11-09. Confirmed against the Flink 2.1 PyFlink pages (overview, dependency management, FAQ, Python UDFs, vectorized UDFs, Python configuration): supported Python versions, `func_type="pandas"`, `python.files`/`python.requirements`/`python.archives`/`python.executable`, `-pyfs`, `add_python_file`, `add_python_archive`, batch-size options. Removed: the thread/PEMJA mode and its version gate, managed-memory consumer weights, the Kubernetes operator submission snippet and the `flink run` flag line. Example code (connector jar path, topic names) is illustrative.
Method: documentation only; no commands were run.
