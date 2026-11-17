---
id: computing-software.it-support-helpdesk.remote-support-tools.rmm-policy-hierarchy-backup-monitoring-and-amt
name: rmm-policy-hierarchy-backup-monitoring-and-amt
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, rmm-policy-hierarchy, backup-monitoring, intel-amt, rmm, out-of-band-management, vpro]
level: practitioner
status: draft
description: "Structure RMM sites, groups and policy inheritance, monitor backup jobs through the RMM, and use Intel AMT/vPro out-of-band access when the OS won't boot."
sources:
  - "https://www.intel.com/content/www/us/en/support/articles/000055532/technologies.html"
  - "https://www.intel.com/content/www/us/en/architecture-and-technology/vpro/manageability.html"
  - "https://learn.microsoft.com/en-us/mem/configmgr/core/clients/manage/manage-intel-amt-based-computers"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# rmm-policy-hierarchy-backup-monitoring-and-amt

## Policy hierarchy in an RMM
Most RMMs (NinjaOne, Datto RMM, N-able, ConnectWise Automate) follow the same shape:
- **Organisation / client > site > device group > device**. Policies attach at levels
  and inherit downward; a lower-level policy overrides specific settings.
- Design: one **global baseline** per device role (workstation, server, laptop), then
  site-level overrides only for genuine differences (patch window per time zone, a
  site without backup).
- Keep override count low; document every override with a reason. Audit quarterly:
  devices with device-level overrides are where surprises live.
- Patch policies, monitors, scripts and AV settings should each be in role policies, not
  copied per client.
- Test policy changes on a pilot group or test site before promoting.

## Backup monitoring through RMM
- Monitor: last successful backup age (alert if over 24-48 h for servers, per policy for
  endpoints), job failures, backup agent service down, and storage/quota warnings.
- Sources: backup product integration in the RMM, Windows event log monitors (e.g.
  Veeam, Windows Server Backup event IDs), or scripts reading the agent's status.
- Alerts become tickets with the job name, last success time, and error; failed backups
  for 2 consecutive runs escalate.
- Monthly: report coverage (devices that should be backed up vs devices with a recent
  successful backup). Monitoring that only alerts on failures misses devices with no job.

## Intel AMT / vPro out-of-band
- AMT runs in the chipset's management engine: remote power on/off/reset, KVM remote
  control from BIOS onwards, IDE-redirect/USB-redirect boot media, even when the OS is
  down. Only on vPro-capable business models.
- Provisioning: activate AMT in Admin Control Mode (certificate-based, via Intel EMA or
  a supported RMM/ConfigMgr integration) or Client Control Mode (user consent required
  for KVM). Unprovisioned AMT does nothing.
- Use: boot to BIOS to change settings, watch a boot loop, mount a recovery ISO, power on
  for patching.
- Security: AMT admin credentials must be unique and stored in the vault; restrict AMT
  network ports (16992-16995) to management networks; keep ME firmware patched.

## Verify
No device has unexplained overrides; the backup coverage report shows every in-scope
device with a recent success; an AMT-provisioned test device can be power-cycled and
viewed in BIOS remotely.
