---
id: computing-software.systems-network-administration.patch-management.patching-air-gapped-networks
name: patching-air-gapped-networks
category: computing-software
field: systems-network-administration
product: patch-management
tags: [air-gapped-patching, offline-patching, disconnected-network, wsus-export, reposync, data-transfer, patch-acquisition]
level: advanced
status: draft
description: "Patch air-gapped networks: build update bundles on a connected side (WSUS export, reposync, aptly snapshots), move them through controlled media transfer, verify and import."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/manage/wsus-messages-and-troubleshooting-tips
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/plan/plan-your-wsus-deployment
  - https://docs.redhat.com/en/documentation/red_hat_satellite/6.15/html/installing_satellite_server_in_a_disconnected_network_environment/index
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Patching air-gapped networks

**Goal:** keep isolated networks on the same patch cadence as connected ones, with a defensible transfer process.

## Architecture
Connected "low side" staging server mirrors vendor content; content crosses on controlled media (or a one-way data diode); "high side" server serves clients. Same products/classifications both sides.

## Windows (WSUS export/import)
Low side:
```cmd
"%ProgramFiles%\Update Services\Tools\wsusutil.exe" export export.xml.gz export.log
robocopy <WSUS_DIR>\WsusContent <TRANSFER_MEDIA>\WsusContent /MIR
```
High side (identical WSUS version, same language/product settings, "Store update files locally" with express settings matching):
```cmd
robocopy <TRANSFER_MEDIA>\WsusContent <WSUS_DIR>\WsusContent /E
wsusutil.exe import export.xml.gz import.log
```
Metadata import does not carry approvals; approve on the high side.

## Linux
```bash
# low side
dnf reposync --repoid=rhel-9-for-x86_64-baseos-rpms --download-metadata -p /transfer/repos
# or aptly: aptly mirror update ubuntu-jammy-security && aptly snapshot create sec-2026-10 from mirror ubuntu-jammy-security
```
High side: serve the directory over HTTP; clients point to it. For Satellite, use disconnected Satellite with content export/import (`hammer content-export complete version`, `hammer content-import version`).

## Transfer controls
- Write-once media where possible; scan media on a dedicated kiosk before the high side.
- Generate a SHA-256 manifest on the low side; verify it on the high side (`sha256sum -c manifest.sha256`).
- Log every transfer: date, media ID, contents, operator, approver.

## Gotchas
- Defender/AV definition updates need their own frequent channel (daily) separate from monthly OS bundles.
- Skipping a month means the next transfer must include superseding cumulative updates only; keep bundles self-contained.

## Verify
High-side compliance report matches the low-side baseline for the same month within the agreed lag.
