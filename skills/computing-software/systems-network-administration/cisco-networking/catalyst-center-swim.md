---
id: computing-software.systems-network-administration.cisco-networking.catalyst-center-swim
name: catalyst-center-swim
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst-center, dnac, swim, software-image-management, golden-image, image-distribution, image-activation, upgrade-readiness]
level: practitioner
status: draft
description: "Upgrade devices with Catalyst Center SWIM: importing images, marking golden per family/role, readiness checks, distribution and activation, and failure handling."
sources:
  - https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/catalyst-center/2-3-7/user_guide/b_cisco_catalyst_center_user_guide_237/b_cisco_dna_center_ug_2_3_7_chapter_0100.html
  - https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/catalyst-center/2-3-7/user_guide/b_cisco_catalyst_center_user_guide_237.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SWIM image management in Catalyst Center

## Flow
1. **Import** (Design > Image Repository): from cisco.com (CCO account linked), URL, or local file.
   Catalyst Center verifies the image checksum.
2. **Golden image**: mark the image golden per device family, per site, optionally per device role
   (access/distribution/core). Devices not on golden show "Outdated".
3. **Readiness checks** (Provision > Inventory > Software Images): flash space, config register,
   startup config, install mode, CDP/LLDP neighbours, service entitlement, NTP; failing checks block update.
4. **Distribute**: copy image to devices (HTTPS/SCP/SFTP from Catalyst Center or a distribution server).
   Can be scheduled ahead.
5. **Activate**: install/reload in a maintenance window; optionally run distribution and activation together.
6. Post-checks: device reachability, version, and optional custom CLI checks.

## Practices
- Use **add-on images (SMUs)** and subpackages where supported for hotfixes.
- Pre-stage distribution days before; activate in a window with a rollback plan.
- Stacks and StackWise Virtual: Catalyst Center handles install mode; bundle-mode devices may need conversion first.
- Upgrade path constraints (ROMMON, FPGA, intermediate releases) are not always automated: read release notes.
- Use tags/sites to batch upgrades (pilot site first).

## Failures
| Symptom | Check |
|---|---|
| Distribution fails | device can reach Catalyst Center on HTTPS, flash free space, `ip http client source-interface` |
| Activation fails | install state on device (`show install summary`), leftover uncommitted install, boot variable |
| Device unreachable after reload | console; boot variable / ROMMON compatibility |

## Verify
- [ ] Inventory "Software Image" column shows golden version and Compliant for the batch.
- [ ] `show install summary` committed on each device.
