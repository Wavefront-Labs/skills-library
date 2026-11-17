---
id: computing-software.cloud-infrastructure-engineering.aws.aws-batch-and-hpc
name: aws-batch-and-hpc
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-batch, batch, hpc, parallelcluster, compute-environment, job-queue, job-definition, array-job, job-dependencies, fargate-batch, spot-batch, efa, fsx-lustre, slurm, placement-group, hpc-instances, retry-strategy, multi-node-parallel, fair-share-scheduling]
level: advanced
status: gated
description: "Run batch and HPC workloads: AWS Batch compute environments, queues, job definitions, array jobs, Spot retries; ParallelCluster with Slurm, EFA and FSx for Lustre."
sources: ["https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html", "https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html", "https://docs.aws.amazon.com/batch/latest/userguide/array_jobs.html", "https://docs.aws.amazon.com/batch/latest/userguide/job_retries.html", "https://docs.aws.amazon.com/parallelcluster/latest/ug/what-is-aws-parallelcluster.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html", "https://docs.aws.amazon.com/batch/latest/userguide/fair-share-scheduling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Batch and HPC workloads

**Goal:** choose correctly between AWS Batch (embarrassingly parallel container jobs,
pay only while running) and ParallelCluster (Slurm cluster for MPI/tightly coupled
simulation), and configure either so Spot interruptions, retries and storage do not
silently eat results.

## 1. Decide
| Workload | Use |
|---|---|
| Many independent container jobs (ETL, rendering, genomics per-sample, ML inference) | **AWS Batch** |
| Jobs need shared scratch at > 1 GB/s or hundreds of GB | Batch + **FSx for Lustre** volume, or ParallelCluster |
| MPI / tightly coupled, low-latency interconnect, researchers want `sbatch` | **ParallelCluster** (Slurm) with EFA |
| A handful of long GPU training runs | SageMaker training jobs or Batch with GPU job definitions |

## 2. AWS Batch: three objects
```bash
# Compute environment: managed, Spot, diversified, scales to zero
aws batch create-compute-environment --compute-environment-name spot-ce --type MANAGED \
  --compute-resources '{"type":"SPOT","allocationStrategy":"SPOT_PRICE_CAPACITY_OPTIMIZED",
    "minvCpus":0,"maxvCpus":2000,"instanceTypes":["c6i","c6a","c7i","m6i","m6a"],
    "subnets":["subnet-a","subnet-b","subnet-c"],"securityGroupIds":["sg-batch"],
    "instanceRole":"ecsInstanceRole","ec2Configuration":[{"imageType":"ECS_AL2023"}]}' \
  --service-role AWSServiceRoleForBatch
# Queue: On-Demand CE first for the base, Spot CE second
aws batch create-job-queue --job-queue-name main --priority 10 \
  --compute-environment-order order=1,computeEnvironment=ondemand-ce order=2,computeEnvironment=spot-ce
# Job definition
aws batch register-job-definition --job-definition-name process --type container \
  --container-properties '{"image":"<ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/process:1.4",
    "resourceRequirements":[{"type":"VCPU","value":"4"},{"type":"MEMORY","value":"16384"}],
    "jobRoleArn":"arn:aws:iam::<ACCOUNT_ID>:role/batch-job","executionRoleArn":"arn:aws:iam::<ACCOUNT_ID>:role/ecsTaskExecutionRole",
    "logConfiguration":{"logDriver":"awslogs"}}' \
  --retry-strategy '{"attempts":3,"evaluateOnExit":[{"onStatusReason":"Host EC2*","action":"RETRY"},{"onReason":"*","action":"EXIT"}]}' \
  --timeout attemptDurationSeconds=7200
aws batch submit-job --job-name run-2026-10 --job-queue main --job-definition process \
  --array-properties size=5000 --container-overrides 'environment=[{name=INPUT_PREFIX,value=s3://bucket/in/}]'
```
- **Allocation strategy**: `SPOT_PRICE_CAPACITY_OPTIMIZED` for Spot, `BEST_FIT_PROGRESSIVE`
  for On-Demand. `BEST_FIT` (legacy) cannot scale past a single pool and gets stuck.
- Use instance *families* (`c6i`) not sizes so Batch packs jobs onto the best size.
- `minvCpus: 0` scales to zero; `desiredvCpus` is managed — do not set it.
- **Array jobs** (`size` up to 10,000): each child gets `AWS_BATCH_JOB_ARRAY_INDEX`; map it to
  an input shard. Dependencies: `--depends-on jobId=<parent>,type=N_TO_N` for element-wise
  chaining, or `SEQUENTIAL` within an array.
- `evaluateOnExit` with `onStatusReason: "Host EC2*"` retries Spot reclamation but not
  application failures — the single most valuable line in the definition.
- Fargate compute environments (`type: FARGATE`/`FARGATE_SPOT`) skip instance
  management; per-job size limits apply, and Fargate has no GPUs or EFA (gated: unconfirmed, source is paywalled or blocked); fine for small, bursty jobs.
- GPU: `resourceRequirements` `{"type":"GPU","value":"1"}` on `g`/`p` families with
  `ECS_AL2023_NVIDIA` image type.
- Fair-share scheduling (`schedulingPolicyArn` on the queue, `shareIdentifier` on jobs)
  stops one team's 10,000-job array starving everyone else.

## 3. Storage patterns for Batch
- Inputs/outputs in S3; stage with the CLI inside the container (`aws s3 cp` honours
  multipart). Container root is ephemeral and small — mount instance store or an EBS
  volume via launch template for scratch.
- Shared scratch: **FSx for Lustre** linked to the S3 bucket (`DataRepositoryAssociation`)
  mounted via launch template user data on the CE; jobs read S3 objects as files
  lazily and `lfs hsm_archive` or auto-export writes results back.
- EFS works for small shared config/results, not for high-throughput scratch.

## 4. ParallelCluster for HPC
```bash
pip install aws-parallelcluster
pcluster configure --config cluster.yaml   # wizard; or write YAML directly
pcluster create-cluster -n sim -c cluster.yaml
pcluster ssh -n sim -i ~/.ssh/key.pem
```
Key YAML decisions:
```yaml
HeadNode: {InstanceType: c6i.xlarge, Networking: {SubnetId: subnet-pub}, Ssh: {KeyName: key}}
Scheduling:
  Scheduler: slurm
  SlurmQueues:
    - Name: compute
      CapacityType: SPOT          # or ONDEMAND for MPI runs that cannot checkpoint
      Networking: {SubnetIds: [subnet-priv], PlacementGroup: {Enabled: true}}
      ComputeResources:
        - {Name: hpc7a, InstanceType: hpc7a.96xlarge, MinCount: 0, MaxCount: 64, Efa: {Enabled: true}}
SharedStorage:
  - {MountDir: /fsx, Name: scratch, StorageType: FsxLustre,
     FsxLustreSettings: {StorageCapacity: 4800, DeploymentType: SCRATCH_2, ImportPath: s3://bucket/in, ExportPath: s3://bucket/out}}
```
- **EFA** (Elastic Fabric Adapter) gives OS-bypass MPI; only on supported types
  (`hpc7a`, `hpc6id`, `c6gn`, `p4d/p5`…), and all ranks must be in one **cluster
  placement group** in one AZ. ParallelCluster installs the EFA driver, Open MPI/
  Intel MPI and libfabric; `fi_info -p efa` on a node confirms it.
- HPC instance families (`hpc7a`, `hpc7g`, `hpc6id`) have no Spot, are On-Demand only
  and **only in a few regions**; check availability before designing around them.
- Slurm scales compute nodes from `MinCount` to `MaxCount` on demand (`sinfo` shows
  `idle~` for not-yet-launched). Set `ScaledownIdletime` (see the ParallelCluster docs for the default) to balance cost vs cold start.
- Head node is a single point of failure and holds `/home` by default; put `/home`
  on EFS and keep the head node small — it only schedules.
- Updates: most queue changes need `pcluster update-compute-fleet --status STOP_REQUESTED`
  then `pcluster update-cluster`; head-node type changes require stop/start.

## Gotchas
- Batch job stuck in `RUNNABLE`: CE cannot launch (quota, subnet without route to ECR/S3,
  instance role missing, job asks more memory than any allowed type provides). Check CE
  `statusReason` and the ASG/EC2 Fleet activity. Memory is strict: ECS reserves some, so
  a job asking for all of an instance's memory will not fit — leave headroom or use the next size.
- Spot interrupted jobs count as failed attempts; without `evaluateOnExit` they exit.
- `awslogs` driver is required to see stdout; the default `ecsInstanceRole` can write it.
- Container images > a few GB make every new instance slow to start — keep them lean
  or bake into a custom ECS AMI via launch template.
- ParallelCluster API/CLI version must match the cluster's version for updates.
- Unconfirmed: current maximum `maxvCpus` and array size limits; check quotas.

## Verify
- [ ] Submitting an array of 100 jobs scales the CE from 0 and back to 0 within `ScaledownIdletime` after completion.
- [ ] Forced Spot interruption (FIS) retries affected children; `describe-jobs` shows `attempts` > 1 with `Host EC2` reason, final `SUCCEEDED`.
- [ ] No job in `RUNNABLE` longer than expected launch time; CE status `VALID`.
- [ ] ParallelCluster: `srun -N2 --mpi=pmix fi_info -p efa` succeeds on both nodes; OSU latency benchmark shows single-digit microseconds.
- [ ] Results appear in the S3 export path after the job (`lfs hsm_state` / data repository task status `SUCCEEDED`).

## Checked

Date: 2026-11-02. Confirmed on AWS Batch User Guide (what is Batch, compute environments, array jobs, job retries, fair-share scheduling) and ParallelCluster/EFA pages: component roles, array jobs, retries, queue types. Removed as not stated there: the 16 vCPU / 120 GB Fargate cap, the 10-minute idle-scaledown default, the 10% memory headroom figure. Left, marked gated: Fargate no-GPU/no-EFA limits.

Method: documentation only; no commands were run.
