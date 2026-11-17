---
id: computing-software.cybersecurity-defensive.security-architecture.iot-embedded-device-security
name: iot-embedded-device-security
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [security-architecture, iot-security, embedded-devices, etsi-en-303-645, nistir-8259, device-onboarding, iot-segmentation]
level: advanced
status: draft
description: "Secure IoT and embedded devices in an enterprise: procurement baselines (ETSI EN 303 645, NISTIR 8259), onboarding, segmentation, credentials, updates and monitoring."
sources: ["https://www.etsi.org/deliver/etsi_en/303600_303699/303645/02.01.01_60/en_303645v020101p.pdf", "https://csrc.nist.gov/pubs/ir/8259/a/final", "https://owasp.org/www-project-internet-of-things-top-10/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IoT and embedded device security

**Goal:** cameras, badge readers, building management, printers, sensors, conference room
systems and medical/lab devices do not become the easy way into the network.

## Procurement baseline (ETSI EN 303 645 / NISTIR 8259A)
Require from vendors: no universal default passwords; vulnerability disclosure policy;
security updates for a stated support period; secure storage of credentials; encrypted
communications; minimal exposed services; secure defaults; ability to delete data; SBOM on
request. Prefer devices supporting 802.1X, SNMPv3, syslog, central management and signed
firmware.

## Onboarding
- Inventory every device (type, firmware, owner, location, network) before connection.
- Change default credentials to unique ones stored in the vault; disable unused services
  (Telnet, UPnP, cloud P2P features).
- Register MAC/certificate for NAC; assign to the right segment automatically by profile.

## Network architecture
- Dedicated IoT VLANs/segments per device class, deny by default to corporate networks.
- Allow only required flows: device to its management server/NVR/controller, NTP, DNS;
  block direct internet unless the vendor cloud is required (then restrict to vendor domains
  via proxy).
- No inbound access from user networks except via management hosts.
- Wireless IoT on separate SSIDs (WPA2/3-Enterprise if supported, otherwise PSK per device
  group with rotation).

## Lifecycle
- Firmware update process with owners and a cadence; track vendor advisories (subscribe).
- End of support date in inventory; replace or isolate further when reached.
- Decommission: factory reset and remove credentials/certificates.

## Monitoring
NDR or flow monitoring on IoT segments: new destinations, scanning behaviour, unexpected
protocols. IoT devices rarely run EDR, so network is the main sensor. Defender for IoT /
Armis / Forescout give device profiling and anomaly detection.

## Gotchas
- Facilities and OT teams buy devices outside IT; involve procurement.
- Devices with hard-coded vendor backdoors or unpatchable flaws: compensate with strict isolation.
- Cloud-managed cameras phoning home to unknown regions; review data residency.

## Verify
From an IoT segment, attempts to reach corporate subnets fail; scans of the IoT segment show
no default credentials (checked by scanner) and only expected services.
