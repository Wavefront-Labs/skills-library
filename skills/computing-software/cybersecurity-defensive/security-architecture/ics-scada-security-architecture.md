---
id: computing-software.cybersecurity-defensive.security-architecture.ics-scada-security-architecture
name: ics-scada-security-architecture
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [security-architecture, ics-security, scada, nist-800-82, ot-security, safety-systems, defense-in-depth]
level: advanced
status: draft
description: "Design ICS/SCADA security architecture per NIST SP 800-82: asset and flow baselines, defence in depth, engineering workstation and remote access controls, patching and monitoring."
sources: ["https://csrc.nist.gov/pubs/sp/800/82/r3/final", "https://www.cisa.gov/topics/industrial-control-systems", "https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ICS/SCADA security architecture

**Goal:** protect industrial control systems where availability and safety come first,
using controls that respect real-time constraints and long equipment lifecycles (NIST SP
800-82r3, IEC 62443).

## Principles that differ from IT
- Safety and availability outrank confidentiality; a security control must not trip the process.
- Systems run 15-30 years; many cannot be patched or run agents.
- Changes need engineering and safety review and often a planned outage.
- Protocols (Modbus, DNP3, S7, EtherNet/IP) often lack authentication.

## Architecture layers
1. **Asset and flow baseline:** passive inventory of PLCs, RTUs, HMIs, historians, engineering
   workstations (EWS), firmware versions, and the normal communications matrix.
2. **Segmentation:** Purdue levels and IEC 62443 zones/conduits, industrial DMZ between IT and OT,
   SIS separated from basic process control.
3. **Engineering workstations:** the crown jewels (they can reprogram PLCs). Dedicated,
   hardened, application allowlisting, no email/web, logged access, project files in version control.
4. **Remote access:** via IDMZ jump hosts with MFA, approval per session, session recording,
   vendor access time-boxed; no persistent vendor VPNs.
5. **Controller protection:** PLC key switches in RUN (not PROG) mode, controller passwords,
   disable unused services (web servers on PLCs), firmware signing where supported.
6. **Patching:** risk-based; vendor-qualified patches during outages; compensating controls
   (isolation, allowlisting, IPS virtual patching) for unpatchable systems.
7. **Monitoring:** OT-aware network detection (Dragos, Claroty, Nozomi, Defender for IoT):
   new devices, new flows, PLC program downloads, mode changes, firmware updates. Feed OT alerts
   to a SOC with OT playbooks.
8. **Recovery:** offline backups of PLC programs, HMI projects and configurations; tested
   restoration; manual operation procedures.

## IR considerations
OT incident playbooks agreed with operations: who can isolate what, when to shut down
safely, how to preserve evidence without disrupting control.

## Gotchas
- Active vulnerability scanning can crash PLCs; use passive methods or vendor-approved tools
  in maintenance windows.
- IT antivirus on HMIs without vendor approval can break the application.
- Shared accounts on HMIs are common; at minimum, log physical and logical access.

## Verify
Architecture review against the flow baseline: no direct IT-to-L2 paths, EWS access logged,
PLC backups restorable (tested in a lab), OT monitoring alerts on a test program download.
