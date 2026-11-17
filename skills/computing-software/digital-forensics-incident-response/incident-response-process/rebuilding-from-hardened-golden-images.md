---
id: computing-software.digital-forensics-incident-response.incident-response-process.rebuilding-from-hardened-golden-images
name: rebuilding-from-hardened-golden-images
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [golden-image, rebuild, recovery, hardening, dfir]
level: practitioner
status: draft
description: "Rebuild compromised systems from hardened golden images: verifying image provenance, patch level, baked-in agents, clean credentials and data restore without reinfection."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://www.cisecurity.org/cis-hardened-images", "https://www.cisa.gov/stopransomware/ransomware-guide", "https://learn.microsoft.com/en-us/security/ransomware/human-operated-ransomware"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rebuilding from hardened golden images

Rebuild beats clean when you cannot be sure you found everything. It only works if the image itself is trustworthy and the rebuild does not reintroduce the attacker through restored data or reused credentials.

## Before using an image
- **Provenance**: the image and its build pipeline (Packer templates, MDT/SCCM task sequences, AMIs) were not reachable by the attacker. If the build server or image repository was in scope, rebuild the pipeline first.
- **Integrity**: compare image hashes with the recorded release hash; for cloud images check the AMI/Image ID against the approved list and owner account.
- **Patch level**: patch the image for the exploited vulnerability before deployment, not after.
- **Hardening**: CIS benchmark or internal baseline applied; local admin password unique (Windows LAPS), unnecessary services off.
- **Agents baked in**: EDR, log forwarding (Sysmon config), backup agent, enrolled automatically so the host is visible from first boot.

## Rebuild procedure
1. Wipe or replace the disk (preserve the old disk image as evidence first if needed).
2. Deploy the image onto a clean network segment (staging VLAN) not reachable from still-compromised zones.
3. Join domain only after domain trust is restored (krbtgt reset, tier-0 clean); use new machine accounts.
4. Restore data, not binaries: application data from backups taken before the earliest compromise date, scanned with current AV/YARA. Reinstall applications from vendor media.
5. Re-issue secrets: new service-account passwords, certificates, API keys; never restore old credential stores.
6. Validate with the service owner, then move to production with heightened monitoring.

## Gotchas
- Restoring a full system-state backup brings back persistence; restore files selectively.
- Configuration management (Ansible, GPO, Intune) that the attacker modified will re-apply their changes; review it before rebuilt hosts pull config.
- Track rebuilt vs not-yet-rebuilt hosts on the incident asset list; mixed states cause re-infection.

## Verify
Rebuilt host shows the expected image version, EDR checked in from first boot, and an IOC sweep on it returns clean.
