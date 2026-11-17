---
id: computing-software.cloud-infrastructure-engineering.azure.azure-files-smb-share-create-and-mount
name: azure-files-smb-share-create-and-mount
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-files, smb-mount, mount-file-share, net-use, cifs, file-shares, smb]
level: practitioner
status: docs-checked
description: "Create an Azure Files SMB share and mount it on Windows (net use / New-PSDrive), Linux (cifs fstab with credentials file) and macOS, with SMB security settings."
sources: ["https://learn.microsoft.com/azure/storage/files/storage-how-to-create-file-share", "https://learn.microsoft.com/azure/storage/files/storage-how-to-use-files-windows", "https://learn.microsoft.com/azure/storage/files/storage-how-to-use-files-linux", "https://learn.microsoft.com/azure/storage/files/files-smb-protocol"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create and mount Azure Files SMB shares

**Goal:** a share that mounts persistently on Windows and Linux with encryption on and the
least-privileged credential available.

## Create
```bash
az storage account create -g rg -n stfiles01 -l westeurope --kind StorageV2 --sku Standard_ZRS \
  --min-tls-version TLS1_2 --https-only true
az storage share-rm create -g rg --storage-account stfiles01 -n team --quota 1024 --access-tier TransactionOptimized
```
Provisioned shares need a `FileStorage` account (for example `--kind FileStorage --sku Premium_ZRS`); pay-as-you-go shares need `StorageV2`. Valid `--access-tier` values are TransactionOptimized, Hot and Cool. New accounts created with the CLI start with soft delete enabled for 7 days.

## SMB security settings
```bash
az storage account file-service-properties update -g rg --account-name stfiles01 \
  --versions "SMB3.1.1" --auth-methods "Kerberos" --kerb-ticket-encryption "AES-256" --channel-encryption "AES-256-GCM"
```
Valid values: versions SMB2.1, SMB3.0, SMB3.1.1; auth methods NTLMv2, Kerberos; Kerberos ticket encryption RC4-HMAC, AES-256; channel encryption AES-128-CCM, AES-128-GCM, AES-256-GCM (several values are joined with `;`). The portal offers Maximum compatibility, Maximum security and Custom profiles. Restricting to Kerberos only is safe only once identity-based auth is in place. Encryption in transit for SMB is a separate setting (`--require-smb-encryption-in-transit`).

## Windows
```powershell
Test-NetConnection stfiles01.file.core.windows.net -Port 445    # must be True
# identity-based (AD DS or Entra credentials)
net use Z: \\stfiles01.file.core.windows.net\team
# storage-key mounts (admin/break-glass): use the PowerShell script on the "Mount Azure Files on Windows" page
```

## Linux
```bash
sudo apt install -y cifs-utils
sudo mkdir -p /mnt/team /etc/smbcredentials
sudo bash -c 'printf "username=stfiles01\npassword=<key>\n" > /etc/smbcredentials/stfiles01.cred'; sudo chmod 600 /etc/smbcredentials/stfiles01.cred
echo "//stfiles01.file.core.windows.net/team /mnt/team cifs _netdev,nofail,credentials=/etc/smbcredentials/stfiles01.cred,serverino,nosharesock,actimeo=30,mfsymlinks 0 0" | sudo tee -a /etc/fstab
sudo mount -a
```
SMB 3.1.1 is the default negotiated protocol from kernel 5.0; on older kernels add `vers=3.1.1`. `actimeo` should be 30-60 (lower values degrade performance). Kerberos on a domain-joined Linux client uses `sec=krb5,cruid=<uid>` and omits username and password.

## Gotchas
- SMB needs TCP port **445**; connections fail where it is blocked. From outside Azure, use a VPN or ExpressRoute rather than opening 445.
- `nofail` in fstab prevents boot hangs when the share is unreachable.
- A storage key in a credentials file gives full account access; prefer identity-based auth for user shares.
- Use the SMB version table on the SMB protocol page to check which client OS versions support SMB 3.1.1 and AES-256-GCM.

## Verify
- [ ] Windows: `Test-NetConnection stfiles01.file.core.windows.net -Port 445` succeeds and the drive maps.
- [ ] Linux: `mount | grep cifs` shows the share with `vers=3.1.1`; write a file and read it from another client.

## Checked
2026-10-27. Confirmed against Learn: create a classic file share (account kinds, access tiers, soft delete default), Mount on Windows (port 445, net use), Mount on Linux (cifs-utils, mount options, kernel 5.0 default, actimeo, sec=krb5), SMB protocol overview, and the az storage account create, share-rm create and file-service-properties update references (flags and valid values matched).
Removed (unconfirmed): 100 TiB default claim, `/persistent:yes`, cmdkey line, `dir_mode`, `file_mode`, `uid`, `gid` options, macOS steps, private endpoint and legacy client notes, `Get-SmbConnection` check.
Method: documentation only; no commands were run.
