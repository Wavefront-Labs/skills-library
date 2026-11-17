---
id: computing-software.cybersecurity-defensive.threat-modelling.ics-threat-modelling
name: ics-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [ics-threat-modelling, ot-security, purdue-model, nist-800-82, scada]
level: advanced
status: docs-checked
description: "Threat model industrial control systems using NIST SP 800-82r3: segment by Purdue level or zone, DMZ and firewall rules, safety systems, passive monitoring."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ICS threat modelling

Source: NIST SP 800-82r3, Guide to Operational Technology (OT) Security (September 2023).
Many OT-controlled physical processes can create hazardous situations for human life,
property and the environment, so the model must account for the safety systems that bring the
process to a safe state.

## System model
- Characterise, segment and isolate IT and OT devices. Segment by management authority, level
  of trust, functional criticality, data flow, location or other logical combinations.
- Use an industry-recognised model to organise segments: the Purdue model, ISA-95 levels, the
  three-tier IIoT architecture, or a combination. A DMZ can serve as an enforcement boundary
  between segments (Fig. 16).
- Grouping components into levels, tiers or zones comes before applying isolation devices.
  Consider how the zone layout affects day-to-day operations, safety and response.
- Use mapped data flows to find the required communications, then permit only those.
- Field I/O is Purdue Level 0 (section 5.3.6 covers its security considerations).
- Control and fieldbus networks often use standard protocols such as Modbus and Fieldbus.

## Safety systems in the model
- Safety systems (emergency shut down, process safety shutdown, fire and gas systems) reduce
  the likelihood or consequence of hazards by bringing the system to a safe state.
- A safety instrumented system (SIS) is made of safety instrumented functions: sensors, logic
  solvers and final control elements that act when thresholds are violated. It is designed per
  IEC 61511 and is often independent of the basic process control system, so a BPCS failure
  does not impair the SIS.
- Model whether that independence actually holds in the system under review.

## Boundary rules to check
- Firewall rules should permit connections only between adjacent levels, tiers or zones. In a
  Purdue layout, prevent Level 4 devices from communicating directly with Levels 2, 1 or 0.
- Outbound traffic from the control network varies in practice and can be a significant risk if
  unmanaged; consider outbound rules as strict as inbound.
- A unidirectional gateway or data diode is an alternative to a firewall. Deployed between
  layers 2 and 3 it may protect layers 0 to 2 from an event at layers 3 to 5.

## Monitoring and scanning
- Understand the normal state of the OT network before network security monitoring; a passive
  (listen or learning) mode is a possible first step.
- Some IDS/IPS products include signatures for OT protocols such as Modbus, DNP3 and ICCP.
- Encrypted traffic can blind a network IDS; capturing before or after encryption (host-based
  tools) can help.
- Solutions that actively scan or use local resources should be tested before deployment into
  the OT system. A passive network monitor might detect vulnerable network services without
  scanning the devices.

## Verify
- [ ] Every asset sits in a named level, tier or zone, with required data flows listed.
- [ ] No path lets Level 4 reach Levels 0 to 2 directly; outbound rules are reviewed.
- [ ] The SIS independence from the BPCS has been checked, not assumed.

## Checked
Confirmed 2026-11-09 against NIST SP 800-82r3 (pdftotext): section 5.2.3.1 network architecture, the safety systems passage, section 5.2 monitoring recommendations, the continuous monitoring passage, and the protocol mentions.
Removed as unconfirmed: the Purdue level-by-level device list, IEC 62443-3-2 zones, conduits and SL 1-4 targets, the protocol list beyond Modbus, DNP3, ICCP and Fieldbus, the consequence-driven (INL CCE) procedure, ATT&CK for ICS tactic mappings, historic incidents (Ukraine, Industroyer, Triton), the typical-controls list (MFA vendor access, PLC key switch, offline backups), and the MITRE, INL and ISA sources, which are unreadable hosts.
Method: docs-checked 2026-11-09 against NIST SP 800-82r3 PDF via pdftotext
