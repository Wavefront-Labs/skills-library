---
id: computing-software.systems-network-administration.cisco-networking.model-driven-telemetry-gnmi
name: model-driven-telemetry-gnmi
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, model-driven-telemetry, gnmi, yang, grpc, telemetry-subscription, telegraf]
level: practitioner
status: draft
description: "Stream IOS-XE operational data with model-driven telemetry: configured gRPC dial-out subscriptions, gNMI dial-in, xpath choice, and a Telegraf collector."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/1712/b_1712_programmability_cg/m_1712_prog_mdt_telemetry.html
  - https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Model-driven telemetry (MDT) and gNMI

MDT pushes YANG-modelled data on a period or on change, instead of SNMP polling.

## Configured dial-out (device -> collector, gRPC)
```
netconf-yang                                   ! YANG infra must be running
telemetry ietf subscription 101
 encoding encode-kvgpb
 filter xpath /process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds
 source-address 10.255.0.7
 stream yang-push
 update-policy periodic 3000                    ! centiseconds: 30 s
 receiver ip address 10.99.0.70 57500 protocol grpc-tcp
```
`update-policy on-change` only for xpaths that support it (interface oper-status, for example).

## gNMI dial-in (collector subscribes)
```
gnxi
gnxi server
gnxi secure-server
gnxi secure-trustpoint GNMI-TP
gnxi secure-port 9339
```
Test: `gnmic -a 10.255.0.7:9339 -u netadmin -p <PW> --skip-verify subscribe --path "/interfaces/interface/state/counters" --sample-interval 30s`.

## Collector (Telegraf)
```toml
[[inputs.cisco_telemetry_mdt]]
  transport = "grpc"
  service_address = ":57500"
[[outputs.influxdb_v2]]
  urls = ["http://influx:8086"]
```

## Picking xpaths
Explore with YANG Suite or `show platform software yang-management process` / pyang on
Cisco's YANG models (github.com/YangModels/yang). Prefer Cisco-IOS-XE-*-oper models.

## Verify
```
show telemetry ietf subscription 101 detail     ! State Valid
show telemetry receiver all                      ! Connected
```
- [ ] Subscription Valid, receiver Connected, data arriving at the configured interval in the TSDB.
