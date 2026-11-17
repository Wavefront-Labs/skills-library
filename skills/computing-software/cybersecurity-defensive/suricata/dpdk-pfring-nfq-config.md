---
id: computing-software.cybersecurity-defensive.suricata.dpdk-pfring-nfq-config
name: dpdk-pfring-nfq-config
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [dpdk, pf-ring, nfq, ipfw]
level: advanced
status: docs-checked
description: "Configure DPDK, PF_RING, NFQ and IPFW capture sections in suricata.yaml, including DPDK eal-params, hugepages and NFQ modes."
sources: ["https://docs.suricata.io/en/latest/configuration/suricata-yaml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DPDK, PF_RING, NFQ, IPFW

## DPDK
Build with `--enable-dpdk`; config under `dpdk:` with `eal-params` and `interfaces`. Interface keys include `threads`, `promisc`, `multicast`, `checksum-checks`, `vlan-strip-offload`, `mtu`, `mempool-size`, `rx-descriptors`, `tx-descriptors`, `copy-mode`, `copy-iface`; a `default` entry fills gaps. Runmode is workers with a symmetric RSS hash; hugepages go on the NIC's NUMA node. Minimum DPDK 19.11.

## PF_RING
`interface`, unique `cluster-id`, `cluster-type` (default `cluster_flow`; `cluster_round_robin` not recommended; inner types hash after VLAN removal).

## NFQ
Modes: `accept` (default), `repeat` (with `repeat-mark` and `repeat-mask`), `route` (with `route-queue`).

## IPFW
Inline mode on FreeBSD uses ipfw; `ipfw-reinjection-rule-number: 5500` is the rule packets are re-injected at, and must come after the rule that sends traffic to Suricata.

## Checked

2026-11-04. Confirmed against the suricata.yaml configuration page: DPDK (eal-params, interfaces keys, default interface, workers runmode with symmetric hash, hugepages on the NIC's NUMA node, minimum DPDK 19.11), PF_RING cluster types, NFQ modes and options, Ipfw.

Method: documentation only; no commands were run.
