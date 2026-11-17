---
id: computing-software.systems-network-administration.patch-management.lenovo-xclarity-firmware-updates
name: lenovo-xclarity-firmware-updates
category: computing-software
field: systems-network-administration
product: patch-management
tags: [xclarity-administrator-updates, lenovo-xclarity, xcc, firmware-patching, onecli, patch-management]
level: practitioner
status: gated
description: "Update Lenovo ThinkSystem firmware with XClarity Administrator compliance policies, repository packs and OneCLI, including XCC/UEFI order, staging and verification."
sources:
  - https://pubs.lenovo.com/lxca/update_fw
  - https://pubs.lenovo.com/lxce-onecli/
  - https://pubs.lenovo.com/xcc2/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Lenovo XClarity firmware updates

## Tools
- **XClarity Administrator (LXCA)**: central appliance; firmware repository, compliance policies, apply updates to many servers.
- **XClarity Controller (XCC/XCC2)**: per-server BMC (web UI and Redfish).
- **XClarity Essentials OneCLI**: scriptable updates in-band (from the OS) or out-of-band (via XCC).

## LXCA workflow
1. Firmware Updates: Repository page: refresh the catalog, then download or import update packages, repository packs and **UpdateXpress System Packs (UXSP)** (firmware and drivers by operating system). Downloading a UXSP creates a default firmware-compliance policy named like `{uxsp-version}-{date}-{server-short-name}-UXSP`.
2. Create or copy a **firmware compliance policy** and assign it to servers.
3. Apply: choose immediate activation (restarts the device as part of the update) or delayed activation (restart in a later maintenance window). Updates to CMMs and Flex switches are always activated immediately.
4. Watch Jobs; then the compliance column shows Compliant.

## OneCLI
OneCLI is Lenovo's consolidated command-line tool for managing Lenovo systems. Take the exact `update` and `inventory` command syntax, in-band and out-of-band options from the OneCLI documentation for your version; never put passwords on a shared command line.

## Order and staging
- Follow the update order in the package readme; UXSP packages group firmware and drivers released together.
- Devices must be restarted to activate firmware updates (see activation modes above).
- Use vendor cluster patterns: evacuate VMs or fail over before activation.

## Gotchas
- Read each package readme for prerequisites and intermediate versions.
- Manage repository storage: remove update packages you no longer need.
- Mixing OS-level driver versions with new adapter firmware: update drivers in the same window per the UXSP.

## Verify
LXCA compliance shows Compliant for the assigned policy; OneCLI inventory output or the XCC firmware listing shows the expected versions (gated: unconfirmed, source is paywalled or blocked); no new hardware errors after reboot.

## Checked
Date: 2026-10-27. Documentation: Lenovo XClarity Administrator "Updating firmware" page (repository, repository packs, UXSP, default compliance policy naming, immediate versus delayed activation) and the OneCLI documentation home. The OneCLI command syntax and the update order could not be confirmed, so they were replaced with pointers to the documentation; one residual claim (XCC listing firmware on its Firmware page) (gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
