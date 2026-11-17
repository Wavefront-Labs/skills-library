---
id: computing-software.cybersecurity-defensive.system-hardening.intel-amt-me-management
name: intel-amt-me-management
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [intel-amt, intel-me, csme, vpro, firmware-security, out-of-band-management]
level: advanced
status: draft
description: "Manage Intel AMT and the Management Engine securely: find provisioned devices, disable or provision AMT with strong credentials and TLS, patch CSME firmware, and monitor ports."
sources: ["https://www.intel.com/content/www/us/en/security-center/default.html", "https://www.intel.com/content/www/us/en/developer/topic-technology/edge-5g/hardware/vpro-platform-retail.html", "https://github.com/intel/lms", "https://www.intel.com/content/www/us/en/support/articles/000025619/software.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intel AMT and ME management

Intel vPro machines contain the Converged Security and Management Engine (CSME), an independent processor with
its own firmware. **Active Management Technology (AMT)** runs on it and offers remote power control, KVM and
storage redirection over the network, below the OS, even when the machine is off. Unprovisioned, misprovisioned
or unpatched AMT is a powerful backdoor (e.g. INTEL-SA-00075, 2017, authentication bypass of the AMT web UI).

## Decide per fleet
- **Not using AMT**: ensure it is unprovisioned and disabled in BIOS (MEBx / "Intel AMT" setting off), or
  ordered from the OEM with AMT disabled. Still patch CSME firmware (ME vulnerabilities exist beyond AMT).
- **Using AMT** (remote support, out-of-band recovery): provision deliberately in Admin Control Mode with
  strong credentials and TLS via a management server (Intel EMA, Configuration Manager integrations, or open
  source Open AMT Cloud Toolkit).

## Discover state
- Network: AMT listens on TCP 16992 (HTTP), 16993 (HTTPS), 16994/16995 (redirection), 623/664 (WS-MAN/ASF).
  Scan internal ranges for these ports to find provisioned devices.
- On the host: Intel CSME Version Detection Tool / `MEInfo` (OEM packages) shows firmware version and AMT state;
  Windows LMS service presence; vendor inventory (Dell Command, HP, Lenovo).

## If provisioned
- Unique, strong AMT admin password per device (MEBx default `admin` must be changed at provisioning),
  stored in the management server.
- TLS (port 16993) with certificates; disable non-TLS 16992.
- Admin Control Mode vs Client Control Mode: CCM requires user consent for KVM; keep user consent for KVM where
  appropriate.
- Restrict network access to AMT ports to management servers via network ACLs; Intel's CIRA (client-initiated
  remote access) can tunnel through the internet to your MPS - secure that server.
- Audit log in AMT and management server logs to SIEM.

## Patch CSME firmware
CSME and AMT fixes come through **OEM BIOS/firmware packages**, not Windows Update alone. Track Intel Security
Center advisories (INTEL-SA-xxxxx) and OEM bulletins; include firmware in patch management with version
reporting.

## Gotchas
- The HECI/MEI driver and LMS service let local admin software interact with ME; LMS being installed does not
  mean AMT is provisioned, but local-provisioning attacks have existed.
- "Disabled" in OS-level tools may not equal disabled in firmware; verify in MEBx/BIOS.
- Fully disabling the ME is not supported by Intel; the "HAP bit" approach is for specialists.

## Verify
Network scan finds AMT ports only on intentionally provisioned devices; those use TLS and non-default
credentials; CSME firmware versions across the fleet are at or above the latest advisory fixed versions.
