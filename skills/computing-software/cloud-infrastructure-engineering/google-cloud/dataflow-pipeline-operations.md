---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dataflow-pipeline-operations
name: dataflow-pipeline-operations
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataflow, apache-beam, streaming-engine, dataflow-prime, flex-templates, classic-templates, dataflow-autoscaling, worker-service-account, dataflow-networking, update-pipeline, drain, cancel, dataflow-snapshots, streaming-pipelines, batch-pipelines, job-monitoring, data-freshness, system-lag, fusion]
level: practitioner
status: gated
description: "Operate Dataflow pipelines: launch from Flex Templates, worker SA and private networking, autoscaling, Streaming Engine, update vs drain vs cancel, snapshots, lag metrics."
sources: ["https://cloud.google.com/dataflow/docs/overview", "https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates", "https://cloud.google.com/dataflow/docs/guides/specifying-networks", "https://cloud.google.com/dataflow/docs/guides/updating-a-pipeline", "https://cloud.google.com/dataflow/docs/guides/stopping-a-pipeline", "https://cloud.google.com/dataflow/docs/guides/using-monitoring-intf", "https://cloud.google.com/dataflow/docs/guides/troubleshooting-your-pipeline"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataflow pipeline operations

**Goal:** Beam pipelines that launch from a versioned template inside the private network,
scale on their own, can be upgraded without losing in-flight data, and page you on lag rather than on angry users.

## 1. Launch the right way
- **Flex Templates**: pipeline packaged as a container in Artifact Registry + a JSON spec in GCS; launch with `gcloud dataflow flex-template run`. Classic templates are frozen graphs and cannot take runtime-only options — use Flex for anything new.
```bash
gcloud dataflow flex-template run orders-stream-$(date +%s) --region=europe-west1 \
  --template-file-gcs-location=gs://<P>-templates/orders-stream/v42.json \
  --service-account-email=df-orders@<P>.iam.gserviceaccount.com \
  --subnetwork=regions/europe-west1/subnetworks/dataflow --disable-public-ips \
  --temp-location=gs://<P>-df-temp/orders --staging-location=gs://<P>-df-staging/orders \
  --enable-streaming-engine --max-workers=20 --worker-machine-type=n2-standard-4 \
  --parameters=inputSubscription=projects/<P>/subscriptions/orders-df,outputTable=<P>:analytics.orders
```
Add `--dataflow-service-options=enable_prime` for Dataflow Prime.
- **Worker service account**: `roles/dataflow.worker` + the data roles (Pub/Sub subscriber, BigQuery dataEditor, storage on temp/staging buckets). The *launcher* needs `roles/dataflow.admin` + `iam.serviceAccountUser` on the worker SA.
- **Networking**: `--disable-public-ips` + subnet with Private Google Access (workers must reach `dataflow.googleapis.com`, GCS, and the Streaming Engine); Shared VPC subnet needs `compute.networkUser` for the Dataflow service agent and worker SA. Firewall: allow tcp:12345-12346 between workers (shuffle) for non-Streaming-Engine jobs.
- Pin `--worker-region`/`--region` and use `--kms-key-name` for CMEK on worker disks and state.

## 2. Scaling and cost
- **Streaming Engine** (streaming) / **Dataflow Shuffle** (batch) move state/shuffle off workers → smaller VMs, faster autoscaling; always on for new jobs.
- **Horizontal autoscaling**: `--max-workers` caps cost; streaming scales on backlog + CPU; batch on remaining work. **Dataflow Prime** adds vertical autoscaling (memory) and right-fitting per stage (`--dataflow-service-options=enable_prime`).
- Batch: `--flexrs-goal=COST_OPTIMIZED` (FlexRS) runs on Spot-like capacity with delayed start (up to 6 h) for non-urgent jobs.
- Each worker bills vCPU/mem/PD per second plus Streaming Engine data processed; `--number-of-worker-harness-threads` and fusion matter for CPU-bound Python.

## 3. Change a running streaming job
| Action | Effect | Use |
|---|---|---|
| **Update** (`--update --job-name=<same>` or `gcloud dataflow jobs update-options`) | replaces the job in place, preserves state and buffered data; transforms are mapped by name (`--transform-name-mapping` if renamed) | code/config change that keeps compatible graph |
| **Drain** (`gcloud dataflow jobs drain`) | stops reading new input, finishes in-flight windows/bundles, then ends | safe stop; incompatible update = drain + launch new |
| **Cancel** | stops immediately; buffered data lost (at-least-once sources will redeliver) | emergencies |
| **Snapshot** (`jobs snapshot --snapshot-sources`) | saves state (+ Pub/Sub source positions) to restart a new job from it | long-running jobs with big state before risky updates |
Updates fail with "incompatible" when windowing/coders/state change; the error names the transform. Drain can take as long as the longest window; `--drain` with session windows of hours is a plan, not a click.

## 4. Watch
- **Job metrics** tab / Cloud Monitoring: `job/data_watermark_age` and **system lag** (`job/system_lag`) — rising lag = cannot keep up or stuck; `job/backlog_elements`/`backlog_bytes` (Streaming Engine); `job/current_num_vcpus` for cost; `job/elements_produced_count` per step; **data freshness** on the console.
- Alert: data freshness > N min for streaming; job state `FAILED` (`--format` on `gcloud dataflow jobs list --status=active`). Pipeline logs land in `dataflow.googleapis.com/worker` (gated: unconfirmed, source is paywalled or blocked) with `step` labels; use `Error Reporting` for exceptions.
- Hot keys show as one worker saturated and the step's execution details showing uneven work; fix with `Reshuffle`/sharded keys or `--experiments=enable_hot_key_logging` (gated: unconfirmed, source is paywalled or blocked).
- Stuck "Processing stuck in step … for at least 05m00s" messages are the classic sign of an external call hanging; set timeouts in `DoFn`s.

## 5. Templates as code
Build in CI: `gcloud dataflow flex-template build gs://<P>-templates/orders-stream/<GIT_SHA>.json --image-gcr-path=europe-docker.pkg.dev/<P>/df/orders-stream:<GIT_SHA> --sdk-language=PYTHON --flex-template-base-image=PYTHON3 --py-path=. --env=FLEX_TEMPLATE_PYTHON_PY_FILE=main.py --metadata-file=metadata.json`. Pin the Beam SDK version; Dataflow deprecates old SDKs on a schedule (job launch fails with "SDK version unsupported").

## Gotchas
- Default worker SA = Compute default SA with Editor; set `--service-account-email` always.
- Without Private Google Access on the subnet, workers start then die with "Workers failed to connect to the service" after ~1 h of billing.
- `temp-location` and `staging-location` buckets accumulate files; add a lifecycle rule to delete after 7 days.
- Python pipelines pull dependencies at worker start unless baked into the Flex image (`requirements.txt` → slow scale-up); bake them.
- Regional endpoint ≠ worker zone; `--region` must be a Dataflow regional endpoint (not every region has one — check the list).

## Verify
- [ ] Job runs with `--disable-public-ips` and workers have no external IP (`gcloud compute instances list --filter=labels.dataflow_job_id`).
- [ ] Publishing 10× normal load raises `backlog_bytes` then worker count scales toward `--max-workers`, and freshness recovers.
- [ ] `--update` with a trivial code change keeps the same job name and no messages are lost (count in sink = count published).
- [ ] Drain on a test job completes with sink totals equal to source totals; freshness alert fires in a test when the job is paused.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: the 'GBs per job' claim. Gated: the Cloud Logging log name dataflow.googleapis.com/worker and the enable_hot_key_logging experiment were not found in the fetched pages.

Method: documentation only; no commands were run.
