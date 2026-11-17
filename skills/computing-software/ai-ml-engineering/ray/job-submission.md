---
id: computing-software.ai-ml-engineering.ray.job-submission
name: job-submission
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-job-submit, jobsubmissionclient, job-logs, job-stop]
level: practitioner
status: docs-checked
description: "Submit, monitor and stop Ray jobs via ray job submit and JobSubmissionClient against the dashboard address, with runtime environments."
sources:
  - https://docs.ray.io/en/latest/cluster/running-applications/job-submission/quickstart.html
  - https://docs.ray.io/en/latest/cluster/running-applications/job-submission/cli.html
  - https://docs.ray.io/en/latest/cluster/running-applications/job-submission/sdk.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job submission

```bash
export RAY_API_SERVER_ADDRESS="http://head:8265"   # dashboard / job server address (falls back to RAY_ADDRESS)
ray job submit --working-dir ./ --runtime-env-json='{"pip":["pandas"]}' -- python train.py
ray job submit --no-wait --submission-id exp-42 -- python train.py
ray job status exp-42
ray job logs exp-42 --follow
ray job stop exp-42
ray job list
```
Options for `ray job submit` go before the `--`; the entrypoint command goes after it. Without `--no-wait` the command streams logs until the job finishes.

```python
from ray.job_submission import JobSubmissionClient, JobStatus
c = JobSubmissionClient("http://head:8265")
jid = c.submit_job(entrypoint="python train.py", runtime_env={"working_dir": "./"})
print(c.get_job_status(jid), c.get_job_logs(jid))
c.stop_job(jid)
```

## Gotchas
- Install with `pip install "ray[default]"`; Ray Jobs needs the full installation.
- `--working-dir` is downloaded to all nodes of the cluster; it can also be a remote URI to a .zip file.
- The entrypoint runs on the head node by default and reserves 0 CPUs and 0 GPUs. Pass `entrypoint_num_cpus`, `entrypoint_num_gpus`, `entrypoint_memory` or `entrypoint_resources` (CLI: `--entrypoint-*`) to schedule it on a node with those resources. These are logical resources for scheduling only.
- Do heavy computation in Ray tasks, actors or libraries, not at the top level of the entrypoint.
- The dashboard port (8265 by default) must be reachable: port-forward it, or use `ray dashboard` on a cluster started with the cluster launcher.
- A job id passed as submission id must be unique per cluster, or submission errors.
- Job information stays on the cluster indefinitely; call `client.delete_job(job_id)` on jobs in a terminal state to remove it.
- Terminal states are SUCCEEDED, STOPPED and FAILED.

## Verify
`ray job status exp-42` ends in `SUCCEEDED` and logs show your script output.

## Checked

Method: docs-checked 2026-11-09 against docs.ray.io job-submission quickstart, CLI reference and Python SDK overview (downloaded and read); removed the metadata kwarg, upload size and excludes claim, the disconnect remark and the unconfirmed auth remark
