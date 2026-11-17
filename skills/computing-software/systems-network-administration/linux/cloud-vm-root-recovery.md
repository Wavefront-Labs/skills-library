---
id: computing-software.systems-network-administration.linux.cloud-vm-root-recovery
name: cloud-vm-root-recovery
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, cloud-root-recovery, rescue-instance, serial-console, root-password-recovery, ssh-lockout, ec2, azure, gcp]
level: advanced
status: draft
description: "Regain access to a locked-out cloud VM: provider serial console, detaching the root volume to a rescue instance, chroot fixes for sshd/keys/fstab, and cloud-init key reset."
sources:
  - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-serial-console.html
  - https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/linux/repair-linux-vm-using-azure-virtual-machine-repair-commands
  - https://cloud.google.com/compute/docs/troubleshooting/troubleshooting-using-serial-console
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud VM root recovery

**Situations:** lost SSH key, broken sshd_config, bad fstab hanging boot, firewall locked you out,
password expired, sudoers broken. No physical console — use the provider's paths.

## Option 1 — serial console (fastest, if a password works)
- AWS EC2 Serial Console (Nitro, enable at account level), Azure Serial Console, GCP serial port
  (`gcloud compute connect-to-serial-port`). Needs a local user with a password, or GRUB access to
  boot `init=/bin/bash` / `rd.break` exactly as on bare metal.

## Option 2 — rescue instance (always works)
1. Snapshot the broken root volume first.
2. Stop the VM; detach its root disk; attach to a rescue VM in the same AZ (Azure: `az vm repair create`
   automates this; AWS: EC2Rescue / manual).
3. On the rescue VM:
```bash
lsblk -f                                   # find it; beware duplicate XFS UUID with the rescue root
mount -o nouuid /dev/nvme1n1p1 /mnt        # XFS: nouuid when both disks are from the same image
# LVM with same VG name as rescue: vgimportclone --basevgname recover /dev/nvme1n1p3
for d in dev proc sys; do mount --rbind /$d /mnt/$d; done
chroot /mnt
```
4. Fix: append your key to `/home/<user>/.ssh/authorized_keys` (check owner/600), `sshd -t`, comment the
   bad fstab line or add `nofail`, `visudo -c`, `passwd <user>`. SELinux: `touch /.autorelabel` if you edited
   labelled files from a non-SELinux rescue.
5. Exit, unmount, reattach as root/boot disk, start.

## Option 3 — provider agents
AWS SSM Session Manager (agent + role), Azure `az vm user update --ssh-key-value`, GCP metadata
`ssh-keys` (guest agent), or cloud-init re-run by changing the instance id (images vary).

## Gotchas
- Root disk detach changes nothing on instance-store/ephemeral disks — data there is lost on stop.
- Encrypted volumes: rescue instance needs the KMS key permission.
- Keep one break-glass path enabled in advance (serial console password user or SSM).

## Verify
- [ ] SSH works with the intended key; the fix is captured in config management so the next deploy doesn't undo it.
