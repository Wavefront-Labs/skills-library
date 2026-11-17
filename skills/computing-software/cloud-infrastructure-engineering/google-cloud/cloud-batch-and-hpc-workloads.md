---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-batch-and-hpc-workloads
name: cloud-batch-and-hpc-workloads
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-batch, batch, hpc, slurm, cluster-toolkit, hpc-toolkit, task-arrays, batch-jobs, compact-placement, placement-policy, h3, c3, gpu-batch, spot-batch, parallelstore, lustre, job-arrays, retries, task-parallelism]
level: practitioner
status: docs-checked
description: "Run batch and HPC on GCP: Cloud Batch job specs with task arrays, retries, Spot and GPUs; Slurm clusters via Cluster Toolkit with compact placement and parallel filesystems."
sources: ["https://cloud.google.com/batch/docs/get-started", "https://cloud.google.com/batch/docs/create-run-basic-job", "https://cloud.google.com/batch/docs/automate-task-retries", "https://cloud.google.com/cluster-toolkit/docs/overview", "https://cloud.google.com/compute/docs/instances/use-compact-placement-policies", "https://cloud.google.com/parallelstore/docs/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Batch and HPC workloads

**Goal:** thousands of embarrassingly-parallel tasks or a tightly-coupled MPI job run on
exactly the hardware they need, on Spot VMs where tolerable, and clean up after themselves.

## 1. Cloud Batch: managed job runner
```json
{
  "taskGroups": [{
    "taskCount": 1000, "parallelism": 200,
    "taskSpec": {
      "runnables": [{"container": {"imageUri": "europe-docker.pkg.dev/<P>/img/render:1.4",
                                   "commands": ["--frame", "${BATCH_TASK_INDEX}"]}}],
      "computeResource": {"cpuMilli": 4000, "memoryMib": 16384},
      "maxRetryCount": 2, "maxRunDuration": "3600s",
      "volumes": [{"gcs": {"remotePath": "render-assets"}, "mountPath": "/mnt/assets"}]
    }
  }],
  "allocationPolicy": {
    "instances": [{"policy": {"machineType": "c3-standard-8", "provisioningModel": "SPOT"}}],
    "location": {"allowedLocations": ["regions/europe-west4"]},
    "serviceAccount": {"email": "batch-runner@<P>.iam.gserviceaccount.com"},
    "network": {"networkInterfaces": [{"network": "projects/<P>/global/networks/prod", "subnetwork": "regions/europe-west4/subnetworks/batch", "noExternalIpAddress": true}]}
  },
  "logsPolicy": {"destination": "CLOUD_LOGGING"}
}
```
`gcloud batch jobs submit render-$(date +%s) --location=europe-west4 --config=job.json`.
- `BATCH_TASK_INDEX` / `BATCH_TASK_COUNT` env vars shard the work; `parallelism` bounds concurrent VMs (and quota).
- Runnables can be containers or scripts, run in sequence per task; a `barrier` runnable blocks later runnables until all tasks reach it; `taskEnvironments` injects per-task env (`taskCount` must equal its length, maximum 200).
- **Retries:** `maxRetryCount` (0-10) plus one `lifecyclePolicies` entry (`actionCondition.exitCodes` with `RETRY_TASK` or `FAIL_TASK`); Spot preemption is exit code 50001. A non-zero exit that matches no policy is retried up to `maxRetryCount`.
- GPUs: on accelerator-optimized machine types (A2, A3, G2) set only `machineType`; for N1 VMs use `"accelerators": [{"type": "<GPU_TYPE>", "count": 1}]`. Set `installGpuDrivers: true` on `instances[]` to let Batch install drivers.
- Volumes: Cloud Storage buckets, NFS (such as Filestore), persistent disks and local SSDs are supported.
- The runner SA needs `roles/batch.agentReporter` and `roles/logging.logWriter`; you need `roles/batch.jobsEditor` and `roles/iam.serviceAccountUser` on it.

## 2. Slurm with Cluster Toolkit (tightly-coupled HPC)
Cluster Toolkit is an open-source tool for deploying HPC, AI and ML clusters from blueprints. A **blueprint** is a YAML file that selects **modules** (schedulers, storage, compute nodes) and configures them; the `gcluster` tool compiles it into a deployment folder of Terraform and Packer configuration. Example blueprints live in the Cluster Toolkit repository.
- Workflow: `gcluster create <blueprint>.yaml` generates the deployment folder, then run the commands `gcluster` prints so Terraform or Packer deploys the cluster.
- It integrates with partners including Slurm, Intel DAOS and DDN EXAScaler, and with Cloud Monitoring.
- **Compact placement policies** place instances physically closer together to reduce network latency for HPC and ML workloads. Some A3, A4 and H4D machine types use workload policies instead in MIGs; see the compact placement page for the machine types and maximum distance values that apply.
- Storage: Filestore (NFS), Managed Lustre (a fully managed parallel file system for AI and HPC) or Cloud Storage; check each product's page for capacity and throughput.

## 3. Choosing
| Need | Pick |
|---|---|
| independent tasks, containers, "fire and forget" | Cloud Batch |
| MPI/tightly-coupled, researchers who know Slurm | Cluster Toolkit (Slurm blueprints) |
| Kubernetes-native batch (Kueue, JobSet), mixed with services | GKE with Kueue |
| ad-hoc Spark/Hadoop | Dataproc (see `dataproc-clusters-and-serverless-spark`) |

## Gotchas
- `allowedLocations` lists the regions or zones a job may use.
- Batch VMs use the project's default network if you omit `network`. If the `compute.vmExternalIpAccess` constraint applies or your network uses Private Google Access, block external access for the job's VMs and provide Cloud NAT or Private Google Access.
- Jobs can be delayed or fail on quota: the `statusEvents` field names the quota (see `quotas-and-quota-management`).

## Verify
- [ ] `gcloud batch jobs describe` reaches `SUCCEEDED` with all tasks succeeded.
- [ ] Task stdout and stderr appear in Cloud Logging under `batch_task_logs`.
- [ ] Cluster Toolkit: `gcluster create` produces a deployment folder and the cluster deploys from it.

## Checked
2026-10-27. Confirmed against the Batch get-started, basic-job, troubleshooting, GPU and retry pages and the Batch discovery document (job fields, retries, GPUs, roles), the Cluster Toolkit overview (blueprints, modules, gcluster, Terraform and Packer deployment folder, partners), the compact placement page and the Managed Lustre overview (the parallelstore URL now serves Managed Lustre). Removed: the Slurm blueprint with module ids and settings, H3/C3/A3 and tier_1 bandwidth statements, Parallelstore/DAOS capacity claims, compact-placement restrictions and stockout message, Artifact Registry reader claim, Slurm image and Packer advice, nodes-appear-within-minutes and latency verify steps. The job-and-task-retries page returned 404 and was replaced by the automate-task-retries page in sources.
Method: documentation only; no commands were run.
