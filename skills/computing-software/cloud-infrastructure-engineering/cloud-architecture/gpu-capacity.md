---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.gpu-capacity
name: gpu-capacity
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, compute-selection, gpu-capacity, accelerators, capacity-reservations, ml-infrastructure]
level: advanced
status: docs-checked
description: "Plan accelerator and GPU capacity: pick GPU families by workload, secure capacity with EC2 Capacity Blocks or Google reservations, Spot and Flex-start, and monitor with DCGM."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-blocks.html", "https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/overview", "https://docs.cloud.google.com/compute/docs/gpus", "https://docs.nvidia.com/datacenter/dcgm/latest/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accelerator / GPU capacity planning

## Steps
1. **Characterise the workload**: large multi-node training (needs fast GPU interconnect), fine-tuning, inference
   (latency versus throughput, model memory footprint) or HPC/rendering. Check GPU memory per accelerator in the
   vendor's table before sizing: for example Google lists 80 GB HBM3 per H100, 141 GB HBM3e per H200, 180 GB per B200
   and 24 GB GDDR6 per L4.
2. **Choose the family** from the cloud's own table, not memory. Azure splits GPU sizes into NC (compute, graphics,
   visualisation), ND (large-memory compute, deep learning), NV (virtual desktop, rendering) and others. Google's
   accelerator-optimised series are A4X (GB200), A4 (B200), A3 Ultra (H200), A3 Mega/High/Edge (H100) for training and
   serving, and G2 (L4), described as suited to cost-optimised inference.
3. **Secure capacity**:
   - AWS EC2 Capacity Blocks for ML reserve GPU instances for a future date and period: start up to 8 weeks ahead (offers
     can start in as little as 30 minutes), up to 64 instances per block and 256 across blocks (and across the
     organisation on a given date). Instances must target the reservation ID; blocks cannot be cancelled, moved or
     split, end at 11:30 UTC (termination starts at 11:00 UTC), do not support placement groups, and only some instance
     types and Regions are offered.
   - Google A4 and A3 Ultra require you to reserve capacity, use Spot VMs, use Flex-start VMs or create a resize
     request in a managed instance group; some small A3 High shapes must use Spot or Flex-start.
   - Azure: check the size family page and the Azure capacity reservation documentation for the SKU (not covered by the
     page cited here).
4. **Quotas and regional offers**: confirm that your chosen instance type is offered in your Region (Capacity Blocks
   are listed per instance type and Region) before planning dates.
5. **Monitor utilisation** with NVIDIA DCGM (its Field Identifiers reference lists the metric IDs, and DCGM Exporter
   publishes them to Prometheus); idle reserved GPUs are the main waste.
6. **Auto Scaling / EKS**: you can schedule scaling to run at the start of a Capacity Block; AWS retries for you.

## Gotchas
- A Capacity Block is paid for its reserved duration. Instances in it do not count against your On-Demand instance limits.
- Data loading bottlenecks leave GPUs idle; profile input pipelines.
- For P5 instances with a custom AMI, ensure the EFA software and configuration are present.

## Verify
- [ ] Capacity plan with reservation dates matches project timeline.
- [ ] GPU utilisation dashboard with idle alerting.

## Checked
2026-11-08. Confirmed against the EC2 Capacity Blocks page (limits, timings, restrictions), the Azure VM sizes
overview (GPU family names), the Google GPU machine types page (series, GPU memory, reserve/Spot/Flex-start
requirements) and the DCGM documentation home page; all read in full. Removed as unconfirmed: the 70B/140 GB sizing
arithmetic, L40S/A10G recommendations, Trainium/Inferentia and TPU advice, MIG partitioning, DWS calendar mode,
named DCGM metric IDs, Slurm/Kueue/Volcano, and advice to request quota weeks ahead.
Method: documentation only; no commands were run.
