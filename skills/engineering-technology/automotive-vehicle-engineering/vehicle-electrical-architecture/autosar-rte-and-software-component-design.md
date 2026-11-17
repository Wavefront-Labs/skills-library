---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.autosar-rte-and-software-component-design
name: autosar-rte-and-software-component-design
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [autosar-swc, swc, rte, runnable, sender-receiver, client-server, port-interface, arxml, implicit-access, inter-runnable-variable, autosar-classic, software-component]
level: practitioner
status: gated
description: "Design AUTOSAR Classic software components: ports and interfaces, runnables and RTE events, data consistency, composition, mapping to tasks, and generator workflow."
sources:
  - "AUTOSAR Specification of RTE, R22-11 (https://www.autosar.org/fileadmin/standards/R22-11/CP/AUTOSAR_SWS_RTE.pdf)"
  - "AUTOSAR Specification of Operating System, R22-11 (https://www.autosar.org/fileadmin/standards/R22-11/CP/AUTOSAR_SWS_OS.pdf)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# RTE and software component design (AUTOSAR Classic)

## 1. Concept
Application software is split into software components (SWCs) with ports defining their interfaces; the Runtime Environment (RTE), generated per ECU, connects components to each other and to the Basic Software, hiding the physical location (same ECU or other ECU via communication stack).

## 2. Component types and ports
- **Application SWC:** pure logic, no hardware dependency.
- **Sensor/actuator SWC:** connects to hardware abstraction.
- **ECU abstraction and service components** from the Basic Software.
- **Composition:** group of SWCs wired together, used for hierarchy.
Port interfaces: sender-receiver (data), client-server (operation call), mode-switch (mode ports), nv-data, parameter (calibration data), trigger. Define data types (implementation data types with base types) and units/ranges in the data type description, not in code comments.

## 3. Runnables and events
A runnable is a function that the RTE schedules in an OS task according to RTE events: TimingEvent (periodic), DataReceivedEvent, OperationInvokedEvent, ModeSwitchEvent, InitEvent. Use as few distinct rates as practical (for example 5, 10, 20, 100 ms) and map runnables to OS tasks accordingly. Inter-runnable variables carry data within a component between runnables of different tasks safely.

## 4. Data consistency
Choose implicit (buffered at start/end of the runnable, consistent snapshots, more memory and copying) or explicit access (direct API calls, immediate). Define exclusive areas or use implicit to avoid races between preemptible tasks. Check that read-modify-write sequences across tasks are protected.

## 5. Design guidelines
- Keep SWCs small and cohesive; stable interfaces; no direct access to Basic Software drivers.
- Avoid blocking (client-server synchronous calls across ECUs need timeouts and are often better as asynchronous).
- Use mode management (BswM, mode ports) rather than ad hoc state sharing.
- Document timing: period, deadline, worst-case execution time per runnable.
- Keep behaviour model-based (Simulink or hand code) and test the component stand-alone (virtual ECU).

## 6. Workflow
Model in an AUTOSAR authoring tool (vendor authoring tools, or ARXML exported from a modelling tool; tool names unconfirmed (gated: unconfirmed, source is paywalled or blocked)), import ARXML into the BSW configuration tool, generate RTE and BSW, build with OS configuration (OSEK/AUTOSAR OS), analyse timing, flash. Review RTE generator warnings seriously.

## Verify
- [ ] Interfaces typed with units and ranges; versions controlled.
- [ ] Runnable-to-task mapping and WCET documented.
- [ ] Data access mode chosen and race conditions reviewed.
- [ ] SWC tested stand-alone and integrated via RTE.
