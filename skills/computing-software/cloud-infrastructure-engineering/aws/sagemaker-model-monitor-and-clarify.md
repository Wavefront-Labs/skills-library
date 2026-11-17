---
id: computing-software.cloud-infrastructure-engineering.aws.sagemaker-model-monitor-and-clarify
name: sagemaker-model-monitor-and-clarify
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sagemaker, model-monitor, clarify, data-drift, bias-detection, explainability, data-capture]
level: practitioner
status: draft
description: "Watch production ML models with SageMaker Model Monitor (data quality, model quality, bias and attribution drift) and SageMaker Clarify bias metrics and SHAP explanations."
sources: ["Amazon SageMaker AI Developer Guide - Data and model quality monitoring with Amazon SageMaker Model Monitor", "Amazon SageMaker AI Developer Guide - Capture data from real-time endpoints", "Amazon SageMaker AI Developer Guide - Fairness, model explainability and bias detection with SageMaker Clarify"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SageMaker Model Monitor and Clarify

## Capture data
```python
from sagemaker.model_monitor import DataCaptureConfig
capture = DataCaptureConfig(enable_capture=True, sampling_percentage=20,
                            destination_s3_uri="s3://ml-monitor/capture/fraud")
predictor = model.deploy(initial_instance_count=2, instance_type="ml.m5.large", data_capture_config=capture)
```
Requests and responses land in S3 as JSONL per hour. Batch transform jobs can capture too.

## Baseline and schedules
```python
from sagemaker.model_monitor import DefaultModelMonitor, CronExpressionGenerator
mon = DefaultModelMonitor(role=role, instance_count=1, instance_type="ml.m5.xlarge")
mon.suggest_baseline(baseline_dataset="s3://ml-data/fraud/train.csv",
                     dataset_format=DatasetFormat.csv(header=True),
                     output_s3_uri="s3://ml-monitor/baseline/fraud")
mon.create_monitoring_schedule(endpoint_input=predictor.endpoint_name,
    output_s3_uri="s3://ml-monitor/reports/fraud",
    statistics=mon.baseline_statistics(), constraints=mon.suggested_constraints(),
    schedule_cron_expression=CronExpressionGenerator.hourly(), enable_cloudwatch_metrics=True)
```
| Monitor | Detects | Needs |
|---|---|---|
| Data quality | schema violations, missing values, distribution drift vs baseline | baseline from training data |
| Model quality | accuracy/precision/recall/RMSE degradation | **ground truth labels** uploaded to S3 and merged with captures |
| Bias drift (Clarify) | change in bias metrics on live data | Clarify bias config |
| Feature attribution drift (Clarify) | changes in SHAP feature importance | Clarify explainability config |
- Violations reports (`constraint_violations.json`) go to S3; CloudWatch metrics per feature enable alarms (e.g. drift distance above threshold).
- Edit `constraints.json` to relax noisy constraints rather than ignoring alerts.

## Clarify
- **Pre-training bias** metrics on the dataset (class imbalance CI, difference in proportions of labels DPL).
- **Post-training bias** on predictions (disparate impact DI, difference in positive proportions DPPL, accuracy difference).
- **Explainability:** SHAP values per prediction and global feature importance; partial dependence plots.
- Run as processing jobs (`SageMakerClarifyProcessor`) in pipelines before registration, and as monitors after deployment.

## Gotchas
- Monitoring jobs cost processing instance time each run; hourly is the minimum frequency.
- Ground truth delays (fraud labels arrive weeks later) shift model quality monitoring windows.
- Capture contains real inputs (PII): encrypt, restrict, set lifecycle.

## Verify
- [ ] Schedules show completed executions; CloudWatch alarms on drift metrics exist.
- [ ] A synthetic shifted dataset triggers a data quality violation in test.
