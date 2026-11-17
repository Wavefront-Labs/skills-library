---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gpu-jobs-on-cloud-batch
name: gpu-jobs-on-cloud-batch
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-batch, batch-gpu-jobs, install-gpu-drivers, accelerators, gpu-containers]
level: practitioner
status: docs-checked
description: "Run GPU workloads on Cloud Batch: accelerator policy with installGpuDrivers, container GPU options, Spot GPUs, quota and zone selection, and verifying the GPU inside tasks."
sources: ["https://cloud.google.com/batch/docs/create-run-job-gpus", "https://cloud.google.com/batch/docs/reference/rest/v1/projects.locations.jobs#accelerator", "https://cloud.google.com/compute/docs/gpus/gpu-regions-zones"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU jobs on Cloud Batch

## Job spec (container)
```json
{
  "taskGroups": [{
    "taskCount": 20, "parallelism": 4,
    "taskSpec": {
      "runnables": [{"container": {
        "imageUri": "us-docker.pkg.dev/<P>/ml/infer:2.1",
        "commands": ["python", "infer.py", "--shard", "${BATCH_TASK_INDEX}"]
      }}],
      "computeResource": {"cpuMilli": 8000, "memoryMib": 30000},
      "maxRetryCount": 2, "maxRunDuration": "7200s"
    }
  }],
  "allocationPolicy": {
    "location": {"allowedLocations": ["regions/us-central1"]},
    "instances": [{
      "installGpuDrivers": true,
      "policy": {
        "machineType": "g2-standard-8",
        "provisioningModel": "SPOT"
      }
    }]
  },
  "logsPolicy": {"destination": "CLOUD_LOGGING"}
}
```
```bash
gcloud batch jobs submit infer-oct --location=us-central1 --config=job.json
```
- `installGpuDrivers: true` (set on `instances[]`, not inside `accelerators`) lets Batch fetch and install the NVIDIA driver; set `driverVersion` to pin a version. This is the recommended method when you do not need to install drivers manually.
- To install drivers yourself, use a custom image through an instance template (`instances[].instanceTemplate`) and leave `installGpuDrivers` false (the default).
- For accelerator-optimized machine types (A2, A3, G2) the machine type determines the GPU, so set only `machineType`; the `accelerators` field (`type`, `count`) is for GPUs attached to N1 VMs.

## Capacity
- Check GPU quota for the region before submitting; a job that lacks quota is delayed and reports it in `statusEvents`.
- `allowedLocations` can list several regions or zones.
- Spot tasks can be preempted (exit code 50001): keep `maxRetryCount` above 0 (maximum 10) and tasks idempotent.

## Verify
- [ ] A one-task test that prints the visible GPUs shows the expected model in Cloud Logging.
- [ ] `gcloud batch jobs describe infer-oct --location=us-central1 --format='value(status.state)'` = SUCCEEDED.

## Checked
2026-10-27. Confirmed against the Batch Create and run a job that uses GPUs page (installGpuDrivers recommended and driverVersion, custom image through instanceTemplate, accelerators only for N1 VMs, STANDARD or SPOT provisioning models) and the Batch discovery document (InstancePolicyOrTemplate.installGpuDrivers; Accelerator.installGpuDrivers deprecated; Accelerator.type and count). Removed: --gpus all container option, boot-time claim, bootDisk.image advice, GPU quota metric names, zone-obtainability claim. Corrected: the example set accelerators on a G2 machine type, but accelerators apply to N1 VMs only.
Method: documentation only; no commands were run.
