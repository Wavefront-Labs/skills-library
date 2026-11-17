---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-cpu-options-cores-and-threads
name: ec2-cpu-options-cores-and-threads
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, cpu-options, threads-per-core, licensing, hpc]
level: advanced
status: docs-checked
description: "Set EC2 CPU options (core count and threads per core) for per-core licensing and HPC, check valid values per type, and change them on stopped instances."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-specify-cpu-options.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/cpu-options-supported-instances-values.html", "https://docs.aws.amazon.com/cli/latest/reference/ec2/modify-instance-cpu-options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPU options: cores and threads per core

## 1. Why
- **Licensing:** fewer active cores on a memory-rich type can reduce per-core software licence cost (check
  your licence terms). For EC2 instances launched from license-included Windows and SQL Server AMIs, the EC2
  Optimize CPUs feature bills licensing fees on the vCPUs you configure; other instances are charged the same
  as with default CPU options.
- **HPC / latency:** disabling SMT (`ThreadsPerCore=1`) gives each thread a full core and more predictable performance.

## 2. Valid values
```bash
aws ec2 describe-instance-types --instance-types r7i.4xlarge \
  --query 'InstanceTypes[].VCpuInfo.{default:DefaultVCpus,cores:DefaultCores,validCores:ValidCores,validThreads:ValidThreadsPerCore}'
```
You cannot modify threads per core for T2, C7a, M7a, R7a, Apple silicon Mac instances, or instances on
AWS Graviton processors; check the supported-CPU-options table for the type before relying on a value.

## 3. Set at launch
```bash
aws ec2 run-instances --instance-type r7i.4xlarge --image-id <AMI> \
  --cpu-options CoreCount=4,ThreadsPerCore=1 ...
```
Or in a launch template `CpuOptions`.

## 4. Change later
```bash
aws ec2 stop-instances --instance-ids i-0abc && aws ec2 wait instance-stopped --instance-ids i-0abc
aws ec2 modify-instance-cpu-options --instance-id i-0abc --core-count 4 --threads-per-core 1
aws ec2 start-instances --instance-ids i-0abc
```

## Gotchas
- There is no additional charge for specifying CPU options, and the EC2 price of an instance with default licensing
  is the same as for default CPU options.
- The number of instances you can run is based on the default vCPUs of the instance types, not the reduced count
  (the vCPU quota is not affected by CPU options).
- `modify-instance-cpu-options` also accepts `--nested-virtualization`; the instance must be Stopped for any change.
- Check the licence terms of any commercial software before changing core or thread counts.

## Verify
- [ ] `lscpu` shows `Thread(s) per core: 1` and the expected `Core(s) per socket`.
- [ ] `aws ec2 describe-instances --query 'Reservations[].Instances[].CpuOptions'` matches.

## Checked

Date: 2026-10-27. Sources: EC2 User Guide pages "CPU options for Amazon EC2 instances" and "Specify CPU options for an Amazon EC2 instance"; AWS CLI 2.38.6 modify-instance-cpu-options reference; botocore EC2 model (VCpuInfo DefaultVCpus/DefaultCores/ValidCores/ValidThreadsPerCore, CpuOptionsRequest CoreCount/ThreadsPerCore).
Confirmed: run-instances --cpu-options syntax, launch template CpuOptions, modify-instance-cpu-options with --core-count and --threads-per-core on a stopped instance, the describe-instance-types query fields, no extra charge, quota counted on default vCPUs.
Corrected: Graviton, T2, C7a, M7a, R7a and Apple silicon Mac types cannot change threads per core (not only Graviton); the "reset on type change" claim was removed as unsupported.

Method: documentation only; no commands were run.
