---
id: computing-software.cloud-infrastructure-engineering.aws.efs-mount-troubleshooting
name: efs-mount-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, efs, efs-mount-troubleshooting, nfs-port-2049, mount-target-dns, amazon-efs-utils, stale-file-handle]
level: practitioner
status: docs-checked
description: "Fix EFS mounts that fail, hang or are denied: security group on 2049, DNS resolution, efs-utils, IAM and file system policy, access points, fstab and NFS mount options."
sources: ["https://docs.aws.amazon.com/efs/latest/ug/troubleshooting-efs-mounting.html", "https://docs.aws.amazon.com/efs/latest/ug/mounting-fs-mount-helper-ec2-linux.html", "https://docs.aws.amazon.com/efs/latest/ug/mounting-fs-nfs-mount-settings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EFS mount troubleshooting

## 1. Mount hangs, then fails with a timeout
Symptom: `mount.nfs: Connection timed out` after a minute or two. The troubleshooting page gives two causes:
1. The mount target security group lacks an inbound rule allowing NFS on **port 2049** from the EC2 instance's security group.
2. The mount target IP address you specified is wrong. With nothing else at that address to reject the mount, you get the same hang.

## 2. DNS name does not resolve
`mount.nfs: Failed to resolve server ... Name or service not known` when using a plain NFS client with the file system DNS name. File system and mount target DNS names are not resolvable from outside the VPC where they exist. Before mounting by DNS name:
- There must be a mount target in the same Availability Zone as the instance, and in the same VPC.
- The instance must use the Amazon-provided DNS server (DHCP option set) and the VPC must have DNS hostnames enabled.
For a different VPC or account, see the AWS page "Mounting EFS file systems from another AWS account or VPC". With the mount helper you can mount by mount target IP: `sudo mount -t efs -o tls,mounttargetip=<mount-target-ip> <file-system-id> <mount-point>/`.

## 3. Mount fails right after creation
It can take up to 90 seconds after creating a mount target for DNS records to propagate fully in a Region. In CloudFormation or other automation, add a wait condition.

## 4. Access denied
`mount.nfs4: access denied by server while mounting 127.0.0.1:/` means the NFS client lacks permission. If you mount with IAM, use `-o iam` or `-o tls` so the mount helper passes credentials. Then check the file system policy and the identity policy: no DENY clause may apply, and at least one ALLOW clause must.

## 5. Access point mount fails
`mounting access_point failed, reason given by server: No such file or directory` means the access point root directory does not exist. EFS creates it only if you supply ownership and permissions for it on the access point.

## 6. Other documented errors
- `wrong fs type, bad option, bad superblock`: install `nfs-utils` (`nfs-common` on Ubuntu).
- `mount.nfs: an incorrect mount option was specified`: the distribution probably lacks NFSv4.1. The page checks with `grep CONFIG_NFS_V4_1 /boot/config*`; `# CONFIG_NFS_V4_1 is not set` means it is unsupported.
- Windows EC2 instances: EFS is not supported.
- `nfs: server_name still not responding` on TCP reconnection: use the `noresvport` mount option.
- "bad file handle" on a newly mounted file system: can happen when a deleted file system's mount target IP is reused by a new one. Unmount and remount.
- Mount target stuck in `creating` or `deleting`: retry `CreateMountTarget` or `DeleteMountTarget`.
- Mount target in `error`: a conflicting `efs.<region>.amazonaws.com` hosted zone in the VPC stops EFS creating DNS records. Delete the conflicting host and recreate the mount target.
- Commands such as `ls` hang: another process writing large amounts of data (in uninterruptible sleep, state D) can block access to that file. Wait, or use `/bin/ls` directly rather than an alias, or have the writer flush periodically with `fsync(2)`.
- Unmount fails because the file system is busy: `umount -l` (lazy), wait for I/O to finish, or `umount -f`, which interrupts in-flight reads and writes.

## 7. fstab and mount options
- `_netdev` in `/etc/fstab` stops the client mounting until the network is enabled. Without it the instance might become unresponsive; the page says to contact AWS Support if that happens.
- `nofail` lets the instance start regardless of the EFS mount state.
- Two or more EFS entries in `/etc/fstab` under systemd can fail to mount, with `nfs4_discover_server_trunking unhandled error -512` in dmesg. The page's workaround is a oneshot systemd unit `mount-nfs-sequentially.service` (`After=remote-fs.target`, `ExecStart=/bin/mount -avt efs` with the mount helper, or `-avt nfs4` for manual mounts), enabled with `systemctl daemon-reload` and `systemctl enable`.
- Recommended NFS options: `nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport`. `noresvport` makes the client use a new TCP source port after reconnection; clients on Linux kernel v5.4 and below retry on the same port and can fail to reconnect quickly. The mount helper uses optimised options; prefer it.
- `timeo` should be at least 150 (15 seconds) if you change it, and a soft mount should use at least that.
- EFS does not support `nconnect` or Kerberos security variants.
- Mount via the DNS name so the client reaches the mount target in its own AZ; a cross-AZ mount target adds standard EC2 cross-AZ data charges and latency.

## Method
Each point above is taken from the three cited EFS pages. Port numbers, option values and error strings are quoted from them.

## Checked
Checked 2026-11-08 against the three cited EFS User Guide pages (troubleshooting mount issues, mounting with the EFS mount helper, recommended NFS mount settings). Removed as not stated on those pages: CLI query snippets, NACL and ephemeral port advice, efs-utils TLS port range and log path, IAM client action names, burst-credit and `PercentIOLimit` metric advice, Fargate/Lambda notes.
Method: docs-only read of cited pages, 2026-11-08
