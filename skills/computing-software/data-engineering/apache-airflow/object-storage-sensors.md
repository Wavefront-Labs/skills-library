---
id: computing-software.data-engineering.apache-airflow.object-storage-sensors
name: object-storage-sensors
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, sensors, s3keysensor, gcsobjectexistencesensor, wildcard-match, deferrable-sensor, success-marker, file-arrival, sensor-timeout]
level: practitioner
status: docs-checked
description: "Wait for files in S3/GCS with Airflow sensors: S3KeySensor wildcards and check_fn, deferrable mode, _SUCCESS markers vs partial uploads, timeouts and soft_fail."
sources:
  - https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/s3/s3.html#wait-on-an-amazon-s3-key
  - https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/gcs.html
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sensors for files in object storage

**Goal:** start processing exactly when a complete file set has landed, without burning worker slots or waiting forever.

## S3KeySensor
```python
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

wait = S3KeySensor(
    task_id="wait_for_vendor_drop",
    bucket_name="landing",
    bucket_key="vendor/{{ ds }}/_SUCCESS",       # templated
    aws_conn_id="aws_default",
    deferrable=True,                             # waits in the triggerer
    poke_interval=300,
    timeout=6 * 3600,
    soft_fail=False,
)
```
- `wildcard_match=True` for patterns (`vendor/{{ ds }}/*.csv`).
- `check_fn=lambda files: sum(f["Size"] for f in files) > 0` to validate matched objects (size, count).
- GCS: `GCSUploadSessionCompleteSensor` (waits until no new objects for `inactivity_period`). 

## Complete vs partial uploads
- Wait for a **marker** (`_SUCCESS`, `manifest.json`) written last by the producer: the only reliable "batch complete" signal.
- No marker possible? Wait for an expected count, or for inactivity (no new objects for N minutes), and validate sizes/row counts afterwards.
- Partial **sets** of files are the main risk; confirm in the S3 docs when a single object becomes visible.

## Modes and limits
- `poke` mode holds a worker slot for the whole wait; `mode="reschedule"` frees it between pokes; `deferrable=True` is cheapest.
- Always set `timeout` (default 7 days!). `soft_fail=True` marks the task skipped on timeout (use when "no file today" is legitimate).
- `exponential_backoff=True` for long waits.
- Listing large prefixes every few minutes costs API calls; narrow the key prefix by date.

## Alternative: push instead of poll
Airflow's event-driven scheduling (asset watchers with a trigger; see the Airflow docs) can replace polling and its API cost.

## Verify
- [ ] Sensor task shows `deferred` (or `up_for_reschedule`) while waiting, not `running`.
- [ ] Uploading files without the marker does not start processing; adding the marker does.
- [ ] Timeout behaviour (fail vs skip) matches the business rule.

## Checked

2026-10-28. Confirmed against: Amazon provider S3 operator page (S3KeySensor, wildcard_match, check_fn, deferrable examples), Google provider GCS page (GCSUploadSessionCompleteSensor, inactivity_period), Airflow sensors page (soft_fail, exponential_backoff, reschedule), configuration reference ([sensors] default_timeout 604800 s = 7 days). Removed (not confirmable in the fetched pages): Azure sensor names, other GCS sensor class names, multipart-visibility claim, SQS/Lambda route.

Method: documentation only; no commands were run.
