---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-instance-families-and-burstable-credits
name: ec2-instance-families-and-burstable-credits
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, instance-family, burstable, cpu-credits, t-unlimited, graviton, instance-types]
level: practitioner
status: docs-checked
description: "Pick EC2 instance families from the naming scheme and workload profile, and run T-family burstable instances safely: CPU credits, baseline, unlimited mode and the alarms to set."
sources: ["https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances-unlimited-mode-concepts.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EC2 instance families and burstable CPU credits

## 1. Read the name: `m7gd.2xlarge`
- **Series** (first letters): `c` compute optimized, `m` general purpose, `r` memory optimized,
  `x` memory intensive, `u` high memory, `i`/`im`/`is` storage optimized, `d` dense storage, `g`/`p` graphics and GPU,
  `inf`/`trn` Inferentia and Trainium, `vt` video transcoding, `f` FPGA, `hpc` high performance computing, `t` burstable
  performance, `z` high memory with high CPU frequency, `mac` macOS.
- **Generation**: the number after the series, for example the 7 in `m7g`.
- **Options**: `g` AWS Graviton, `a` AMD, `i` Intel, `d` instance store volumes, `n` network and EBS optimized,
  `e` extra storage, memory or GPU memory, `b` block storage optimization, `z` high CPU frequency, `flex` flex
  instances (`m7i-flex`).
- **Size**: after the period, such as `xlarge` or `4xlarge`; `metal` is bare metal.

Find candidates by requirements rather than memory:
```bash
aws ec2 get-instance-types-from-instance-requirements --architecture-types arm64 --virtualization-types hvm \
  --instance-requirements 'VCpuCount={Min=4,Max=8},MemoryMiB={Min=16384},InstanceGenerations=[current]'
aws ec2 describe-instance-types --instance-types m7g.xlarge --query 'InstanceTypes[0].[VCpuInfo.DefaultVCpus,MemoryInfo.SizeInMiB,NetworkInfo.NetworkPerformance,EbsInfo.EbsOptimizedInfo.BaselineThroughputInMBps]'
```
Graviton (`g`) instances are Arm-based, so check that your binaries and containers are multi-arch.

## 2. Burstable (T family)
- Each size has a **baseline** CPU % per vCPU (e.g. t3.micro 10%, t3.large 30%); below it you
  earn credits, above it you spend them (1 credit = 1 vCPU at 100% for 1 minute).
- **Standard mode**: at zero balance CPU is throttled to baseline → latency cliffs.
- **Unlimited mode** (default for T4g, T3a and T3; T2 defaults to standard): bursts continue; if the average CPU
  over a rolling 24-hour period exceeds baseline, the surplus credits are billed per vCPU-hour.
```bash
aws ec2 modify-instance-credit-specification --instance-credit-specifications 'InstanceId=i-123,CpuCredits=unlimited'
```
Metrics: `CPUCreditBalance`, `CPUCreditUsage`, `CPUSurplusCreditBalance`, `CPUSurplusCreditsCharged`.

Rule: if average CPU sits above baseline most of the day, unlimited mode incurs surplus-credit charges —
compare against a fixed-performance family such as `m` or `c`.

## Gotchas
- Standard mode instances that run out of credits are held to the baseline CPU.
- Some instance sizes also have burstable EBS bandwidth; `EBSIOBalance%` and `EBSByteBalance%` track it (basic monitoring only, some `*.4xlarge` sizes).
- Features differ by hypervisor generation: for example the EC2 Serial Console needs a Nitro-based instance.

## Verify
- [ ] For each T instance: `CPUSurplusCreditsCharged` over 30 days is ~0, or the instance was moved to a fixed-performance family.
- [ ] Alarm on `CPUCreditBalance` low for standard-mode instances.
- [ ] Chosen type validated with a load test at peak, not just average CPU.

## Checked

Checked 2026-10-27 against the Amazon EC2 instance types guide (naming conventions), the EC2 User Guide (burstable performance instances, key concepts, unlimited mode, serial console prerequisites) and the botocore EC2 model.
- Naming components (series, generation, options, size, `metal`) and the option letters confirmed on the naming conventions page; the memory-per-vCPU ratios, the "doubles each size" rule and the cheaper-per-performance claims are not on that page and were removed.
- Credit definition (1 credit = 1 vCPU at 100% for 1 minute), baselines (t3.micro 10%, t3.large 30%), unlimited as default for T4g, T3a and T3 and standard for T2, and surplus billing against the 24-hour average confirmed on the key concepts page.
- `get-instance-types-from-instance-requirements`, `describe-instance-types` output fields and `modify-instance-credit-specification` (`CpuCredits`) confirmed in the service model.
- Removed the Graviton "about 20% cheaper" statement and the steal-time remark.

Method: documentation only; no commands were run.
