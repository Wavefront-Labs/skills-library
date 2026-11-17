---
id: computing-software.qa-testing-engineering.performance-testing.load-generator-saturation-checks
name: load-generator-saturation-checks
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [load-generator-saturation, performance-test-environment, performance-monitoring, load-injector, client-side-bottleneck, k6, jmeter]
level: practitioner
status: verified
description: "Make sure the load generator is not the bottleneck: monitor injector CPU, memory, network and ports, calibrate per-injector capacity, and spot client-side artefacts."
sources:
  - https://grafana.com/docs/k6/latest/testing-guides/running-large-tests/
  - https://jmeter.apache.org/usermanual/best-practices.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Load generator saturation checks

**Goal:** the response times you report come from the system under test, not from an overloaded injector.

## Monitor on every injector during the test
- CPU: k6's guide says to keep utilisation within 80% and warns that at 100% on all cores response-time metrics become much larger than reality; Locust logs "CPU usage above 90%!" (threshold 90 in its source). JMeter's best-practices page covers sizing threads to the hardware, and the same logic applies.
- Memory: JMeter's best-practices page says it runs with a 1 GB heap by default and to increase it for big plans; k6's guide estimates ~1-5 MB per VU for simple tests (1000 VUs = 1-5 GB) and suggests `discardResponseBodies: true` where bodies are not needed (with it, `res.body` was `null` in a run); disable swap.
- Network: NIC throughput vs capacity; bandwidth-heavy tests (downloads) saturate links first.
- Ephemeral ports / file descriptors: the k6 large-test guide gives, for Linux, `ulimit -n 250000`, `sysctl -w net.ipv4.ip_local_port_range="1024 65535"` plus `net.ipv4.tcp_tw_reuse=1` and `net.ipv4.tcp_timestamps=1`; these values are for Linux generators, so check the k6 guide's OS fine-tuning section for the current text.
- k6 warnings: "Insufficient VUs, reached N active VUs and cannot initialize more" plus `dropped_iterations` (seen in a run), and high `http_req_blocked` / `http_req_connecting` times (both metrics appear with `--summary-mode=full`).

## Calibrate
1. Run the script against a fast stub (or the real SUT at low load) from one injector, increasing load until injector CPU ~70%: that is per-injector capacity.
2. Plan injectors = target load / capacity, plus margin.
3. Distributed runs for more (k6 operator / cloud, JMeter distributed mode (multiple CLI instances, per its best-practices page), Locust workers).

## Symptoms of a saturated injector
Response times rise with load while SUT CPU and queue metrics are flat; throughput plateaus with no server-side errors; timings differ between injectors.

## Gotchas
- Running the injector on the same host/cluster as the SUT: they compete for resources.
- Injector in a different region adds network latency to every number; document location.

## Verify
Injector metrics included in the report, all below thresholds for the whole run.

## Checked
k6 v1.4.0 and Locust 2.47.0 on Windows; fetched docs.
- Run: `discardResponseBodies: true` (`r.body` is null); under-provisioned arrival-rate scenario (the Insufficient VUs warning and `dropped_iterations` 63 vs 17 iterations); `--summary-mode=full` lists `http_req_blocked` and `http_req_connecting`; the Locust CPU warning threshold read from the installed source (`CPU_WARNING_THRESHOLD = 90`).
- Fetched: k6 running-large-tests guide (80% CPU, 1-5 MB per VU, swap advice, `discardResponseBodies`, the ulimit and sysctl lines) and JMeter best-practices page (1 GB default heap, CLI instances on several machines, thread sizing and coordinated omission).
- The Linux sysctl and ulimit values are quoted from the fetched k6 guide, not from a local run.
