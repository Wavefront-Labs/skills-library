---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.autosar-software-component-export
name: autosar-software-component-export
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [autosar-blockset, autosar, swc, arxml, runnable, rte, embedded-coder]
level: practitioner
status: verified
description: "Map a Simulink model to an AUTOSAR software component: runnables, ports, data types and ARXML export, and check integration with the RTE."
sources:
  - "AUTOSAR Blockset: Code Mappings editor (https://www.mathworks.com/help/autosar/ref/autosarcodemappingseditor.html)"
  - "AUTOSAR Blockset: Configure AUTOSAR code generation and ARXML packaging (https://au.mathworks.com/help/autosar/ug/generating-autosar-code-and-description-files.html)"
  - "AUTOSAR Blockset: Model AUTOSAR communication (https://www.mathworks.com/help/autosar/ug/autosar-communication.html)"
  - "AUTOSAR specifications (https://www.autosar.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Export AUTOSAR software components

1. Partition: one Simulink model per atomic software component; each function-call subsystem or rate becomes a **runnable**.
2. Interfaces: model I/O as sender-receiver ports (data elements with AUTOSAR types) or client-server operations; map to AUTOSAR data types and units.
3. Configure the AUTOSAR code interface (Classic Platform; check the release notes for Adaptive support) and open the Code Mappings editor to map entry-point functions to runnables, inports/outports to sender-receiver ports and function callers to client-server ports and operations, and parameters to component parameters.
4. Generate code and ARXML (Share > Generate Code and ARXML). Modular packaging writes `<model>_component.arxml` (ports, events, runnables, inter-runnable variables), `_datatype`, `_interface`, `_implementation` (code descriptors) and, for multi-runnable models only, `_timing`; single-file packaging writes one `<model>.arxml`. Import into the system or ECU configuration tool.
5. Test with the RTE stub or the production RTE in SIL.
6. Keep timing events consistent with the OS task mapping.

**Gotchas:** data type name mismatches between the SWC and the system description; mismatched data access modes between ports and the system description.

## Verify
- [ ] ARXML validates in the integration tool without errors.
- [ ] Each runnable's period matches the OS task.
