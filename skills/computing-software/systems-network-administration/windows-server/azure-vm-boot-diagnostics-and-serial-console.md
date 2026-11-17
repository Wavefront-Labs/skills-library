---
id: computing-software.systems-network-administration.windows-server.azure-vm-boot-diagnostics-and-serial-console
name: azure-vm-boot-diagnostics-and-serial-console
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, boot-troubleshooting, winre, serial-console, boot-diagnostics, azure-vm, sac, az-vm-repair]
level: practitioner
status: docs-checked
description: "Troubleshoot Windows Server VMs in Azure that will not boot: boot diagnostics, Serial Console with SAC/CMD, and az vm repair to fix the OS disk offline."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/windows/serial-console-windows
  - https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/windows/repair-windows-vm-using-azure-virtual-machine-repair-commands
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure VM boot diagnostics and Serial Console

## Boot diagnostics
Enable boot diagnostics on the VM first: Serial Console needs it, and it is compatible
with a managed boot diagnostics storage account. If nothing shows in the serial console,
check that boot diagnostics is enabled. The screenshot and serial log show whether the VM
is stuck booting or reaches a login screen (in which case look at networking, not boot).
```bash
az vm boot-diagnostics get-boot-log -g rg -n vm01
```

## Serial Console (Special Administration Console)
Newer Windows Server images on Azure have SAC enabled by default; a Windows Server image
created before February 2018 probably does not. If SAC is off, the console shows only
health information or a blank screen. Connected, the prompt is `SAC>`:
```
SAC> cmd
SAC> ch -si 1          # switch to the channel running CMD (or press esc then tab)
```
Then log on with an account that has a password. Enable SAC on custom or older images
from an elevated prompt, then reboot:
```
bcdedit /ems {current} on        (PowerShell: bcdedit /ems '{current}' on)
bcdedit /emssettings EMSPORT:1 EMSBAUDRATE:115200
```
To show boot loader prompts in the console, Learn also lists
`bcdedit /set {bootmgr} displaybootmenu yes`, `bcdedit /set {bootmgr} timeout 10` and
`bcdedit /set {bootmgr} bootems yes`. If you cannot type at the SAC prompt and kernel
debugging is enabled, run `bcdedit /debug {current} off` from an elevated prompt (RDP),
or edit the BCD store offline with `bcdedit /store <drive>:\boot\bcd`.
Known issue: with a custom boot diagnostics storage account behind a firewall, use the
Serial Console in the Azure portal rather than `az serial-console`.

## Offline repair (OS will not boot)
Workflow on Learn: add or update the extension, `create`, `run` (or fix by hand), `restore`.
```bash
az extension add -n vm-repair
az vm repair create -g rg -n vm01 --repair-username repadmin --repair-password '<pw>' --verbose
az vm repair list-scripts            # pick a run-id, or use the one a troubleshooting guide names
az vm repair run -g rg -n vm01 --run-id <run-id> --verbose
az vm repair restore -g rg -n vm01 --verbose     # swaps the repaired OS disk back
```
`create` attaches a copy of the OS disk to a new repair VM. `run` and `restore` need the
same-case inputs used in `create`; do not modify the tags on the repair VM, as `restore`
depends on them.

## Verify
- [ ] Screenshot shows the login screen; RDP works; root cause recorded.

## Checked
2026-10-28. Confirmed against the Learn pages "Use the Azure Serial Console for SAC and boot loader" (SAC default on newer images, pre-February-2018 caveat, `cmd`, `ch -si 1`, bcdedit EMS commands, managed storage compatibility) and "Repair a Windows VM by using the Azure Virtual Machine repair commands" (extension add, create, run with run-id, list-scripts, restore swapping the disk, tags, case rule). `check_commands.py` passed the `az` commands. Removed as unconfirmed: the registry, firewall and `net user` snippets, `win-toggle-safe-mode`, Reset password, Run Command, and the stuck-state descriptions.
Method: documentation only; no commands were run.
