---
id: computing-software.cloud-infrastructure-engineering.aws.direct-connect-monitoring-and-alarms
name: direct-connect-monitoring-and-alarms
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, direct-connect, dx-monitoring, connection-state, bgp-status, cloudwatch-alarms]
level: advanced
status: docs-checked
description: "Monitor Direct Connect with ConnectionState, light levels, errors, bandwidth and BGP peer status, plus AWS Health maintenance events, and alarm on each."
sources: ["https://docs.aws.amazon.com/directconnect/latest/UserGuide/monitoring-cloudwatch.html", "https://docs.aws.amazon.com/directconnect/latest/UserGuide/monitoring-overview.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Direct Connect monitoring

Direct Connect publishes metrics to CloudWatch in 5-minute intervals by default (1 minute minimum aggregation for the bit and packet rates).

## 1. Connection metrics (`AWS/DX`, dimension `ConnectionId`)
| Metric | Alarm idea |
|---|---|
| `ConnectionState` (1 up, 0 down; dedicated and hosted connections) | Minimum < 1 for 1 period |
| `ConnectionBpsEgress` / `ConnectionBpsIngress` (bits per second) | Sustained high share of port speed (your own threshold) |
| `ConnectionLightLevelTx` / `Rx` (dBm; also filterable by `OpticalLaneNumber`) | outside optic spec, early fibre warning |
| `ConnectionErrorCount` (all MAC-level errors since the last datapoint; use Sum) | > 0 |
| `ConnectionEncryptionState` (1 up, 0 down; on a LAG 1 means all connections up) | MACsec down |
Other connection metrics: `ConnectionPpsEgress/Ingress`, `ConnectionDiscardsPpsEgress`. `ConnectionCRCErrorCount` is no longer used.
Virtual interface metrics (dimension `VirtualInterfaceId`): `VirtualInterfaceBpsEgress/Ingress`, `VirtualInterfacePpsEgress/Ingress`.

```bash
aws cloudwatch put-metric-alarm --alarm-name dx-dxcon-abc-down --namespace AWS/DX --metric-name ConnectionState \
  --dimensions Name=ConnectionId,Value=dxcon-abc --statistic Minimum --period 60 --evaluation-periods 1 \
  --threshold 1 --comparison-operator LessThanThreshold --treat-missing-data breaching --alarm-actions <SNS_ARN>
```

## 2. BGP status
A physically up port with BGP down still black-holes traffic. Alarm on the native
`VirtualInterfaceBgpStatus` metric (1 up, 0 down; dimensions `ConnectionId`, `VirtualInterfaceId`
and `IpAddressFamily` = `ipv4` or `ipv6`). `VirtualInterfaceBgpPrefixesAccepted` and
`VirtualInterfaceBgpPrefixesAdvertised` count prefixes per peer, so a drop to zero is also an alarm.
For a point-in-time check:
```bash
aws directconnect describe-virtual-interfaces --query 'virtualInterfaces[].{vif:virtualInterfaceId,state:virtualInterfaceState,bgp:bgpPeers[].bgpStatus}'
```

## 3. Maintenance
Route AWS Health events for Direct Connect to the network on-call (Health events reach EventBridge
with `source: aws.health`; look up the exact event type codes in the AWS Health documentation).
Planned maintenance is why every DX needs a second path (second DX location or VPN backup).

## 4. Path checks
Ingress/egress drop to zero on one connection while the other spikes means BGP failed over: verify with
on-prem router logs and `bgpPeers` before declaring an outage.

## Verify
- [ ] Disabling the BGP session in a test window flips `VirtualInterfaceBgpStatus` and pages.
- [ ] Health maintenance events reach the team channel.

## Checked
2026-10-28. Confirmed on the Direct Connect CloudWatch metrics page: every metric name, unit and dimension above, the 5-minute default, ConnectionErrorCount semantics, ConnectionCRCErrorCount retired. Fixed: BGP status is a native metric (`VirtualInterfaceBgpStatus`), not something to build with a Lambda. Removed as unconfirmed: the `AWS_DIRECTCONNECT_MAINTENANCE_SCHEDULED` event code, VIF state events in EventBridge, the 80%/15 min threshold.
Method: documentation only; no commands were run.
