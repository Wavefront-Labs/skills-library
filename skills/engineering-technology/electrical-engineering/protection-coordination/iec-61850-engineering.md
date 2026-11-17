---
id: engineering-technology.electrical-engineering.protection-coordination.iec-61850-engineering
name: iec-61850-engineering
category: engineering-technology
field: electrical-engineering
product: protection-coordination
tags: [electrical-engineering, goose, goose-performance-testing, iec-61850, iec-61850-engineering, mms, protection-coordination, sampled-values, scl, scl-file-engineering]
level: advanced
status: draft
description: "Engineer IEC 61850 substation automation: SCL files, GOOSE messages and performance testing."
sources:
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# IEC 61850 engineering

1. **Data model:** logical devices contain logical nodes (for example XCBR for a breaker, PTOC for overcurrent) with data objects and attributes.
2. **SCL files:** engineering uses XML files (SSD system specification, ICD IED capability, CID configured IED, SCD system configuration); manage versions in a configuration tool and exchange via SCD.
3. **Services:** MMS client-server (reporting, control), GOOSE (multicast event messaging on layer 2), Sampled Values (IEC 61869-9 / 9-2LE profile) for process bus.
4. **GOOSE design:** assign appID, VLAN and priority, confirm subscribers; peer-to-peer trips typically target transfer times of a few milliseconds (Class P2/P3 performance in the standard); supervise via the message state number and time-allowed-to-live.
5. **Network:** use switched Ethernet with redundancy (PRP/HSR per IEC 62439-3) and time synchronisation (PTP or IRIG-B).
6. **Testing:** with a protocol simulator, verify publishing/subscribing and measure end-to-end transfer times; test failure of the network and loss of messages.
7. Maintain cyber-security measures (IEC 62351 principles, segmentation, access control) as a defensive baseline.

**Verify:** prove GOOSE interlocks and trips with a test set before the breaker is energised.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
