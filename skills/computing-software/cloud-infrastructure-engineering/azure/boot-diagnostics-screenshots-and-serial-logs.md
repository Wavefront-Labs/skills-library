---
id: computing-software.cloud-infrastructure-engineering.azure.boot-diagnostics-screenshots-and-serial-logs
name: boot-diagnostics-screenshots-and-serial-logs
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, boot-diagnostics, boot-screenshot, boot-log, boot-diagnostics-storage, vm-troubleshooting, serial-log]
level: practitioner
status: docs-checked
description: "Enable boot diagnostics with managed or custom storage and read VM screenshots and serial logs to diagnose boot failures, stop errors, fsck prompts and cloud-init hangs."
sources: ["https://learn.microsoft.com/azure/virtual-machines/boot-diagnostics", "https://learn.microsoft.com/troubleshoot/azure/virtual-machines/windows/boot-diagnostics", "https://learn.microsoft.com/cli/azure/vm/boot-diagnostics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Boot diagnostics screenshots and logs

**Goal:** when a VM is "running" but unreachable, see what the console shows.

## Enable
```bash
az vm boot-diagnostics enable -g rg -n vm1                          # managed storage (recommended)
az vm boot-diagnostics enable -g rg -n vm1 --storage https://stdiag.blob.core.windows.net/   # custom
```
- Managed storage: no account to maintain and recommended; boot diagnostics is enabled by default for VMs created in the portal. If `--storage` is not given, managed storage is used.
- Custom storage: pass the account's blob endpoint URI; see the boot diagnostics page for its current restrictions.
Policy *Boot Diagnostics should be enabled on virtual machines* to audit fleet-wide.

## Read
```bash
az vm boot-diagnostics get-boot-log -g rg -n vm1 | tail -100       # serial output (Linux mostly)
az vm boot-diagnostics get-boot-log-uris -g rg -n vm1               # SAS URIs to screenshot + log
```
Portal: VM → Help → **Boot diagnostics** → Screenshot / Serial log. Screenshots and output can take up to 10 minutes to appear.

## What to look for
| Screenshot / log | Meaning | Next step |
|---|---|---|
| Windows "Getting ready" / "Applying updates x%" | Updates in progress | Wait; don't restart mid-update |
| Blue screen with stop code (e.g. INACCESSIBLE_BOOT_DEVICE) | Driver/disk issue | `az vm repair` rescue VM |
| "Preparing automatic repair" loop | Boot config corrupt | Repair VM, bcdedit/chkdsk offline |
| Linux `emergency mode` / `Give root password for maintenance` | fstab entry failed | Serial Console, fix fstab (add `nofail`) |
| `fsck` prompt / `UNEXPECTED INCONSISTENCY` | Filesystem corruption | Serial console fsck or repair VM |
| `cloud-init` stuck on `waiting for network` | NIC/DHCP/cloud-init config | Check NIC, redeploy |
| GRUB prompt | Kernel/GRUB misconfig | Serial Console GRUB menu, previous kernel |
| Login prompt visible but SSH fails | OS is up — network/NSG/sshd | Network Watcher, Run Command |

## Gotchas
- Screenshots and console output can lag by minutes; the serial log is the main source for Linux.

## Verify
- [ ] `az vm show -g rg -n vm1 --query diagnosticsProfile.bootDiagnostics` shows `enabled: true`.
- [ ] Screenshot and serial log reflect the last boot of the VM.

## Checked
2026-10-28. Confirmed on the boot diagnostics and CLI pages: managed storage recommended and used when `--storage` is omitted, enabled by default for portal-created VMs, screenshots plus serial log, screenshots and output can take up to 10 minutes to appear. Wrong claim fixed: screenshot refresh about every 30 s. Removed: custom-storage firewall/premium restrictions, deallocation, framebuffer, Trusted Launch and silent-block claims, the 'within a minute' promise. The symptom table is troubleshooting guidance and was not individually sourced.
Method: documentation only; no commands were run.
