---
id: computing-software.cybersecurity-defensive.network-defence.suricata-performance
name: suricata-performance
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [suricata-performance, suricata, af-packet, cpu-affinity, packet-drops, flow-bypass, ids-ips]
level: advanced
status: docs-checked
description: "Tune Suricata for line rate: AF_PACKET/cluster settings, worker threads and CPU affinity, ring sizes, memcaps, bypass for elephant flows, and reading drop counters."
sources: ["https://docs.suricata.io/en/latest/performance/index.html", "https://docs.suricata.io/en/latest/performance/high-performance-config.html", "https://docs.suricata.io/en/latest/performance/packet-capture.html", "https://docs.suricata.io/en/latest/performance/statistics.html", "https://docs.suricata.io/en/latest/performance/tuning-considerations.html", "https://docs.suricata.io/en/latest/performance/analysis.html", "https://docs.suricata.io/en/latest/rule-management/rule-profiling.html", "https://docs.suricata.io/en/latest/configuration/suricata-yaml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Suricata performance tuning

## Measure first
`suricatasc -c "dump-counters"` or `stats.log`/EVE stats: watch `capture.kernel_packets`,
`capture.kernel_drops`, `tcp.reassembly_gap`, `tcp.ssn_memcap_drop` and `tcp.segment_memcap_drop`. The docs say
`capture.kernel_drops` should stay below 1% of `capture.kernel_packets`, and any `memcap` counter in the stats
means the configured memcaps need raising.

## Capture (AF_PACKET, workers runmode)
```yaml
runmode: workers
af-packet:
  - interface: ens1f0
    threads: 16
    cluster-id: 99
    cluster-type: cluster_flow     # or cluster_qm with RSS symmetric hashing
    defrag: yes
    use-mmap: yes
    tpacket-v3: yes
    ring-size: 100000
    block-size: 1048576
```
NIC: disable LRO/GRO (they merge packets into super packets and break `dsize` and TCP state tracking; checksum
offload may stay on for AF_PACKET): `ethtool -K ens1f0 gro off lro off`. Set the RSS queue count to the thread count
(`ethtool -L`) with a symmetric hash (the docs use a repeating `6D:5A` Toeplitz key via `ethtool -X ... hkey`), and
size the rx ring (the docs example uses `ethtool -G eth1 rx 1024`).

## CPU
```yaml
threading:
  set-cpu-affinity: yes
  cpu-affinity:
    management-cpu-set:
      cpu: [ 0 ]
    worker-cpu-set:
      cpu: [ "2-17" ]
      mode: "exclusive"
      prio:
        default: "high"
```
Keep workers on the NUMA node local to the NIC; isolate CPUs from the scheduler (`isolcpus`).

## Memory and flows
- `stream.memcap`, `stream.reassembly.memcap`, `flow.memcap` sized to traffic; memcap hits show up as `memcap` counters in the stats.
- `stream.reassembly.depth` (1mb in the documented example) limits inspection per stream.
- **Bypass**: `stream.bypass: yes` bypasses a flow once either side reaches its reassembly `depth`; the docs warn it can lead to missing important traffic. For encrypted TLS or SSH sessions see the `encryption-handling: bypass` options under `app-layer.protocols`.

## Rules
Profile rules to find expensive ones: build with `--enable-profiling-rules`, then `suricatasc -c ruleset-profile-start`, `ruleset-profile-stop` and `ruleset-profile` (report written to `rule_perf.log`); `sample-rate` in the `profiling` section of suricata.yaml limits the cost on busy systems.

## Gotchas
- Drops counted by the NIC (`ethtool -S` rx_missed) are invisible to Suricata counters; check both.
- Asymmetric hashing splits a flow across workers and breaks reassembly.

## Verify
- [ ] Kernel drops < 1% at peak over a week.
- [ ] No memcap counters increasing.

## Checked

Checked 2026-10-25 against Suricata user guide source (OISF/suricata doc/userguide, main branch, last pushed 2026-10-23, 8.x documentation). Confirmed: `workers` runmode as the best performing, `cluster_flow` (default) and `cluster_qm` with symmetric RSS, `tpacket-v3`, `block-size`, `management-cpu-set`/`worker-cpu-set` with `mode: "exclusive"` and `prio`, `isolcpus`, `stream.bypass` semantics, `stream.reassembly.depth` of 1mb, the below-1% kernel drop guideline, and that NIC drops are separate from Suricata counters. Corrected: the CPU affinity layout is a mapping (not a list), the rule profiling build flag is `--enable-profiling-rules` with `suricatasc` start/stop/dump commands, the offload advice is limited to LRO/GRO per the packet-capture page, and the counter list uses documented names. Removed unconfirmed `tso`/`gso`, `4096` ring, eBPF/XDP bypass and silent-memcap claims.

Method: documentation only; no commands were run.
