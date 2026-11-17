---
id: computing-software.computer-graphics-engineering.computer-vision.inference-speed-benchmarking
name: inference-speed-benchmarking
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, cv-data-evaluation, inference-benchmarking, latency, throughput, trtexec, profiling]
level: practitioner
status: gated
description: "Benchmark vision model inference honestly: warm-up, synchronisation, batch and resolution sweeps, end-to-end vs model-only latency, percentiles, trtexec and ORT perf tools."
sources: ["https://pytorch.org/tutorials/recipes/recipes/benchmark.html", "https://github.com/NVIDIA/TensorRT/tree/main/samples/trtexec", "https://onnxruntime.ai/docs/performance/tune-performance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Benchmarking inference speed

## Rules
1. **Warm up** (10 to 50 iterations): first runs include allocation, kernel autotuning, JIT.
2. **Synchronise** GPU before reading timers: CUDA calls are asynchronous.
```python
import torch.utils.benchmark as tb
t = tb.Timer("m(x)", globals={"m": model, "x": x}).blocked_autorange(min_run_time=5)
print(t.median * 1e3, "ms")   # ran on CPU (ResNet-18, 224x224, no_grad): 48 ms median
# manual: torch.cuda.synchronize(); t0 = time.perf_counter(); ...; torch.cuda.synchronize()
```
3. Report **p50/p90/p99** latency, not just the mean; tail latency matters for real time.
4. Fix clocks/power mode (Jetson `nvpmodel`/`jetson_clocks` (gated: unconfirmed, source is paywalled or blocked), laptop on AC power) and record
   hardware, drivers, runtime versions, precision, batch size and input resolution.

## Latency vs throughput
Batch 1 latency for interactive/real-time; throughput (images/s) at the best batch size for
offline jobs. Sweep batch sizes and resolutions; plot.

## End-to-end
Measure decode -> preprocess -> inference -> postprocess (NMS) -> output. Preprocessing on CPU and
host-device copies often dominate small models. Profile each stage separately.

## Tools
- `trtexec --onnx=m.onnx --fp16 --shapes=images:1x3x640x640 --warmUp=500 --duration=10`: `--onnx`, `--fp16` and `--shapes=name:NxCxHxW` appear in the TensorRT trtexec README; `--warmUp`, `--duration` and the latency-percentile and H2D/D2H report were not confirmed and need a GPU (gated: unconfirmed, source is paywalled or blocked).
- `onnxruntime_perf_test -e cuda -r 200 m.onnx` (or the Python profiler) (gated: unconfirmed, source is paywalled or blocked; needs CUDA).
- `benchmark_app -m model.xml -d CPU` (OpenVINO) (gated: unconfirmed, source is paywalled or blocked; OpenVINO not installed).
- Nsight Systems for timeline-level bottlenecks.

## Gotchas
- Thermal throttling on edge devices: run for minutes, not seconds.
- Comparing frameworks at different precisions or with different preprocessing is not a comparison.
- Accuracy must be checked at the benchmarked configuration (FP16/INT8).

## Verify
Repeat runs on different days: results within a few percent indicate a stable setup.

## Checked
PyTorch 2.14.1 CPU, onnxruntime 1.31.0, torchvision 0.29.1.
- Run: `torch.utils.benchmark.Timer(...).blocked_autorange(min_run_time=...)` returns a `Measurement` with `.median` (48 ms for ResNet-18 on CPU); ONNX Runtime CPU on the same network took about 8.5 ms per run after warm-up (30 runs), a reminder to compare runtimes at equal settings.
- Fetched: NVIDIA TensorRT trtexec README on GitHub (the docs.nvidia.com command-line page URL in sources was 404, replaced): `--onnx`, `--shapes`, `--fp16`, `--int8`, `--saveEngine`.
- Not run: trtexec duration/warm-up flags, onnxruntime_perf_test, OpenVINO benchmark_app, Jetson clock tools (no GPU/devices); gated.
