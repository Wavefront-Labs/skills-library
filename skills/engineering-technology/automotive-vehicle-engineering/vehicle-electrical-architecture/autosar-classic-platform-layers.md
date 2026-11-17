---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.autosar-classic-platform-layers
name: autosar-classic-platform-layers
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [autosar-classic, autosar, basic-software, rte, mcal, bsw, ecu-configuration]
level: practitioner
status: gated
description: "Understand AUTOSAR Classic layers: application SWCs, RTE, basic software stacks and MCAL, the configuration workflow and where integration problems arise."
sources:
  - "AUTOSAR Layered Software Architecture, R22-11 (https://www.autosar.org/fileadmin/standards/R22-11/CP/AUTOSAR_EXP_LayeredSoftwareArchitecture.pdf)"
  - "AUTOSAR Specification of Operating System, R22-11 (https://www.autosar.org/fileadmin/standards/R22-11/CP/AUTOSAR_SWS_OS.pdf)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# AUTOSAR Classic platform layers

1. **Application layer:** software components (SWCs) with ports and runnables, independent of hardware.
2. **RTE (runtime environment):** generated middleware implementing port communication between SWCs and between SWCs and basic software, per the configuration.
3. **Basic software (BSW):** services layer (OS, diagnostics Dcm/Dem, communication services Com/PduR, memory services NvM, mode management), ECU abstraction layer (I/O, communication and memory hardware abstraction), microcontroller abstraction layer (MCAL: drivers for ADC, CAN, SPI, PWM, GPT, watchdog), and complex device drivers for timing-critical hardware.
4. **OS:** the AUTOSAR OS specification extends OSEK OS (it lists restrictions and extensions to OSEK OS) and includes memory protection and timing protection chapters for mixed-criticality.
5. Workflow: system description (ARXML) from the vehicle-level tool -> ECU extract -> BSW configuration in the vendor tool (vendor tool names vary; confirm in your project (gated: unconfirmed, source is paywalled or blocked)) -> RTE and BSW generation -> integrate SWC code -> compile and link -> flash.
6. Roles: OEM defines system and SWCs; Tier 1 integrates BSW; MCAL typically comes from the microcontroller vendor (gated: unconfirmed, source is paywalled or blocked).
7. Typical issues: version mismatches between BSW and MCAL, wrong timing configuration, memory mapping, and unresolved ports.

**Gotchas:** upgrading a release means re-validating generated code and the configuration.

## Verify
- [ ] ECU configuration validates without errors in the tool; generated code compiles with the target toolchain.
- [ ] Timing and stack usage analysis completed on the integrated build.
