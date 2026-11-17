---
id: computing-software.ai-ml-engineering.ml-platform-engineering.cost-optimization-for-training-and-inference
name: cost-optimization-for-training-and-inference
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, cost-optimization, spot-instances, preemptible-vms, gpu-utilization, autoscaling, cost-per-token, reserved-instances, checkpointing-for-preemption, right-sizing, finops, cloud-gpu-cost]
level: advanced
status: draft
description: "Cut ML infra cost without cutting corners: spot/preemptible training with checkpoint-resilience, right-sizing GPU instances, and the utilization metrics that reveal waste."
sources:
  - https://aws.amazon.com/ec2/spot/
  - https://cloud.google.com/compute/docs/instances/preemptible
  - https://www.cncf.io/projects/kubecost/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost optimization for training and inference infrastructure

**Goal:** cut cloud ML spend (often the largest line item after headcount) by targeting the actual waste — idle GPUs, oversized instances, and on-demand pricing where spot/preemptible would do — without sacrificing reliability.

## 1. Spot/preemptible for training — the resilience you need to make it safe
- Spot/preemptible GPU instances run 60–90% cheaper than on-demand but can be reclaimed with short notice (seconds to ~2 minutes depending on cloud). This is **free money only if the job survives preemption** — without checkpoint/resume (see computing-software.ai-ml-engineering.pytorch.training-loop for the full checkpoint contract), a preempted job loses all progress and the "savings" evaporate into wasted compute and wall-clock time.
- Checkpoint frequency should be set from the **preemption notice window and the job's throughput**, not an arbitrary interval: if checkpointing takes 2 minutes and the cloud gives a 2-minute notice, you need a checkpoint already recent enough (e.g. every 10–15 minutes) that the in-flight work lost on preemption is small relative to total runtime — do the arithmetic for your actual job, don't copy a number from a blog post.
- For multi-node distributed jobs, a **single preempted node kills the whole job** unless the orchestrator (Kubernetes + an elastic training framework, or a job queue with automatic retry-from-checkpoint) resubmits automatically — plan for this at the orchestration layer, not by hoping preemption won't happen during a long run.
- Mix spot and on-demand deliberately: a cluster that's majority spot with a small on-demand "anchor" fraction for critical path reduces the chance of losing all capacity simultaneously (spot capacity can dry up in a zone/instance-type entirely during demand spikes).

## 2. Right-sizing — the waste that doesn't show up as an error
- **GPU utilization, not just "is it running," is the metric that matters.** A training job showing 30% GPU utilization on an A100 is paying A100 prices for a fraction of an A100's throughput — usually a DataLoader bottleneck, small batch size, or a CPU-bound preprocessing step (same diagnosis as computing-software.ai-ml-engineering.pytorch.training-loop's DataLoader tuning). Fix the bottleneck before concluding you need a bigger/more GPU.
- Match GPU type to workload: cheaper, older-generation GPUs (or smaller memory tiers) are often adequate for smaller models or inference-only workloads — defaulting every job to the newest flagship GPU because it's available is a common unexamined cost driver. Benchmark cost-per-unit-of-work (cost per training step, cost per 1k inference tokens), not just raw speed.
- For inference, **batch dynamically and autoscale on queue depth** (see computing-software.ai-ml-engineering.mlops.model-serving-architectures) — a fixed fleet sized for peak traffic sitting mostly idle off-peak is one of the largest avoidable inference costs; scale-to-near-zero off-peak if latency SLOs allow, keep a warm minimum if cold starts are too slow.
- Idle notebook/dev GPU instances left running overnight or over weekends are a chronic, boring cost leak — enforce auto-shutdown on idle (via a scheduled check or platform policy), don't rely on users remembering.

## 3. Measurement — you can't optimize what you don't attribute
- Tag every resource (job, notebook, serving endpoint) with team/project/owner at creation time — cost without attribution produces a large bill nobody feels empowered to fix. Tools like Kubecost (Kubernetes) or cloud-native cost allocation reports make per-team/per-model cost visible.
- Track **cost per unit of outcome** (cost per trained model, cost per million inference requests, cost per percentage point of accuracy gained from a larger model) rather than raw dollar totals — this is what lets you compare "is the bigger model worth it" as an actual tradeoff instead of an assumption.
- Reserved/committed-use discounts make sense only for **steady-state, predictable** load (an always-on inference endpoint with known baseline traffic); applying them to bursty/experimental training workloads locks in capacity you may not use and removes the flexibility spot pricing offers for that exact workload shape — match the pricing commitment to the load pattern, not the other way around.

## Verify
- [ ] Every spot/preemptible training job has checkpoint/resume tested under an actual simulated preemption, not just in theory.
- [ ] Checkpoint interval is derived from the cloud's preemption notice window and checkpoint write time, not copied from elsewhere.
- [ ] GPU utilization is monitored per job; jobs under ~70% utilization are investigated for a bottleneck before requesting more/bigger GPUs.
- [ ] Inference fleets autoscale on queue depth/in-flight requests and have a documented off-peak floor.
- [ ] Every cloud resource is tagged with an owning team/project at creation.
- [ ] Reserved/committed spend is limited to workloads with steady, predictable utilization.
