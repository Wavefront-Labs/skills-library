---
id: computing-software.systems-network-administration.cisco-networking.catalyst-center-assurance
name: catalyst-center-assurance
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst-center, dnac, catalyst-center-assurance, network-health, client-health, ai-network-analytics, intelligent-capture, telemetry]
level: practitioner
status: draft
description: "Use Catalyst Center Assurance: device/client/application health scores, issue triage, Path Trace, Intelligent Capture, and the telemetry each view depends on."
sources:
  - https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/catalyst-center-assurance/2-3-7/b_cisco_catalyst_assurance_2_3_7_ug.html
  - https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/catalyst-center/2-3-7/user_guide/b_cisco_catalyst_center_user_guide_237.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Catalyst Center Assurance

## What it collects
Telemetry from managed devices: SNMP, syslog, NetFlow/AVC, streaming telemetry (gRPC model-driven
on IOS XE), wireless controller data (client onboarding, RF), ISE/IPAM integrations.
Assurance correlates these into **health scores** (1-10) and **issues** with suggested actions.

## Views
| View | Use |
|---|---|
| Overall health | network, wired/wireless client, application health over time |
| Device 360 | one device: CPU/memory, interfaces, neighbours, events, issues |
| Client 360 | one client (by MAC/user): onboarding timeline (association, auth, DHCP), RF, roaming |
| Application experience | per-app latency/loss/jitter (AVC/ART from IOS XE routers/switches) |
| Issues | correlated problems (AP down, high CPU, DHCP failures, auth failures) with impact and guidance |
| Path Trace | hop-by-hop path between two endpoints incl. ACL and QoS checks |
| Intelligent Capture | packet capture and RF stats from APs for a client, on demand |

## Making it useful
- Devices must be **managed and provisioned** with telemetry settings (Design > Network Settings >
  Telemetry: syslog, SNMP traps, NetFlow collector = Catalyst Center, wired client data collection).
- Wireless: 9800 controllers need streaming telemetry to Catalyst Center (provisioned automatically).
- AI Network Analytics (cloud) for baselines and anomaly detection: needs cloud connectivity and opt-in.
- Tune issue settings (thresholds, priorities) or the issue list becomes noise.

## Workflow for a "Wi-Fi is bad" ticket
1. Client 360 by username/MAC: onboarding failures (auth/DHCP), RSSI/SNR, roaming events.
2. AP Device 360: radio utilisation, interference, client count.
3. Intelligent Capture on the client if issue is intermittent.
4. Path Trace to the application server for wired-side ACL/QoS problems.

## Verify
- [ ] Health dashboards populated for all sites; device telemetry status "Successful" in Inventory.
