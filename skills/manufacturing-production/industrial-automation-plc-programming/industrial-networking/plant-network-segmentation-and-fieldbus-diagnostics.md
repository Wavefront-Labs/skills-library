---
id: manufacturing-production.industrial-automation-plc-programming.industrial-networking.plant-network-segmentation-and-fieldbus-diagnostics
name: plant-network-segmentation-and-fieldbus-diagnostics
category: manufacturing-production
field: industrial-automation-plc-programming
product: industrial-networking
tags: [industrial-networking, ot-network, profinet, ethernet-ip, modbus-tcp, modbus-rtu, rs-485, opc-ua, ethercat, profibus, devicenet, managed-switch, igmp-snooping, multicast, vlan, dmz, purdue-model, iec-62443, network-segmentation, firewall, ring-topology, mrp, dlr, device-level-ring, cable-shielding, termination, wireshark, ping, ip-addressing, duplicate-ip, industrial-automation-plc-programming]
level: practitioner
status: draft
description: "Lay out and fix plant-floor networks: Purdue/IEC 62443 zones, VLANs and IGMP snooping for EtherNet/IP and PROFINET, ring redundancy, Modbus RS-485 wiring, and a fault-finding sequence."
sources: ["IEC 62443 series (industrial automation and control systems security)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plant network segmentation and fieldbus diagnostics

**Goal:** a control network that keeps running when the office network misbehaves,
and a repeatable way to find out why a drive, I/O block or PLC dropped off.

*Draft: general practice; switch configuration syntax is vendor-specific and not given
here. Security architecture for regulated sites needs a qualified IEC 62443 review.*

## 1. Zones and conduits
- Use the **Purdue model** as a map: Level 0–1 devices/controllers, Level 2 HMI/SCADA,
  Level 3 site operations (historian, MES), **Level 3.5 DMZ**, Level 4–5 business IT.
- **IEC 62443 zones and conduits:** group assets with the same security needs; every
  path between zones goes through a defined conduit (firewall with explicit rules).
- No direct IT-to-PLC traffic. Remote access lands in the DMZ (jump host, MFA, session
  logging), never a modem or remote-desktop tool installed on an HMI.
- Machines from OEMs: put each on its own subnet behind a small firewall or NAT
  router, so identical OEM IP schemes (every machine is 192.168.1.10) don't clash.

## 2. Ethernet for real-time protocols
- **EtherNet/IP** implicit I/O often uses **multicast** (older firmware/defaults).
  Without **IGMP snooping** and a **querier** on the VLAN, unmanaged/badly configured
  switches flood multicast everywhere — HMIs lag and devices time out. Use managed
  switches; set unicast connections where the device supports it.
- **PROFINET RT** is layer-2 with priority tagging; devices are identified by
  **device name**. Keep PROFINET on its own VLAN/segment; IRT needs IRT-capable switches.
- **Ring redundancy:** MRP (PROFINET) or DLR (EtherNet/IP device-level ring) recovers in
  milliseconds from a single break. A ring with no manager configured is a broadcast
  storm. Test by pulling a cable.
- Don't put **unmanaged switches** in cabinets on critical networks — you lose
  diagnostics and port statistics.

## 3. Serial fieldbuses (Modbus RTU, PROFIBUS)
- RS-485: **daisy-chain** (no stars/long stubs), **120 Ω termination at both physical
  ends only**, shield grounded per the vendor's rule (often one end for Modbus;
  PROFINET/PROFIBUS cable usually both ends with equipotential bonding — check).
- Modbus: every slave has a unique address 1–247; baud rate, parity and stop bits must
  match on every node. Register numbering offsets (40001 vs 0-based) cause most
  "wrong value" bugs — test with a known register first.

## 4. Fault-finding sequence (device dropped off)
1. **Scope:** one device, one branch, or everything? Everything → switch/power/ring
   manager. One branch → cable, connector, switch port.
2. **Link LEDs** at both ends; switch port status and error counters (CRC/FCS errors
   = cabling or EMI; increasing over minutes = still happening).
3. **ping** the device from a laptop on the same segment; check for a **duplicate IP**
   (`arp -a` shows a MAC that isn't the device's). For PROFINET, check the device
   name and the controller's diagnostics view.
4. **Cable:** industrial connectors (M12, RJ45) loosen with vibration; routing next to
   VFD motor cables causes errors. Use a cable certifier for intermittent faults.
5. **Wireshark** on a mirrored (SPAN) port: look for multicast floods, retransmissions,
   ARP storms. A tap/SPAN port, not a hub, and with permission.
6. **Load:** too many CIP connections or a too-fast RPI/update time; check controller
   and comms module utilisation.

## 5. OPC-UA
- Use **certificates** and a security policy (Basic256Sha256 or newer), not
  `None`/anonymous, outside a bench test. Certificate trust lists must be exchanged
  both ways — "BadSecurityChecksFailed" usually means an untrusted certificate.

## Gotchas
- Laptops plugged into the control network with Wi-Fi bridging or DHCP servers
  enabled have taken lines down. Use a dedicated engineering laptop.
- Documentation of IPs/device names rots — keep an asset register with switch port.

## Verify
- [ ] Network drawing shows zones, conduits, VLANs and firewall rules.
- [ ] IGMP snooping + querier on every VLAN with multicast I/O.
- [ ] Ring redundancy tested by pulling a link; recovery logged.
- [ ] Switch port error counters near zero over 24 h.
- [ ] No inbound path from business IT to PLCs except via the DMZ.
