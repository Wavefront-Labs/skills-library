---
id: computing-software.systems-network-administration.patch-management.hardware-end-of-service-life
name: hardware-end-of-service-life
category: computing-software
field: systems-network-administration
product: patch-management
tags: [eosl, hardware-eol, end-of-support, hardware-lifecycle, eol-software, patch-management]
level: practitioner
status: draft
description: "Manage hardware end of sale and end of service life: track vendor EoL/EOSL dates, firmware patch end, third-party maintenance options and replacement planning."
sources:
  - https://www.cisco.com/c/en/us/products/eos-eol-policy.html
  - https://www.dell.com/support/kbdoc/en-us/000136213/dell-emc-product-support-lifecycle-policy
  - https://support.hpe.com/hpesc/public/docDisplay?docId=a00026864en_us
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardware end of service life

Hardware EOL ends **firmware and BIOS security fixes** (BMC, CPU microcode packaging, NIC/HBA firmware), not just break/fix support. A server with an unpatchable BMC is a vulnerability you cannot remediate.

## Milestones (Cisco terms; others similar)
| Milestone | Meaning |
|---|---|
| End-of-Sale announcement | dates published |
| End of Sale (EoS) | cannot buy |
| End of SW Maintenance | no more bug-fix releases |
| End of Vulnerability/Security Support | no more security fixes |
| Last Date of Support (LDoS / EOSL) | no TAC, no RMA |

## Track
- Pull serials and models from inventory (Redfish/iDRAC/iLO/XClarity, Cisco `show inventory`, DCIM).
- Vendor APIs: Cisco Support APIs (EoX by serial/PID), Dell TechDirect warranty API, HPE/Lenovo warranty lookups.
- Store EoS/End-of-security/LDoS in CMDB per asset; report 24/12/6-month horizons.

## Options as dates approach
1. Replace (preferred for internet-facing or security-critical gear: firewalls, VPN, BMC-exposed servers).
2. Third-party maintenance (TPM) for parts and break/fix; it does **not** provide security firmware.
3. Isolate: management interfaces on a restricted VLAN, disable unused services, monitor; record risk.
4. Repurpose to non-production with documented acceptance.

## Gotchas
- Component EOL (RAID controller, NIC) can come before chassis EOL.
- Vendors sometimes publish one last firmware after LDoS for critical issues; do not count on it.
- Lease/refresh cycles slip; tie refresh budget to EOSL report, not depreciation alone.

## Verify
No production asset past end-of-security-support without a risk register entry; 12-month horizon list has funded replacement projects.
