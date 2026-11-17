---
id: computing-software.cloud-infrastructure-engineering.aws.aws-parallel-computing-service-slurm
name: aws-parallel-computing-service-slurm
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, parallel-computing-service, aws-pcs, slurm, hpc, compute-node-groups]
level: advanced
status: docs-checked
description: "Stand up managed Slurm with AWS Parallel Computing Service: cluster size, compute and login node groups, queues, instance profile, AMIs and shared storage via lifecycle scripts."
sources:
  - https://docs.aws.amazon.com/pcs/latest/userguide/what-is-service.html
  - https://docs.aws.amazon.com/pcs/latest/userguide/key-concepts.html
  - https://docs.aws.amazon.com/pcs/latest/userguide/getting-started.html
  - https://docs.aws.amazon.com/pcs/latest/userguide/getting-started_create-sg.html
  - https://docs.aws.amazon.com/pcs/latest/userguide/getting-started_create-cng_instance-profile.html
  - https://docs.aws.amazon.com/pcs/latest/userguide/getting-started_create-cng_workers.html
  - https://docs.aws.amazon.com/pcs/latest/userguide/getting-started_create-cng_login-nodes.html
  - https://docs.aws.amazon.com/pcs/latest/userguide/getting-started_create-queue.html
  - https://docs.aws.amazon.com/pcs/latest/userguide/working-with_clusters_size.html
  - https://docs.aws.amazon.com/pcs/latest/userguide/working-with_ami.html
  - https://docs.aws.amazon.com/pcs/latest/userguide/working-with_ami_samples.html
  - https://docs.aws.amazon.com/pcs/latest/userguide/working-with_ami_custom.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Parallel Computing Service (PCS)

AWS PCS is a managed service for running HPC workloads with Slurm. A cluster has one or more queues, each associated with at least one compute node group; jobs are submitted to queues and run on EC2 instances defined by the node groups. The scheduler accepts and schedules jobs and launches the compute nodes. Slurm is the only scheduler offered.

## 1. Cluster
```bash
aws pcs create-cluster --cluster-name cfd --scheduler type=SLURM,version=<SLURM_VERSION> --size SMALL \
  --networking subnetIds=subnet-a,securityGroupIds=sg-pcs
aws pcs get-cluster --cluster-identifier cfd --query 'cluster.status'
```
- Pick the size from two factors: instances the cluster will manage and jobs the controller tracks (running, pending and recently completed). Small: up to 32 instances and 256 jobs; Medium: up to 512 and 8192; Large: up to 2048 and 16384.
- The size cannot be changed after creation; you must create a new cluster.
- The tutorial creates a cluster security group that enables communication between the PCS controller, compute nodes and login nodes, and an optional inbound-SSH security group for login nodes. Restrict the SSH source range to your own address.

## 2. Compute node groups
A node group is a set of instances sharing instance types, min/max count, subnets, AMI, purchase option and launch configuration.
```bash
aws pcs create-compute-node-group --cluster-identifier cfd --compute-node-group-name compute-1 \
  --subnet-ids subnet-a --custom-launch-template id=lt-0abc,version=1 \
  --iam-instance-profile-arn <PROFILE_ARN> --instance-configs instanceType=c6i.xlarge \
  --scaling-configuration minInstanceCount=0,maxInstanceCount=4
aws pcs create-compute-node-group --cluster-identifier cfd --compute-node-group-name login \
  --subnet-ids subnet-pub --custom-launch-template id=lt-login,version=1 --iam-instance-profile-arn <PROFILE_ARN> \
  --instance-configs instanceType=c6i.xlarge --scaling-configuration minInstanceCount=1,maxInstanceCount=1
```
- Compute group: private subnet, min 0 so it scales to no instances when no jobs are queued. Login group: a static group (min and max both 1) in a public subnet, reachable by SSH or SSM.
- A node group needs an instance profile. The tutorial's role has `AWSPCSComputeNodePolicy` (the one permission a node needs to register with and connect to the cluster), `AmazonSSMManagedInstanceCore` (SSM access without SSH), `AmazonS3ReadOnlyAccess` (download lifecycle action scripts) and `CloudWatchAgentServerPolicy` (log forwarding).
- The tutorial mounts shared storage with node lifecycle action scripts at the `nodeBootstrapped` stage, for example AWS-maintained `configure-efs-homes` (EFS as `/home`) and `mount-fsx-lustre` (FSx for Lustre at `/shared`).
- Wait for a node group to show Active before creating the queue.

## 3. AMIs
- PCS runs AMIs you provide. A custom AMI needs the AWS PCS agent and a compatible Slurm version; use the AWS-provided installers for the PCS software (and recommended for Slurm).
- AWS publishes sample AMIs named `aws-pcs-sample_ami-OS-architecture` (OS `al2023`, architecture `x86_64` or `arm64`). They are for demonstration and not recommended for production. Check the AMI description for the Slurm versions it supports. An AWS-maintained PCS-ready DLAMI is offered for production AI/ML and HPC.

## 4. Queues
```bash
aws pcs create-queue --cluster-identifier cfd --queue-name demo --compute-node-group-configurations computeNodeGroupId=<CNG_ID>
```
Users do not submit jobs to a node or node group directly: they submit to a queue (Slurm partition) from the login node. Each queue is associated with one or more node groups.

## Verify
- [ ] Cluster, node groups and queue all show Active.
- [ ] A single-node job and a multi-node MPI job submitted from the login node complete (the getting-started guide includes both).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the PCS User Guide pages listed in sources: concepts, cluster size table and immutability, security groups, instance profile policies, login and compute node group settings, lifecycle scripts, queue, and AMI pages. CLI commands and flags were checked against the botocore model by check_commands.py. Removed as not stated by the pages: the Slurm version value, `pcs:RegisterComputeNodeGroupInstance`, hpc7a instance type, EFA and placement group advice, Image Builder advice, user-data storage mounts (the guide uses lifecycle scripts), the ParallelCluster comparison table, and the `sinfo` check.
