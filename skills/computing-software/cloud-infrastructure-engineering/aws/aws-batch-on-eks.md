---
id: computing-software.cloud-infrastructure-engineering.aws.aws-batch-on-eks
name: aws-batch-on-eks
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, batch, eks, kubernetes, compute-environment, job-queue, job-definition, access-entries]
level: advanced
status: docs-checked
description: "Run AWS Batch jobs as pods on an existing EKS cluster: namespace, access entries, EKS compute environment, job queue, eksProperties job definition and the RUNNABLE trap."
sources: ["https://docs.aws.amazon.com/batch/latest/userguide/eks.html", "https://docs.aws.amazon.com/batch/latest/userguide/getting-started-eks.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Batch on EKS

Batch keeps queueing, dependency tracking, managed retries, priorities and node scaling; EKS runs the pods on nodes Batch
manages. Batch works as an "overlay": there are no Kubernetes operators or custom resources to install, only RBAC
configuration on the cluster. Batch does not create or administer your EKS cluster.

## 1. Cluster preparation (access entries)
The getting-started tutorial uses EKS access entries, which it calls recommended; they are required when the cluster's
`authenticationMode` is `API` and available with `API_AND_CONFIG_MAP`. A `CONFIG_MAP` cluster should move to
`API_AND_CONFIG_MAP`, or follow the page's separate ConfigMap tutorial.
1. Create a dedicated Kubernetes namespace (recommended by the page) for Batch pods.
2. The node instance role named in `computeResources.instanceRole` needs its own cluster access, separate from Batch's
   access entry. If `aws eks describe-access-entry` for that role returns `ResourceNotFoundException`, create one:
```bash
aws eks create-access-entry --cluster-name <CLUSTER> \
  --principal-arn arn:aws:iam::<ACCOUNT_ID>:role/<NODE_INSTANCE_ROLE> --type EC2_LINUX
```
   Skip it if the role already has an access entry, or (on `API_AND_CONFIG_MAP`) is already mapped in `aws-auth`.
   Without cluster access for this role, instances cannot join and jobs stay RUNNABLE.
3. The user calling `CreateComputeEnvironment` needs `eks:DescribeCluster` and, with access entries,
   `eks:DescribeAccessEntry`, `eks:CreateAccessEntry`, `eks:AssociateAccessPolicy` and `eks:DeleteAccessEntry`.

## 2. Compute environment and queue
`accessEntry.desiredState: ENABLED` makes Batch create an access entry for the `AWSServiceRoleForBatch` service-linked role.
```bash
aws batch create-compute-environment --cli-input-json file://./ce.json
```
```json
{"computeEnvironmentName": "my-eks-ce", "type": "MANAGED", "state": "ENABLED",
 "eksConfiguration": {"eksClusterArn": "arn:aws:eks:<REGION>:<ACCOUNT_ID>:cluster/<CLUSTER>",
   "kubernetesNamespace": "<NAMESPACE>", "accessEntry": {"desiredState": "ENABLED"}},
 "computeResources": {"type": "EC2", "allocationStrategy": "BEST_FIT_PROGRESSIVE", "minvCpus": 0, "maxvCpus": 128,
   "instanceTypes": ["m5"], "subnets": ["<SUBNET_ID>"], "securityGroupIds": ["<SG_ID>"],
   "instanceRole": "<NODE_INSTANCE_PROFILE_ARN>"}}
```
Then wait for `aws batch describe-compute-environments --compute-environments my-eks-ce --query
'computeEnvironments[0].eksConfiguration.accessEntry.status'` to read `ACTIVE`, and associate the namespace-scoped policy:
```bash
aws eks associate-access-policy --cluster-name <CLUSTER> \
  --principal-arn arn:aws:iam::<ACCOUNT_ID>:role/aws-service-role/batch.amazonaws.com/AWSServiceRoleForBatch \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AWSBatchNamespacePolicy \
  --access-scope type=namespace,namespaces=<NAMESPACE>
```
Without this association, jobs stay RUNNABLE. Confirm the compute environment `status` is not `INVALID` (see
`statusReason`) before creating the queue:
```bash
aws batch create-job-queue --job-queue-name my-eks-jq --priority 10 \
  --compute-environment-order order=1,computeEnvironment=my-eks-ce
```
- The page says EKS compute environments support EC2 On-Demand and Spot instances; for Fargate use an ECS compute
  environment. With an empty queue Batch scales nodes down to the minimum you set (default zero).
- Batch decorates its nodes with labels and taints so other workloads are not placed there (DaemonSets excepted).

## 3. Job definition and submit
```bash
aws batch register-job-definition --cli-input-json file://./jobdef.json
aws batch submit-job --job-queue my-eks-jq --job-definition <JOB_DEF> --job-name <JOB_NAME>
aws batch describe-jobs --jobs <JOB_ID>
```
```json
{"jobDefinitionName": "my-eks-job", "type": "container",
 "eksProperties": {"podProperties": {"containers": [{"image": "<IMAGE>", "command": ["sleep", "60"],
   "resources": {"limits": {"cpu": "1", "memory": "1024Mi"}}}]}}}
```
The tutorial's definition also sets `hostNetwork: true` and pod labels. The page points to a separate topic for
memory and vCPU considerations; read it before sizing.

## Debugging
- Jobs stuck in RUNNABLE: per the page, a missing node-role access entry or a missing `AWSBatchNamespacePolicy`
  association are two causes.
- The API model's `describe-jobs` output has `eksAttempts` with `podName`, `podNamespace` and `nodeName`.
- Batch deletes the pods it creates after they finish; use `kubectl` to see running pods and nodes.

## Verify
- [ ] `accessEntry.status` is `ACTIVE`, compute environment `status` is not `INVALID`.
- [ ] A test job (e.g. `sleep 60`) leaves RUNNABLE and completes; `describe-jobs` shows its status.

## Checked
Date: 2026-11-07. Read: "Amazon EKS compute environments" overview (eks.html) in full, and getting-started-eks.html
through Step 6 (overview, prerequisites, Steps 1-6 including 3a). Not read: Steps 7-9 of that page, the ConfigMap
tutorial, "Shared responsibility", "Memory and vCPU considerations". API model (botocore batch) checked for
`eksConfiguration.accessEntry`, the allocation-strategy enum, and `eksAttempts[].podName/nodeName`.
Removed or replaced: a hand-written RBAC YAML and a manual `create-access-entry` for the service-linked role (the tutorial
has Batch create it and you associate `AWSBatchNamespacePolicy`), the SPOT example with `SPOT_PRICE_CAPACITY_OPTIMIZED`
(not on the pages read), the `batch.amazonaws.com/job-id` pod label, the `serviceAccountName` example, and the
"instance types/quotas" stuck-job claim. Dropped the eks-job-definitions.html source (stub, unreadable).
Method: documentation only; no commands were run.
