---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dataflow-troubleshooting-with-worker-logs
name: dataflow-troubleshooting-with-worker-logs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataflow, dataflow-troubleshooting, worker-logs, job-logs, stragglers]
level: advanced
status: docs-checked
description: "Debug failing or stuck Dataflow jobs: job vs worker vs startup logs, Logs Explorer filters, common error signatures, stragglers, hot keys, OOMs, and the diagnostics tab."
sources: ["https://cloud.google.com/dataflow/docs/guides/troubleshooting-your-pipeline", "https://cloud.google.com/dataflow/docs/guides/logging", "https://cloud.google.com/dataflow/docs/guides/common-errors", "https://cloud.google.com/dataflow/docs/guides/troubleshoot-oom"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataflow troubleshooting with worker logs

## 1. Which log
| Log | Contains |
|---|---|
| `job-message` | job-level messages: autoscaling configuration, workers starting and stopping, step progress, job errors (worker-level errors from crashing user code propagate here) |
| `worker` | messages logged by your code and Dataflow |
| `worker-startup` | startup process: downloading job jars, starting workers |
| `harness`, `system`, `docker`, `kubelet`, `shuffler` | runner harness, host OS (crashes, OOM), container tooling, shuffle workers |

Logs Explorer:
```
resource.type="dataflow_step"
resource.labels.job_id="<JOB_ID>"
```
Add a `log_id("dataflow.googleapis.com/<TYPE>")` or severity clause to narrow it. If no logs appear, remove exclusion filters on `resource.type="dataflow_step"` from Log Router sinks.

## 2. Error signatures
- **Workers never start**: check `worker-startup` logs; quota, missing `roles/dataflow.worker`, or `--no_use_public_ips` without Private Google Access are typical causes. A single worker repeatedly started and stopped, or "appears to be stuck: no worker activity in the last 1h", points to a networking problem.
- **Python import errors** (for example `ModuleNotFoundError`) in harness logs: see the common-errors page; a custom container (`--sdk_container_image`) avoids dependency installs at startup.
- **"Processing stuck in step X for at least TIME_INTERVAL"** (Java), "Operation ongoing ... Current Traceback" (Python): the DoFn is stuck, deadlocked or slow; expand the log entry for the stack trace.
- **OOM / "Shutting down JVM after 8 consecutive periods of measured GC thrashing"**: avoid hot keys and large per-key state; see the OOM page for reducing SDK processes and threads.
- Batch: a bundle containing a failing item is retried 4 times and then the job fails ("A work item has failed 4 times"); streaming retries indefinitely and can stall (watch system latency and data freshness).

## 3. Stragglers and hot keys
The **Diagnostics** tab of the Logs pane groups errors and shows how often they occur; job execution details show stragglers. A hot key is logged as "A hot key HOT_KEY_NAME was detected"; a pipeline option prints the human-readable key (see the common-errors page for its name). To fix: rekey, `Combine.PerKey.withHotKeyFanout` (Java) or `CombinePerKey.with_hot_key_fanout` (Python), or enable Dataflow Shuffle.

## Gotchas
- Worker log messages are limited to 15,000 per 30 seconds per worker, after which a single throttling message is logged; log a sample, not every element.
- Plain-text lines on stdout have no severity in Logs Explorer; write structured logs to filter by severity.

## Verify
- [ ] Root cause traced to a specific step and log entry; a rerun shows healthy throughput in the step's element counts.

## Checked
2026-10-27. Confirmed against Dataflow logging page (log types, resource.type dataflow_step, Diagnostics tab, throttling limit of 15,000 messages per 30 seconds per worker), common errors page (4 retries in batch, indefinite in streaming, stuck-processing messages, hot-key message and remedies, no-worker-activity message, GC thrashing message), troubleshooting-your-pipeline and troubleshoot-OOM pages. Removed: the 05m00s interval, --requirements_file advice, --number_of_worker_harness_threads for OOM, the hotKeyLoggingEnabled option spelling (page does not give it), Python print and empty-output tips, Execution details tab claim.
Method: documentation only; no commands were run.
