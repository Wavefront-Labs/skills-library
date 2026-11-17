---
id: computing-software.cloud-infrastructure-engineering.aws.aws-batch-jobs-stuck-in-runnable
name: aws-batch-jobs-stuck-in-runnable
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-batch, runnable-stuck, batch-troubleshooting, compute-environment-invalid, job-queue-blocked, ecs]
level: practitioner
status: docs-checked
description: "Unstick AWS Batch jobs left in RUNNABLE: statusReason values, resource requests vs instance types, maxvCpus, INVALID compute environments, networking, quotas, time limits."
sources: ["https://docs.aws.amazon.com/batch/latest/userguide/job_stuck_in_runnable.html", "https://docs.aws.amazon.com/batch/latest/userguide/job_stuck_in_runnable_capacity.html", "https://docs.aws.amazon.com/batch/latest/userguide/job_stuck_in_runnable_misconfiguration.html", "https://docs.aws.amazon.com/batch/latest/userguide/job_stuck_in_runnable_time_limit_actions.html", "https://docs.aws.amazon.com/batch/latest/userguide/job_stuck_in_runnable_common_causes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Batch jobs stuck in RUNNABLE

RUNNABLE means the job is ready but no capacity in the queue's compute environments can
run it yet. Check in this order.

## 1. Read the statusReason
`aws batch describe-jobs --jobs <id> --query 'jobs[].statusReason'` often names the cause:
- `CAPACITY:INSUFFICIENT_INSTANCE_CAPACITY`: every connected compute environment hit
  insufficient-capacity errors. Detection needs the Batch service role to have
  `autoscaling:DescribeScalingActivities` and `ec2:DescribeSpotFleetRequestHistory`; the same
  permissions are needed for time limit cancellations to run.
- `MISCONFIGURATION:COMPUTE_ENVIRONMENT_MAX_RESOURCE`: every compute environment has a
  `maxvCpus` smaller than the job needs. Raise `maxvCpus` or cancel the job.
- `MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT`: the job's vCPU/memory/GPU request is higher
  than any attached compute environment can meet. Widen the allowed instance types or cancel.
- `MISCONFIGURATION:EC2_INSTANCE_CONFIGURATION_UNSUPPORTED`: instance types not available in
  the chosen AZs, or launch template settings incompatible with them.
- `MISCONFIGURATION:SERVICE_ROLE_PERMISSIONS`: fix the Batch service role by hand (prefer the
  service-linked role).
- No reason at all: see section 4.

## 2. Compute environment status
```bash
aws batch describe-compute-environments \
  --query 'computeEnvironments[].{n:computeEnvironmentName,state:state,status:status,reason:statusReason,max:computeResources.maxvCpus,desired:computeResources.desiredvCpus}'
```
- `status` is one of `CREATING`, `UPDATING`, `DELETING`, `DELETED`, `VALID`, `INVALID`. For
  `INVALID`, read `statusReason`, fix the cause and call `update-compute-environment`.
- `state: DISABLED`: enable it.
- `desiredvCpus` stays 0 while jobs wait: Batch cannot find an instance type that fits.
- Check the job's needs: `aws batch describe-jobs --jobs <id> --query 'jobs[].container.resourceRequirements'`.
- `allocationStrategy` for Spot can be `SPOT_PRICE_CAPACITY_OPTIMIZED` (also
  `SPOT_CAPACITY_OPTIMIZED`, `BEST_FIT_PROGRESSIVE` and others); more instance types and AZs
  give Spot more pools.

## 3. Resources vs instance types
- If job definitions ask for more CPU or memory than the compute resources can allocate, the
  job is never placed. Some memory is reserved for the Amazon ECS container agent and other
  system processes, so a job cannot claim an instance's full memory.
- GPU jobs need GPU instance types in the compute environment.

## 4. Instances launch but jobs still RUNNABLE (often no statusReason)
Common causes listed by AWS:
- The `awslogs` log driver is not available on a custom AMI (needs `ECS_AVAILABLE_LOGGING_DRIVERS`
  to include it; the ECS optimized AMI registers it by default).
- Compute resources cannot reach the Amazon ECS endpoint: use an interface VPC endpoint,
  public IP addresses, or NAT.
- The EC2 instance quota (account-wide, plus per-instance-type quotas) is reached.
- The Amazon ECS container agent is not installed on the AMI.
- A long-running user data script in the launch template makes instances time out before they
  register with Amazon ECS.

## 5. Blocked queues: cancel automatically
A job at the head of a queue that cannot run blocks the ones behind it. `jobStateTimeLimitActions`
(on `CreateJobQueue` / `UpdateJobQueue`) cancels a RUNNABLE job after `maxTimeSeconds` when its
`statusReason` matches. For queues on ECS, EKS or Fargate compute environments the only action
is cancel. Supported reasons: `CAPACITY:INSUFFICIENT_INSTANCE_CAPACITY`,
`MISCONFIGURATION:COMPUTE_ENVIRONMENT_MAX_RESOURCE`, `MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT`.
Not supported (investigate by hand): `MISCONFIGURATION:SERVICE_ROLE_PERMISSIONS`,
`ACTION_REQUIRED`, `UNDETERMINED`.
```bash
aws batch update-job-queue --job-queue q --job-state-time-limit-actions \
  'reason=MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT,state=RUNNABLE,maxTimeSeconds=600,action=CANCEL'
```

## Verify
- [ ] CE `VALID`/`ENABLED`, `desiredvCpus` rises when jobs are queued.
- [ ] Instances register with the ECS cluster Batch created.
- [ ] A test job with modest resources goes RUNNABLE to STARTING to RUNNING within minutes.
- [ ] Job state time limit actions configured on each queue.

## Checked
2026-10-31. Confirmed against the AWS Batch User Guide pages on jobs stuck in RUNNABLE (capacity, misconfiguration, automatic remediation, common causes) and the botocore Batch model (`UpdateJobQueue` `jobStateTimeLimitActions` members and enums, compute environment `status` values, `allocationStrategy` enum, `maxvCpus`, `desiredvCpus`). Removed as unconfirmed: the 16384 MiB / 15,000 MiB memory example, the list of VPC endpoint names, the instance role policy name, the `agentConnected` check, the ECS cluster naming pattern, the MIME multipart note, arm64 behaviour and Fargate subnet details.
Method: documentation only; no commands were run.
