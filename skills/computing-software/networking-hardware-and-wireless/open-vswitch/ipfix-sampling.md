---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ipfix-sampling
name: ipfix-sampling
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ipfix, flow-sample-collector, sampling, obs-domain-id, collector-set, sample-action]
level: advanced
status: docs-checked
description: "Configure IPFIX in Open vSwitch: per-bridge sampling defaults, cache and template intervals, and flow-based sampling with the sample action."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
  - https://docs.openvswitch.org/en/latest/ref/ovs-actions.7/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ipfix sampling
Per-bridge sampling uses an IPFIX record attached to the bridge; flow-based sampling uses the OpenFlow `sample` action with a collector set.

IPFIX columns (defaults):
- `targets`: `ip:port` strings (required).
- `cache_active_timeout`: 0 to 4200 s, default 0 (0 = caching disabled); `cache_max_flows`: 0 to 4294967295, default 0 (0 = caching disabled).
- `stats_interval` and `template_interval`: 1 to 3600 s, default 600.
- `other_config:enable-tunnel-sampling`: default true; `other_config:virtual_obs_id`: optional string, max 254 bytes.

Per-bridge only: `sampling` 1 to 4294967295 (default 400), `obs_domain_id` and `obs_point_id` (default 0), `other_config:enable-input-sampling` and `enable-output-sampling` (default true).

Example (create and attach; ovs-vsctl record syntax):
`ovs-vsctl -- set Bridge br0 ipfix=@i -- --id=@i create IPFIX targets=\"10.0.0.1:4739\" sampling=64`

Flow-based: a `Flow_Sample_Collector_Set` row has `id` (0 to 4294967295, unique per bridge, the `collector_set_id`), `bridge`, optional `ipfix`, optional `local_group_id`. Then use an action:
`sample(probability=1000,collector_set_id=1,obs_domain_id=1,obs_point_id=1)` (probability is the number of sampled packets out of 65535, at least 1; `collector_set_id`, `obs_domain_id` and `obs_point_id` default to 0).

Gotcha: `local_group_id` configures the sample group id for local sampling; the `ipfix` reference is optional, so a collector set can exist without IPFIX targets.

## Checked
2026-11-09. Partial read (IPFIX, Flow_Sample_Collector_Set and Bridge ipfix sections) of ovs-vswitchd.conf.db(5): targets, cache_active_timeout, cache_max_flows, stats_interval, template_interval, enable-tunnel-sampling, virtual_obs_id (254 bytes), sampling (default 400), obs ids, enable-input-sampling and enable-output-sampling, collector set id, bridge, ipfix, local_group_id. Read the sample action in ovs-actions(7). Removed: the unsourced datapath restriction on local sampling and the verify step.
Method: documentation only; no commands were run.
