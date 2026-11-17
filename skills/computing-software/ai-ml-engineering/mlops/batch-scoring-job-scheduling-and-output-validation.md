---
id: computing-software.ai-ml-engineering.mlops.batch-scoring-job-scheduling-and-output-validation
name: batch-scoring-job-scheduling-and-output-validation
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, batch-scoring-validation, batch-inference, data-validation, idempotency, scheduling]
level: practitioner
status: draft
description: "Run batch scoring jobs that are idempotent and safe to publish: input readiness, partitioned overwrite outputs, row and distribution checks, staging-then-swap, and SLA alerts."
sources:
  - https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
  - https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html
  - https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/datasets.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Batch scoring job scheduling and output validation

**Goal:** daily or hourly predictions land on time, are complete and plausible, and a bad run never overwrites good published predictions.

## Job shape
1. **Readiness gate:** input partition exists, row count within expected range, feature freshness OK.
2. **Score** with a pinned model version (resolve the alias once at job start and record the version).
3. **Write to staging** partition `predictions_staging/run_date=2026-10-18/`.
4. **Validate** staging output.
5. **Publish** atomically (partition overwrite, table swap, or view pointer update).
6. **Emit** completion event / marker for consumers.

## Idempotency
Parameterise by logical date. Reruns overwrite that date's partition (`INSERT OVERWRITE` / Delta `replaceWhere`) rather than appending, so retries never duplicate predictions.

## Validation checks
| Check | Example rule |
|---|---|
| Completeness | output rows == eligible input rows |
| Keys | entity id unique, non-null |
| Nulls | 0 null scores |
| Range | probabilities in [0, 1]; regression output within business bounds |
| Distribution | PSI vs previous run < 0.2; mean score within 3 sigma of trailing 30 runs |
| Segments | no segment's volume or mean score shifts more than X% |
| Metadata | model version, run date, scored_at columns populated |
Hard failures block publish; soft warnings publish and page the owner.
```python
import numpy as np
def psi(expected, actual, bins=10):
    cuts = np.quantile(expected, np.linspace(0, 1, bins + 1)); cuts[0], cuts[-1] = -np.inf, np.inf
    e = np.histogram(expected, cuts)[0] / len(expected) + 1e-6
    a = np.histogram(actual, cuts)[0] / len(actual) + 1e-6
    return float(np.sum((a - e) * np.log(a / e)))
```

## Scheduling
- Schedule after upstream data SLAs, or trigger on the upstream dataset event rather than a fixed time.
- Set an SLA alert for "predictions not published by HH:MM" - consumers notice missing data before failed jobs.
- Retry transient failures with backoff; do not auto-retry validation failures.
- Keep the last good partition available; consumers should read the latest published, not the latest attempted.

## Verify
- [ ] Rerunning a date yields identical row counts (no duplicates).
- [ ] A forced distribution shift blocks publishing in a test run.
- [ ] Missing-publication alert tested.
