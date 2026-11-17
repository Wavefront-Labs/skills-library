---
id: engineering-technology.biomedical-engineering.medical-device-design.device-cybersecurity
name: device-cybersecurity
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [device-cybersecurity, medical-device-software, samd, threat-modeling, sbom, secure-boot, vulnerability-disclosure, iec-81001-5-1]
level: advanced
status: gated
description: "Build cybersecurity into the device lifecycle: threat modelling, security risk, SBOM, secure update, vulnerability management and links to safety risk per FDA and EU guidance."
sources: ["https://www.law.cornell.edu/uscode/text/21/360n-2","https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-management-system-considerations-and-content-premarket"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Medical device cybersecurity

**Goal:** a device whose security risks are analysed, controlled and maintained through its life, with those risks linked to patient safety.

Regulatory expectations change; confirm current FDA, EU and other guidance. This note is practice guidance, not legal advice.

## Lifecycle
1. **Security risk management** parallel to ISO 14971: identify assets, threats and vulnerabilities, and the effect on safety and essential performance. Use a threat model (for example STRIDE on a data-flow diagram) and document attack surfaces: network ports, USB, Bluetooth, cloud APIs, update channels, service tools.
2. **Security requirements:** authentication and authorisation (including no shared default passwords), encryption in transit (TLS) and at rest where needed, signed and verified firmware (secure boot), logging and audit, least privilege, input validation, and safe behaviour on failure.
3. **Architecture:** segregation of safety-critical functions, minimal services, hardened OS images, and trusted time sources.
4. **SBOM:** a machine-readable list of all software components with versions and suppliers (SPDX or CycloneDX); section 524B(b)(3) of the FD&C Act (21 USC 360n-2) requires premarket submissions for cyber devices to include an SBOM covering commercial, open-source and off-the-shelf components (text checked at law.cornell.edu). FDA's guidance is titled 'Cybersecurity in Medical Devices: Quality Management System Considerations and Content of Premarket Submissions' (final, February 2026, superseding the June 2025 'Quality System Considerations' version; fda.gov page). SPDX and CycloneDX are commonly used formats (confirm which FDA accepts (gated: unconfirmed, source is paywalled or blocked)).
5. **Verification:** security testing: static analysis, dependency scanning, fuzzing, penetration testing by independent testers, and verification of each security control.
6. **Post-market:** a coordinated vulnerability disclosure policy, monitoring of CVEs for components, defined timelines for assessment and patch (for example critical fixes in a short period), secure update mechanism, and customer communications; plan the end-of-support date.
7. **Information to users:** security instructions, network requirements, recommended configurations and decommissioning guidance.

## Gotchas
- Treating security as a late penetration test.
- Update mechanisms that are insecure or impossible in the field.
- Unsupported operating systems in long-lived devices.
- Shared credentials for service access.

## Verify
- [ ] Threat model and security risk file linked to safety hazards.
- [ ] SBOM generated from the actual build.
- [ ] Penetration test findings closed or risk-accepted with rationale.
