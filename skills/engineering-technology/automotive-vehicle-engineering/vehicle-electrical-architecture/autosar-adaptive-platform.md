---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.autosar-adaptive-platform
name: autosar-adaptive-platform
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [autosar-adaptive, adaptive-platform, ara-com, execution-management, manifest, posix, cpp14, service-oriented, high-performance-compute, update-configuration-management, autosar]
level: practitioner
status: gated
description: "Use the AUTOSAR Adaptive Platform: where it fits versus Classic, functional clusters, C++ applications, manifests, service communication, update and diagnostics."
sources:
  - "AUTOSAR specifications overview (https://www.autosar.org); confirm release and documents there"
  - "AUTOSAR Adaptive Platform specification overview; confirm current release names and documents at https://www.autosar.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# AUTOSAR Adaptive Platform

## 1. Where it fits
The Classic Platform targets deeply embedded ECUs with static configuration and hard real-time behaviour. The Adaptive Platform targets high-performance computers (ADAS, central compute, connected services) with POSIX operating systems, dynamic deployment, service-oriented communication and software updates during the vehicle's life. Both coexist in a vehicle and talk over Ethernet using SOME/IP (see service-oriented architecture). Release naming, content and safety support change by release; confirm the current release before planning.

## 2. Main parts (functional clusters)
- **Execution Management:** starts and stops applications (processes) according to manifest and machine state.
- **Communication Management (ara::com):** service-oriented communication, SOME/IP binding and others; generated proxies and skeletons.
- **Diagnostics, Persistency, Logging and Tracing, Time, Cryptography, Identity and Access Management, Update and Configuration Management, Network Management, Platform Health Management.**
- **Operating system interface:** POSIX-based; autosar.org (fetched) recommends the PSE51 profile (POSIX threads, priority scheduling, synchronisation; no complex memory management) for safety-relevant real-time systems; C++ standard library requirements per release.

## 3. Applications and manifests
Applications are C++ executables using the ara APIs. Deployment information lives in manifests (ARXML): application manifest, execution manifest (process start, resources, dependencies), service instance manifest (network bindings), machine manifest. Changing manifests allows updating and reconfiguration without reflashing the whole platform.

## 4. Process
1. Model service interfaces and applications (ARXML or modelling tools).
2. Generate proxy/skeleton code, write application logic in C++ (follow the AUTOSAR C++ coding guidelines; reported to be merged into MISRA C++ (gated: unconfirmed, source is paywalled or blocked), so check which applies).
3. Create manifests, integrate into the machine image, test on target hardware or a virtual machine.
4. Integrate with Classic ECUs through SOME/IP gateways; configure security (certificates, access control).

## 5. Pitfalls
Nondeterministic timing from Linux scheduling and shared caches: use real-time scheduling, core isolation, and measure latency; functional safety support depends on platform release and OS (a separate safety-certified OS or hypervisor partition may be needed); memory and dynamic allocation after startup; platform version compatibility with tools.

## Verify
- [ ] Release and safety capability of the platform checked for the target ASIL.
- [ ] Manifests validated and tested for start, restart and failure of each process.
- [ ] Timing measured on target hardware with realistic load.
- [ ] Security configuration (identity, access, crypto) defined.
