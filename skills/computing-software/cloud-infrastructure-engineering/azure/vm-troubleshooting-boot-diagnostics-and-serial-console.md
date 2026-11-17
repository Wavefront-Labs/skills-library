---
id: computing-software.cloud-infrastructure-engineering.azure.vm-troubleshooting-boot-diagnostics-and-serial-console
name: vm-troubleshooting-boot-diagnostics-and-serial-console
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-troubleshooting, boot-diagnostics, serial-console, vm-redeploy, vm-repair, az-vm-repair, rescue-vm, vm-reset-password, vmaccess-extension, resource-health, allocation-failed, rdp-troubleshooting, ssh-troubleshooting, fstab, grub, sysrq, nmi, provisioning-timeout, wireserver, nested-repair]
level: practitioner
status: draft
description: "Recover a broken Azure VM: boot diagnostics, Serial Console (GRUB/SysRq/SAC), redeploy vs reapply, VMAccess resets, az vm repair rescue-disk workflow, and fstab/network lockouts."
sources: ["Microsoft Learn - Azure boot diagnostics", "Microsoft Learn - Azure Serial Console for Linux and Windows", "Microsoft Learn - Repair a Linux/Windows VM by using the Azure Virtual Machine repair commands", "Microsoft Learn - Redeploy Linux/Windows virtual machine to new Azure node", "Microsoft Learn - Troubleshoot SSH/RDP connections to an Azure VM"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM troubleshooting — boot diagnostics, Serial Console, redeploy, repair

**Goal:** get from "VM unreachable" to root cause in minutes using the control-plane
tools, and have a rescue path that doesn't need the VM to boot.

## 1. Triage order
1. **Resource Health** (`az resource show ... Microsoft.ResourceHealth/availabilityStatuses`
   or portal) — platform issue vs yours. *Unavailable* with a platform reason → wait/redeploy.
2. `az vm get-instance-view --query instanceView.statuses` — `PowerState/running` but
   `ProvisioningState/updating` for ages = extension/agent; `VM agent not ready` = guest
   can't reach WireServer `168.63.129.16` (NSG/UDR/guest firewall) or agent dead.
3. **Boot diagnostics** (`az vm boot-diagnostics get-boot-log`, screenshot
   `az vm boot-diagnostics get-boot-log-uris`): managed boot diagnostics is on by default;
   enable with `az vm boot-diagnostics enable`. Screenshot tells you: BSOD, GRUB rescue,
   fsck prompt, "Press a key", Windows update loop.
4. **Serial Console** — needs boot diagnostics, `az vm` *Contributor* + *VM Login*-ish, and
   the subscription's console not disabled. Linux: a login shell (password or SysRq);
   Windows: SAC (`cmd`, `ch -si 1`, then normal cmd/PowerShell).
5. Network: NSG effective rules (`az network nic list-effective-nsg`), effective routes,
   Network Watcher *Connection troubleshoot* to port 22/3389 from Bastion subnet; guest
   firewall (`ufw`, Windows Firewall) last.

## 2. Control-plane actions, least to most invasive
| Action | What it does | Use when |
|---|---|---|
| `az vm restart` | guest reboot via agent, or hard if agent dead | hung process |
| `az vm reapply` | re-applies VM state/config to the host | stuck `Updating`/`Failed` provisioning |
| `az vm redeploy` | shuts down, moves to a **new host**, keeps disks (temp disk lost) | host-level trouble, RDP/SSH dead with no guest change |
| `az vm deallocate` + `start` | full reallocation, new host, IP may change (Basic IP) | allocation stuck, size change |
| Serial Console SysRq / NMI | Portal Serial Console: *Send Non-Maskable Interrupt* or *Send SysRq Command* | kernel hung, capture crash dump |

## 3. Serial Console moves
- Linux root password lost: GRUB → `e` → append `init=/bin/bash` (or `rd.break`) → `mount -o remount,rw /` → `passwd` → `exec /sbin/init`. Needs the console serial params already in the image (Azure images have `console=ttyS0`).
- Bad `/etc/fstab` (common after a disk detach): boot drops to emergency shell; `mount -o remount,rw /`, fix fstab (`nofail` on every data disk, use `UUID=` not `/dev/sdX`), `exit`.
- SSH broken: `systemctl status sshd`, `/var/log/auth.log`; permissions on `~/.ssh`; `sshd -t` for config errors.
- Windows SAC: `ch -sn Cmd0001 ... ` → `net start`, `netsh advfirewall set allprofiles state off`, `sc config TermService start=auto`, check `netsh interface ip show config`.
- Enable SysRq on Linux `echo 1 > /proc/sys/kernel/sysrq` for `sync`/`unmount`/`reboot` from the console.

## 4. Reset access without the console
`az vm user update -n vm -g rg -u azureuser --ssh-key-value "$(cat ~/.ssh/id_ed25519.pub)"` /
`--password` (Windows) uses the **VMAccess** extension — needs a working agent. It also
`az vm user reset-ssh` (resets sshd config/keys).

## 5. Offline repair with `az vm repair`
```bash
az extension add -n vm-repair
az vm repair create -g rg -n vm-broken --repair-username rescue --repair-password '<pwd>' --unlock-encrypted-vm --verbose
# → copies the OS disk, builds a rescue VM in rg "repair-vm-broken-<guid>" with the copy attached as a data disk
az vm repair run -g rg -n vm-broken --run-id linux-alar2 --parameters fstab      # ALAR scripts: fstab, grub, initrd, kernel, serialconsole, efifix
az vm repair run ... --run-id win-hello  / win-enable-nested-hyperv  (list: az vm repair list-scripts)
az vm repair restore -g rg -n vm-broken       # swaps the fixed OS disk back, deletes rescue resources
```
Manual path: mount the disk copy on the rescue VM (`lsblk`, `mount /dev/sdc1 /mnt`), chroot
(`for i in dev proc sys; do mount --bind /$i /mnt/$i; done; chroot /mnt`), fix, `az vm update --os-disk <fixed-disk>` on the original (OS disk swap requires deallocated VM).
Windows: attach copy to a Windows rescue VM, run `bcdedit /store <DATA_DRIVE>:/boot/bcd`, `sfc`, registry
load, or `chkdsk`; restore the same way.

## 6. Common root causes
- `AllocationFailed`/`OverconstrainedAllocationRequest`: size unavailable in that cluster — deallocate+start, change size/zone, or capacity reservation.
- Kernel upgrade without Azure modules (`hv_*`): boots to a blank screenshot — GRUB select the previous kernel, then fix.
- Disk full on OS: agent fails, extensions fail; grow the disk (`az disk update --size-gb`) and `growpart`.
- Custom NSG/UDR sends `168.63.129.16` through a firewall → agent *Not Ready*, extensions time out, DHCP leases fail.
- Windows: `Shutdown Event Tracker`/`Windows Update` loop shows as "Getting Windows ready" screenshot for hours — wait, then NMI if truly hung.

## Gotchas
- Serial Console writes are visible in the Activity log but console *input* isn't audited beyond that — treat access as root.
- `redeploy` on a VM with ephemeral OS disk reimages it (data gone); on Spot it may fail allocation.
- `az vm repair create` needs quota for the rescue size and fails on Trusted Launch sources unless the extension version supports it (use `--enable-nested`/latest extension).
- Disk swap requires the replacement disk to be the same OS type and not attached elsewhere.
- Boot diagnostics custom storage account must allow trusted services if firewalled, or you get *No data available*.

## Verify
- [ ] Screenshot/log from `az vm boot-diagnostics get-boot-log` is current (timestamp within minutes).
- [ ] Serial Console login works on a healthy VM before you need it (image has `console=ttyS0`/SAC enabled).
- [ ] After `az vm repair restore`, the VM boots, `az vm get-instance-view` shows agent `Ready`, and the rescue RG is gone.
- [ ] Post-incident: `nofail` in fstab, UUID mounts, and an alert on agent *Not Ready*.
