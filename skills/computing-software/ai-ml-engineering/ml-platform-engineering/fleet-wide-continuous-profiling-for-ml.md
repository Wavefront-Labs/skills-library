---
id: computing-software.ai-ml-engineering.ml-platform-engineering.fleet-wide-continuous-profiling-for-ml
name: fleet-wide-continuous-profiling-for-ml
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, continuous-profiling, pyroscope, parca, py-spy, gpu-profiling]
level: practitioner
status: draft
description: "Profile ML workloads continuously across the fleet: eBPF and py-spy CPU profiles with Pyroscope or Parca, GPU profiling signals, on-demand Nsight and torch.profiler."
sources:
  - https://grafana.com/docs/pyroscope/latest/
  - https://www.parca.dev/docs/overview
  - https://github.com/benfred/py-spy
  - https://pytorch.org/docs/stable/profiler.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Fleet-wide continuous profiling

**Goal:** find where training and inference fleets waste CPU and GPU time - dataloaders, tokenisation, serialisation, Python overhead - without reproducing problems by hand.

## Layers
| Layer | Tool | Mode |
|---|---|---|
| CPU (native + Python) | Parca / Grafana Pyroscope eBPF agent, py-spy | always-on, low overhead sampling |
| GPU utilisation shape | DCGM profiling metrics (SM, tensor activity) | always-on metrics |
| Kernel-level GPU | PyTorch profiler, Nsight Systems | on-demand or periodic short captures |
| Hangs | `py-spy dump --pid <pid>`, `torch.distributed` debug env | on demand |

## Always-on CPU profiling
Deploy an eBPF profiler (Parca agent or Grafana Alloy/Pyroscope eBPF) as a DaemonSet; it samples stacks for all processes (~1% overhead) and labels them with Kubernetes pod, namespace and node. Python frames need interpreter-aware unwinding - enable Python support in the agent, or run py-spy in the pod:
```bash
py-spy record -o profile.speedscope -f speedscope --pid $(pgrep -f train.py) --duration 60 --subprocesses
```
Query by job label to compare flame graphs between a fast and a slow run, or before and after a change.

## What it typically finds
- Dataloader workers spending time in image decode or tokenisation -> move to GPU decode (DALI), pre-tokenise, more workers.
- Main process stuck in Python loops between steps (logging, metric syncs, `.item()` calls forcing GPU sync).
- Serialisation / JSON parsing hot paths in inference servers.
- Collective waits (stragglers) visible as time in NCCL wait on some ranks.

## GPU-side
Track SM activity per job continuously; when it drops below baseline, trigger a short `torch.profiler` capture:
```python
from torch.profiler import profile, schedule, ProfilerActivity, tensorboard_trace_handler
with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
             schedule=schedule(wait=5, warmup=2, active=3, repeat=1),
             on_trace_ready=tensorboard_trace_handler("/fsx/profiles/job123")) as p:
    for step, batch in enumerate(loader):
        train_step(batch); p.step()
```
Make captures triggerable by a signal or flag file so long jobs can be profiled without restarts.

## Operating it
- Retention and cardinality: keep high-resolution profiles for days, aggregated for weeks.
- Access control: profiles can contain function names and arguments from proprietary code.
- Feed findings into the golden-path templates (dataloader defaults, logging intervals) so every team benefits.

## Verify
- [ ] Profiles available for any running job by pod label within minutes.
- [ ] At least one measured efficiency win traced to profiling data per quarter.
