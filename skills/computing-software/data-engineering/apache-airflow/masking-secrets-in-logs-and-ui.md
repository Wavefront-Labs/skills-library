---
id: computing-software.data-engineering.apache-airflow.masking-secrets-in-logs-and-ui
name: masking-secrets-in-logs-and-ui
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, secret-masking, sensitive-fields, logging-security, mask-secret]
level: practitioner
status: docs-checked
description: "Keep secrets out of Airflow task logs and the UI: automatic masking of connections and sensitive variables, extending the keyword list, mask_secret, and its limits."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/security/secrets/mask-sensitive-values.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/config.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Masking sensitive values in logs and UI

**Goal:** a password printed by a library or rendered in a template shows as `***`, not the secret.

## What is masked automatically
- Connection passwords of every connection a task accesses, and connection extras, Variables, rendered template dictionaries and XCom dictionaries whose key or name contains a sensitive keyword: `access_token, api_key, apikey, authorization, passphrase, passwd, password, private_key, secret, token, keyfile_dict, service_account`.
- Controlled by `[core] hide_sensitive_var_conn_fields` (default `True`); connection passwords are always hidden in logs.
- Masking applies to task logs, the Variables UI and the Rendered fields views.

## Extend the keyword list
```ini
[core]
sensitive_var_conn_names = client_cert,signing_key,dsn
```
These are added to the default keywords; any Variable name or extra field name containing one is masked. The env var `AIRFLOW__CORE__SENSITIVE_VAR_CONN_NAMES` does the same.

## Mask a runtime value
```python
from airflow.sdk.log import mask_secret
token = fetch_token()
mask_secret(token)          # later output containing it is masked
```
Call it in the task function or an operator's `execute` **before** anything logs the value; the mask has no effect on output produced earlier.

## Limits
- Masking looks for the specific value anywhere in the output, so a short value masks every occurrence of itself: a password of `a` turns every `a` into `***`. Secrets shorter than `[logging] min_length_masked_secret` (default 5) are not masked in log messages.
- Automatic masking is triggered by Connection or Variable access; a sensitive value passed through XCom or another side channel is not masked when printed downstream.
- Secrets passed through environment variables (for example to `KubernetesPodOperator`) are visible to anyone who can see the process environment and are not masked; use native Kubernetes secrets or Airflow Connections or Variables.

## Verify
Run a test task that logs the secret; confirm `***` in the task log and in the Rendered fields view.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: the default keyword list (including `keyfile_dict` and `service_account`), `hide_sensitive_var_conn_fields` default True, `sensitive_var_conn_names` extending the defaults, `min_length_masked_secret` default 5, `mask_secret` from `airflow.sdk.log` and the call-before-output rule, value-based masking, the XCom side-channel caveat and the environment variable warning (mask-sensitive-values.rst). Removed the Airflow 2.x import path, the transformed-secret and `bash_command` claims, which are not documented.

Method: documentation only; no commands were run.
