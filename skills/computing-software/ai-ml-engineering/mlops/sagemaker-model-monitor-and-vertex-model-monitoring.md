---
id: computing-software.ai-ml-engineering.mlops.sagemaker-model-monitor-and-vertex-model-monitoring
name: sagemaker-model-monitor-and-vertex-model-monitoring
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-monitoring, sagemaker-model-monitor, vertex-model-monitoring, data-capture, baseline-constraints, data-drift]
level: practitioner
status: draft
description: "Set up managed monitoring: SageMaker data capture, baselines, monitoring schedules and model-quality jobs, and Vertex AI skew/drift monitoring with thresholds."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-data-capture.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality.html
  - https://cloud.google.com/vertex-ai/docs/model-monitoring/overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SageMaker Model Monitor and Vertex AI Model Monitoring

**Goal:** get scheduled drift and quality reports with alerts from the managed service rather than a hand-built job.

## SageMaker: capture, baseline, schedule
1. **Capture** requests/responses at deploy time:
```python
from sagemaker.model_monitor import DataCaptureConfig
capture = DataCaptureConfig(enable_capture=True, sampling_percentage=20, destination_s3_uri="s3://bucket/capture/")
predictor = model.deploy(..., data_capture_config=capture)
```
2. **Baseline** from the training data (statistics + suggested constraints):
```python
from sagemaker.model_monitor import DefaultModelMonitor, DatasetFormat, CronExpressionGenerator
mon = DefaultModelMonitor(role=role, instance_type="ml.m5.xlarge", instance_count=1)
mon.suggest_baseline(baseline_dataset="s3://bucket/train.csv", dataset_format=DatasetFormat.csv(header=True),
                     output_s3_uri="s3://bucket/baseline/")
```
Review and edit `constraints.json` (types, completeness, allowed categories) - suggested constraints are a starting point and are often too strict on categoricals.
3. **Schedule**:
```python
mon.create_monitoring_schedule(endpoint_input=predictor.endpoint_name, output_s3_uri="s3://bucket/reports/",
    statistics=mon.baseline_statistics(), constraints=mon.suggested_constraints(),
    schedule_cron_expression=CronExpressionGenerator.hourly(), enable_cloudwatch_metrics=True)
```
Violations land in `constraint_violations.json`; per-feature metrics go to CloudWatch, where you alarm on them.

## Model quality (needs labels)
`ModelQualityMonitor` merges captured predictions with ground truth you upload to S3 keyed by `inference_id` (send `InferenceId` on each invoke). Without that ID, labels cannot be joined. Quality jobs lag by however long labels take to arrive.

Also available: bias drift and feature attribution drift monitors (SageMaker Clarify based).

## Vertex AI Model Monitoring
- Configure on an endpoint (or batch prediction) with a **training dataset** for skew detection and/or drift detection against recent serving data.
- Per-feature thresholds; categorical features use L-infinity distance, numerical features Jensen-Shannon divergence. Alerts go to email/Cloud Monitoring notification channels.
- Sampling rate and monitoring window control cost; logging all requests to BigQuery is a separate request-response logging setting.

## Gotchas
- Preprocessing inside the container: captured inputs are raw payloads, so the baseline must also be raw-input format, not post-feature-engineering.
- Low traffic + hourly schedule = tiny samples and noisy alerts; widen the window or lower frequency.
- Captured payloads may include PII; set S3 encryption and retention.

## Verify
- [ ] One manual monitoring execution produced a report and CloudWatch metrics.
- [ ] Alarms fire on a synthetic drifted batch.
- [ ] Ground-truth join tested end to end with inference IDs.
