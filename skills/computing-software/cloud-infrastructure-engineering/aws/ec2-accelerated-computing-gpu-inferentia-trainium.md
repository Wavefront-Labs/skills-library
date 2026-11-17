---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-accelerated-computing-gpu-inferentia-trainium
name: ec2-accelerated-computing-gpu-inferentia-trainium
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, accelerated-computing, gpu-instances, inferentia, trainium]
level: advanced
status: docs-checked
description: "Pick and run accelerated EC2 instances (NVIDIA GPU, Inferentia, Trainium): families, AMIs and drivers, quotas, capacity and multi-node EFA setup."
sources: ["https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html", "https://docs.aws.amazon.com/dlami/latest/devguide/what-is-dlami.html", "https://docs.aws.amazon.com/dlami/latest/devguide/find-dlami-id.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa-start.html", "https://awsdocs-neuron.readthedocs-hosted.com/en/latest/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU, Inferentia and Trainium instances

## 1. Choosing a family
| Need | Families |
|---|---|
| Large-scale training, NVIDIA | P5/P5e/P6 (H100/H200/Blackwell), P4d/P4de (A100) |
| Inference, graphics, small training | G6/G6e (L4/L40S), G5 (A10G) |
| Low-cost inference on AWS silicon | Inf2 (Inferentia2) |
| Cost-efficient training on AWS silicon | Trn1/Trn2 (Trainium) |
| Video transcode | VT1 |
Check Region/AZ availability with `aws ec2 describe-instance-type-offerings --location-type availability-zone --filters Name=instance-type,Values=<TYPE>`.

## 2. Software stack
- NVIDIA: Deep Learning AMI (DLAMI, preconfigured with NVIDIA CUDA, cuDNN and the common frameworks). Check
  the GPUs with `nvidia-smi`.
- Inferentia/Trainium: the Neuron SDK (compiler `neuronx-cc`, PyTorch integration `torch-neuronx`); see the
  Neuron documentation for the matching DLAMI and the monitoring tools.
- AMI lookup by SSM parameter, for example
  `aws ssm get-parameter --name /aws/service/deeplearning/ami/x86_64/base-oss-nvidia-driver-ubuntu-22.04/latest/ami-id`;
  the DLAMI release notes list the parameter name for each AMI.

## 3. Capacity and quotas
- Quotas are vCPU-based per instance family group in Service Quotas; Spot has separate quotas such as
  "All P Spot Instance Requests", "All G and VT Spot Instance Requests", "All Inf Spot Instance Requests" and
  "All Trn Spot Instance Requests". Check the On-Demand and Spot quotas for your family before planning, and request increases early.
- Scarce types: EC2 Capacity Blocks for ML (1 to 14 days in 1-day steps, then 7-day steps up to 182 days, starting up to 8 weeks ahead)
  or On-Demand Capacity Reservations.

## 4. Multi-node training
- EFA-enabled instances; AWS recommends a cluster placement group (not required) for the lowest latency.
- Launch with `--network-interfaces 'DeviceIndex=0,InterfaceType=efa,...'`; the security group must allow all inbound and outbound traffic to and from itself.
- Validate with `fi_info -p efa -t FI_EP_RDM` and the NCCL tests your framework documents.

## Verify
- [ ] `nvidia-smi` (or the Neuron tools) lists all devices; a framework smoke test runs on the accelerator.
- [ ] Multi-node NCCL bandwidth near the figure documented for the instance.

## Checked

Checked 2026-10-27 against the Amazon EC2 instance types guide (accelerated computing specifications), the EC2 User Guide (Spot quotas, Capacity Blocks, EFA), the Deep Learning AMI guide and the Neuron documentation.
- Families and accelerators confirmed on the instance specifications page: P5/P5e (H100/H200), P6 (B200/B300), P4d/P4de (A100), G6 (L4), G6e (L40S), G5 (A10G), Inf2 (Inferentia2), Trn1/Trn2, VT1.
- DLAMI contents, the SSM parameter form (`get-parameter` under `/aws/service/deeplearning/ami`), EFA security group, cluster placement group recommendation, `fi_info -p efa -t FI_EP_RDM` and `InterfaceType=efa` confirmed on the DLAMI and EFA pages.
- Spot quota names confirmed on the Spot quotas page. Capacity Block durations and lead time confirmed on the Capacity Blocks pages.
- Removed the exact On-Demand quota names and the "new accounts start at 0" remark (not on a readable page), the `neuron-ls`/`neuron-top` names, the bulk `get-parameters-by-path` form and the SageMaker HyperPod mention.

Method: documentation only; no commands were run.
