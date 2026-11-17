---
id: computing-software.systems-network-administration.windows-server.kms-host-activation
name: kms-host-activation
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-activation, kms, kms-host, slmgr, vamt, volume-activation, gvlk, kms-client-setup-key, srv-record, port-1688]
level: practitioner
status: docs-checked
description: "Run a KMS host: Volume Activation Services role, CSVLK install, DNS SRV publishing, the 25/5 activation thresholds, GVLKs on clients, and slmgr checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/get-started/kms-create-host
  - https://learn.microsoft.com/en-us/windows-server/get-started/kms-client-activation-keys
  - https://learn.microsoft.com/en-us/windows-server/get-started/kms-activation-planning
  - https://learn.microsoft.com/en-us/windows-server/get-started/activation-slmgr-vbs-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KMS host activation

## Set up the host
```powershell
Install-WindowsFeature VolumeActivation -IncludeManagementTools
slmgr /ipk <KMS_HOST_KEY_CSVLK>       # from the Microsoft licensing portal (VLSC/M365 admin)
slmgr /ato
slmgr /dlv                            # shows "VOLUME_KMS" channel and current count
```
(Or run `vmw.exe` to use the Volume Activation Tools wizard; choose Key Management Service, install the host key,
then activate online or by phone.) Get the KMS host key from the Microsoft 365 admin center. The CSVLK must be for
the newest OS you will activate: the Windows Server 2025 CSVLK group can be hosted on Server 2025, 2022 or 2019 and
activates Server 2025 back to 2008 plus supported Windows 11, 10, 8.1 and 7 editions (some hosts need updates; check
the KMS activation planning table). A KMS host on a Windows client OS can only activate client OSes. A CSVLK can
activate up to six KMS hosts, and the same host can be reactivated up to nine times with the same key.

- Firewall: inbound **TCP 1688** from clients (default). To limit profiles:
  `Set-NetFirewallRule -Name SPPSVC-In-TCP -Profile Domain,Private -Enabled True`.
- DNS: the host publishes `_vlmcs._tcp.<domain>` SRV records automatically if dynamic updates are allowed. If DNS
  does not support dynamic updates, create the SRV record manually (priority 0, weight 0, port 1688, host FQDN) and
  clear Publish in the wizard. Publishing into extra DNS domains uses the `DnsDomainPublishList` registry value
  (see the Microsoft KMS DNS troubleshooting article).

## Thresholds
KMS activates only when the host count is **25 or more** (Windows client OS) or **5 or more** (Windows Server and
volume Office). Below that clients get `0xC004F038` (count insufficient); `slmgr /dli` on the host shows the count.
The count includes only unique connections from the past 30 days and the host keeps the 50 most recent contacts.
Activation lasts 180 days; clients try to renew every 7 days by default.

## Clients
Volume-licensed media installs with a **GVLK** (KMS client setup key) built in. To switch a
machine from MAK/retail to KMS:
```cmd
slmgr /ipk <GVLK_FOR_EDITION>     (public list on Microsoft Learn)
slmgr /skms kms01.ad.example.com:1688     (optional; otherwise found via DNS SRV)
slmgr /ato
slmgr /dlv
```

## Consider instead
**Active Directory-based activation** (no host, no thresholds) for domain-joined machines;
keep KMS for non-domain machines if needed.

## Verify
- [ ] `slmgr /dli` (or `/dlv`) on the host shows a count at or above the threshold.
- [ ] `nslookup -type=srv _vlmcs._tcp.ad.example.com` returns the host.
- [ ] Clients show Licensed and `slmgr /xpr` shows an expiry about 180 days out.

## Checked

2026-10-27. Documentation release: windowsserverdocs get-started pages (Create a KMS host, dated 2025-04-03; KMS activation planning; slmgr options; error codes page dated 2026-02-12). Confirmed: Install-WindowsFeature VolumeActivation, vmw.exe, TCP 1688, SPPSVC-In-TCP rule, SRV record fields, 25 and 5 thresholds and the 30-day and 50-contact counting, 180-day validity and 7-day renewal, CSVLK host and activation tables, six hosts and nine reactivations. Removed the unconfirmed sentence about VLSC and generic multi-domain detail beyond the DnsDomainPublishList name.

Method: documentation only; no commands were run.
