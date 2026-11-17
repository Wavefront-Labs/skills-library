---
id: computing-software.ai-ml-engineering.ml-platform-engineering.high-speed-interconnect-efa-infiniband-nccl
name: high-speed-interconnect-efa-infiniband-nccl
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, gpu, efa, infiniband, nvlink, nccl-tests, placement-groups, multi-node-training]
level: practitioner
status: draft
description: "Set up and verify fast networking for multi-node training: NVLink vs InfiniBand/RoCE vs AWS EFA, placement, NCCL plugins and env vars, nccl-tests bandwidth checks."
sources:
  - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa-start-nccl.html
  - https://github.com/NVIDIA/nccl-tests
  - https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html
  - https://cloud.google.com/compute/docs/gpus/gpudirect
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# High-speed interconnect for multi-node training

**Goal:** multi-node collectives run near hardware bandwidth, so adding nodes actually speeds training.

## The layers
- **Intra-node:** NVLink/NVSwitch between GPUs in one server (hundreds of GB/s per GPU). `nvidia-smi topo -m` shows the topology; PCIe-only paths are much slower.
- **Inter-node:** InfiniBand or RoCE (on-prem and some clouds), AWS **EFA** (p4d/p5 families), GCP GPUDirect-TCPX/TCPXO or RDMA on A3/A4 families, Azure InfiniBand on ND-series.
- **GPUDirect RDMA:** NIC reads/writes GPU memory directly, bypassing host copies.

## Placement
Nodes must be physically close: AWS cluster placement groups, GCP compact placement policies, same InfiniBand fabric/rail. Reserve the topology, not just GPU count.

## AWS EFA checklist
- EFA-enabled instance + security group allowing all traffic to itself; EFA interfaces attached (several on p5).
- Install EFA software, the libfabric-based NCCL plugin (aws-ofi-nccl), matching NCCL/CUDA versions (AWS Deep Learning AMIs/containers include them).
- `FI_PROVIDER=efa`, `FI_EFA_USE_DEVICE_RDMA=1` (where supported); in Kubernetes, the EFA device plugin exposes `vpc.amazonaws.com/efa` resources to request.

## Verify bandwidth with nccl-tests
```bash
mpirun -np 16 -H node1:8,node2:8 -x NCCL_DEBUG=INFO -x FI_PROVIDER=efa \
  ./build/all_reduce_perf -b 8 -e 8G -f 2 -g 1
```
Read **busbw** at large message sizes and compare with the platform's published expectation. `NCCL_DEBUG=INFO` logs show which transport was chosen - "NET/Socket" when you expected EFA/IB means the fast path is not in use (wrong plugin, interface, or permissions).

## Useful NCCL env vars
`NCCL_DEBUG=INFO|WARN`, `NCCL_DEBUG_SUBSYS=INIT,NET`, `NCCL_SOCKET_IFNAME` (bootstrap interface), `NCCL_IB_HCA` (which IB devices), `NCCL_P2P_DISABLE`/`NCCL_SHM_DISABLE` only for debugging. Don't copy env var sets from other clusters blindly; defaults are usually right once the plugin is correct.

## Verify
- [ ] nccl-tests busbw within ~10-20% of expected for the instance type.
- [ ] NCCL logs show the RDMA transport.
- [ ] Training throughput scales near-linearly from 1 to N nodes (measure tokens/s).
