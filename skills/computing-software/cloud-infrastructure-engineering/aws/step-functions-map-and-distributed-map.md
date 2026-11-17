---
id: computing-software.cloud-infrastructure-engineering.aws.step-functions-map-and-distributed-map
name: step-functions-map-and-distributed-map
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, step-functions, map-state, inline-map, distributed-map, batch-processing, s3, parallelism]
level: practitioner
status: docs-checked
description: "Fan out work with Step Functions Map: inline vs distributed mode, S3 item readers, batching, concurrency, failure tolerance, result writers and IAM."
sources: ["https://docs.aws.amazon.com/step-functions/latest/dg/state-map-distributed.html", "https://docs.aws.amazon.com/step-functions/latest/dg/input-output-resultwriter.html", "https://docs.aws.amazon.com/step-functions/latest/dg/input-output-itembatcher.html", "https://docs.aws.amazon.com/step-functions/latest/dg/service-quotas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Step Functions Map and Distributed Map

**Goal:** process N items in parallel without blowing the 25,000-event history limit, the
256 KiB payload limit, or downstream rate limits.

## 1. Inline vs distributed
| | Inline Map | Distributed Map |
|---|---|---|
| Items from | an array in state input | state input array **or** a large S3 data source (CSV, JSON and other formats; see ItemReader) |
| Concurrency | meant for up to about 40 concurrent iterations | up to 10,000 child executions (the default when `MaxConcurrency` is omitted or 0) |
| History | iterations count against parent's 25,000 events | each child is its own execution |
| Payload | whole array ≤ 256 KiB | items streamed from S3 |
Rule (from the guide): use Distributed when the dataset exceeds 256 KiB, the history would exceed 25,000 events, or you need more than 40 concurrent iterations. The parent must be a Standard workflow; children can be Standard or Express.

## 2. Distributed Map over a CSV in S3
```json
"ProcessRows": {
  "Type": "Map",
  "ItemReader": {
    "Resource": "arn:aws:states:::s3:getObject",
    "ReaderConfig": {"InputType": "CSV", "CSVHeaderLocation": "FIRST_ROW"},
    "Arguments": {"Bucket": "my-input", "Key": "{% $states.input.key %}"}
  },
  "ItemBatcher": {"MaxItemsPerBatch": 100, "MaxInputBytesPerBatch": 262144},
  "MaxConcurrency": 200,
  "ToleratedFailurePercentage": 2,
  "ItemProcessor": {
    "ProcessorConfig": {"Mode": "DISTRIBUTED", "ExecutionType": "EXPRESS"},
    "StartAt": "Handle",
    "States": {"Handle": {"Type": "Task", "Resource": "arn:aws:states:::lambda:invoke",
      "Arguments": {"FunctionName": "row-handler", "Payload": "{% $states.input %}"},
      "End": true}}
  },
  "ResultWriter": {"Resource": "arn:aws:states:::s3:putObject",
    "Arguments": {"Bucket": "my-results", "Prefix": "runs/"}},
  "Label": "ProcessRows",
  "End": true
}
```
- `ItemBatcher` sends `{"Items": [...]}` per child — fewer child executions; `MaxInputBytesPerBatch` is capped at 256 KiB (262144) and `BatchInput` adds fixed data to each batch.
- `MaxConcurrency` is your throttle for the downstream (DB connections, API rate limits);
  0 means "as high as possible" (10,000), rarely what you want.
- `ToleratedFailurePercentage`/`Count` (default 0 = any failure fails the Map Run) let the map succeed with some failed items; if both are set, exceeding either fails the run with `States.ExceedToleratedFailureThreshold`. Failed items are listed in the `ResultWriter` output (`FAILED_n.json`).
- Without `ResultWriter`, results are returned inline and the map fails with `States.DataLimitExceeded` if they exceed 256 KiB. The result bucket must be in the same account and Region as the state machine.

## 3. IAM the role needs
`states:StartExecution` on the state machine itself (children), `states:DescribeExecution`
on its executions, S3 read access on the input, `s3:PutObject`, `s3:GetObject`, `s3:ListMultipartUploadParts` and `s3:AbortMultipartUpload` on the result prefix, plus whatever the child tasks call.

## 4. Inline Map for small arrays
```json
"Each": {"Type": "Map", "Items": "{% $states.input.lines %}", "MaxConcurrency": 10,
  "ItemProcessor": {"ProcessorConfig": {"Mode": "INLINE"}, "StartAt": "P", "States": {...}}}
```

## Gotchas
- A Map Run is its own resource (`list-map-runs`, `describe-map-run`); unsuccessful child executions can be redriven. Up to 1,000 Map Runs can be open per account and Region.
- Express children are at-least-once: item handlers must be idempotent.
- Changing an inline Map to Distributed changes how errors and outputs surface; retest catchers.

## Verify
- [ ] `describe-map-run` shows a succeeded item count equal to the input row count (minus tolerated failures).
- [ ] Downstream service metrics stay under its rate limit at the configured `MaxConcurrency`.
- [ ] Result files land under the `ResultWriter` prefix: `manifest.json`, `SUCCEEDED_n.json`, `FAILED_n.json` and `PENDING_n.json` (files split at 5 GB).

## Checked
Checked 2026-10-24 against the Step Functions developer guide (Distributed Map state, ResultWriter, ItemBatcher, service quotas).
Confirmed: when to use Distributed, 10,000 child execution default and MaxConcurrency 0 behaviour, ItemBatcher fields and 256 KiB cap, tolerated failure semantics and error name, ResultWriter output files and same-account-Region rule, DataLimitExceeded without ResultWriter, Distributed Map IAM, Express children, Standard-only parent, open Map Run quota.
Corrected: the IAM list no longer includes StopExecution (not in the documented least-privilege policy). Removed as unconfirmed: S3 listing reader claim and itemCounts field name.

Method: documentation only; no commands were run.
