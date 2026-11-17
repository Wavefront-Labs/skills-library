---
id: computing-software.data-engineering.apache-airflow.remote-task-logging
name: remote-task-logging
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, remote-logging, task-logs, s3-logging, elasticsearch-logging, logging-config, log-retention, kubernetes-executor-logs, secrets-masking]
level: practitioner
status: docs-checked
description: "Ship Airflow task logs to S3/GCS/Azure or Elasticsearch/OpenSearch so they survive ephemeral workers: remote_logging config, connection, retention, and secret masking."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/logging-tasks.html
  - https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/logging/s3-task-handler.html
  - https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/mask-sensitive-values.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote task logging

**Goal:** every task attempt's log is viewable in the UI after the worker or pod is gone, and logs do not leak secrets.

## Object storage (S3 example)
```ini
[logging]
remote_logging = True
remote_base_log_folder = s3://<BUCKET>/airflow/logs
remote_log_conn_id = aws_default        # connection with read/write to that prefix (IRSA/role preferred)
encrypt_s3_logs = False                 # rely on bucket SSE-KMS
delete_local_logs = True                # remove the local copy after upload
```
Same pattern for GCS and Azure: see the matching provider's logging page. Requires the provider installed in the image.
While a task runs, the UI reads logs from the worker's log server (default port 8793, `[logging] worker_log_server_port`).

## Elasticsearch / OpenSearch
Elasticsearch is a streaming handler (alongside CloudWatch and GCP logging) in the logging docs; it suits organisations with central log platforms. Take the settings from the Elasticsearch provider's logging page.

## Retention and size
- Object storage: add a lifecycle rule that matches your `airflow db clean` retention.
- Chatty tasks (printing every row) make UI log pages unusable; log summaries.

## Secrets
Airflow masks sensitive connection fields and variables with sensitive-looking names (`[core] sensitive_var_conn_names` adds more names; see the mask-sensitive-values page). Mask runtime secrets explicitly:
```python
from airflow.sdk.log import mask_secret
mask_secret(token)
```
Do not log derived or encoded forms of secrets.

## Verify
- [ ] After a K8s worker pod is deleted, the task log is still visible in the UI.
- [ ] Objects appear under the expected prefix per dag/run/task/attempt.
- [ ] A test task printing a connection password shows `***`.

## Checked

2026-10-28. Confirmed against: S3 task handler page (remote_logging, remote_base_log_folder, remote_log_conn_id, encrypt_s3_logs), configuration reference (delete_local_logs, worker_log_server_port default 8793, sensitive_var_conn_names), mask-sensitive-values page (mask_secret from airflow.sdk.log). Removed (not confirmable in the fetched pages): Elasticsearch settings and log_id_template, 90-day example, per-attempt file name, 2.6+ gate, masking-rule specifics, GCS/Azure URI forms.

Method: documentation only; no commands were run.
