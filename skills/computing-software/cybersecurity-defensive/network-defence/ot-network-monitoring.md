---
id: computing-software.cybersecurity-defensive.network-defence.ot-network-monitoring
name: ot-network-monitoring
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ot-network-monitoring, ics-monitoring, passive-asset-discovery, modbus, dnp3, zeek-ics, nozomi, claroty, dragos]
level: advanced
status: draft
description: "Monitor OT/ICS networks passively: sensor placement in the Purdue model, industrial protocol parsing, asset inventory, baselining process behaviour and safe response."
sources: ["https://www.cisa.gov/topics/industrial-control-systems", "https://csrc.nist.gov/pubs/sp/800/82/r3/final", "https://github.com/cisagov/icsnpp", "https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OT network monitoring

## Principles
- **Passive only** by default: SPAN/TAP feeds; active scanning can crash PLCs. Use vendor-safe active queries only with operations sign-off.
- Monitor where the risk crosses levels: IT/OT DMZ (Level 3.5), Level 3 site operations, Level 2 control networks (HMI/SCADA to PLCs).

## Tooling
- Commercial: Nozomi Guardian, Claroty xDome/CTD, Dragos Platform, Microsoft Defender for IoT - protocol DPI, asset inventory, vulnerability mapping, OT threat intel.
- Open source: Zeek with CISA **ICSNPP** parsers (Modbus extensions, DNP3, EtherNet/IP/CIP, BACnet, S7comm, OPC UA, PROFINET), Suricata with ICS rules, Malcolm (CISA's packaged NSM stack).

## What to detect
- New assets or new communication pairs (OT is stable - change is the signal).
- Engineering actions: PLC program download/upload, firmware update, mode change to PROGRAM/REMOTE, function codes for writes (Modbus FC 5/6/15/16, S7 write var, DNP3 direct operate) from non-engineering workstations.
- IT protocols appearing in control networks (RDP/SMB from internet-connected hosts, DNS to internet).
- Remote access sessions outside approved windows.

## Response
Coordinate with operations; never auto-block in Level 1/2. Playbooks name who can authorise isolation and
the safe states of the process.

## Gotchas
- SPAN on old industrial switches may be unavailable; use passive taps and plan outages for installation.
- Serial (RS-485) segments are invisible to network sensors.
- Baseline across a full production cycle (weekly/monthly batch processes).

## Verify
- [ ] Asset inventory from passive monitoring reconciled with engineering records.
- [ ] Test PLC write from a non-engineering host generates an alert (in a lab or approved window).
