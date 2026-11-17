---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.performance-benchmarking
name: performance-benchmarking
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, performance-engineering, performance-benchmarking, benchmark-methodology, price-performance, fio]
level: practitioner
status: docs-checked
description: "Benchmark cloud services and instance types rigorously: define KPIs, run active benchmarking, check the limiter and known pitfalls, and compare price-performance."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/perf_process_culture_establish_key_performance_indicators.html", "https://www.brendangregg.com/activebenchmarking.html", "https://github.com/GoogleCloudPlatform/PerfKitBenchmarker"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Benchmarking cloud services

## Steps
1. **Question first**: define quantitative KPIs aligned with business goals (AWS PERF05-BP01 gives response time and
   throughput as examples, and says to document the business risk if a threshold is missed). Choose KPI thresholds
   from industry benchmarks and end-user expectations together.
2. **Know what is tested**: Gregg's "casual benchmarking" warning is that you benchmark A, measure B and conclude C.
   Study the benchmark's configuration and source before running it; avoid unrealistic workloads.
3. **Control variables**: do not compare different client or server software versions, and avoid client-side limits
   (single-threaded benchmark software, network between client and server, software resource controls).
4. **Active benchmarking**: while the benchmark runs, analyse all components with other tools (vmstat, iostat, mpstat,
   sar, top, perf and so on; the USE Method suits this) to find the true limiter. Where possible run long in a
   steady state, for example hours. Be able to explain why the result was X and not 2X.
5. **Statistics last**: Gregg advises statistical analysis only after active benchmarking has produced valid numbers;
   a high coefficient of variation can show results are untrustworthy.
6. **Price-performance**: benchmark results feed choices on "the best price performance"; take prices from the vendor's
   current pricing page.
7. **Standardise runs**: PerfKit Benchmarker wraps benchmarks such as fio, wrk, sysbench_oltp and memtier_benchmark,
   instantiates VMs on the chosen cloud, installs the benchmarks and runs them with default settings for consistency.
   You must accept each benchmark's licence yourself.
8. **Record** setup, raw results and scripts so runs can be repeated.

## Gotchas
- Neighbouring workloads can perturb a benchmark.
- Disk I/O and file system I/O are different things to test; know which you measured.
- A bar chart without supporting technical evidence is passive benchmarking.

## Verify
- [ ] Results reproducible from stored scripts.
- [ ] Limiting factor identified and stated for each configuration tested.

## Checked
2026-11-08. Confirmed against AWS PERF05-BP01 (KPIs, thresholds, documenting risk), Brendan Gregg's Active
Benchmarking page (casual benchmarking, active versus passive, tool list, USE Method, problem checklist, statistics
after active benchmarking, long steady-state runs) and the PerfKitBenchmarker README (wrapped benchmarks, VM
instantiation, default settings, per-benchmark licences). Removed: the 3-5 run rule, warm-up and snapshot-initialisation
advice, burstable-instance claim and the laptop-over-internet claim (not on these pages), and any pricing detail.
Method: documentation only; no commands were run.
