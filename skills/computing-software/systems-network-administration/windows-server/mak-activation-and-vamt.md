---
id: computing-software.systems-network-administration.windows-server.mak-activation-and-vamt
name: mak-activation-and-vamt
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-activation, mak, vamt, slmgr, activation-errors]
level: practitioner
status: docs-checked
description: "Activate servers with MAK keys, track remaining activations, proxy-activate isolated hosts and manage keys at scale with VAMT."
sources:
  - https://learn.microsoft.com/en-us/windows/deployment/volume-activation/volume-activation-management-tool
  - https://learn.microsoft.com/en-us/windows/deployment/volume-activation/install-vamt
  - https://learn.microsoft.com/en-us/windows/deployment/volume-activation/manage-product-keys-vamt
  - https://learn.microsoft.com/en-us/windows/deployment/volume-activation/proxy-activation-vamt
  - https://learn.microsoft.com/en-us/windows-server/get-started/activation-slmgr-vbs-options
  - https://learn.microsoft.com/en-us/windows-server/get-started/activation-error-codes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MAK activation and VAMT

MAK (Multiple Activation Key) activates each machine once against Microsoft. Use it for servers that cannot reach
KMS/ADBA (DMZ, isolated networks, too few machines for KMS threshold).

## Single server
```cmd
slmgr /ipk XXXXX-XXXXX-XXXXX-XXXXX-XXXXX
slmgr /ato
slmgr /dlv          :: license details for the installed key
```
`/ato` tries online activation for MAK keys. Where the internet is blocked, use offline activation (`slmgr /dti`
shows the installation ID, then `slmgr /atp <confirmation ID>`) or VAMT proxy activation. MAK and retail activation
is perpetual (`slmgr /xpr` is mainly useful for KMS clients).

## VAMT at scale
VAMT installs as part of the Windows ADK on any supported Windows machine and needs SQL Server Express (or a full
SQL instance) for its database. It manages MAK, retail and KMS (GVLK) activation.
1. Add products: search Active Directory, by name or IP, in a workgroup or by LDAP query. VAMT needs administrator
   rights on targets, and the WMI firewall exception must be enabled on them.
2. Product Keys: add the MAK; select it and use Refresh product key data online to retrieve **remaining
   activations** (MAKs only; needs internet).
3. Select machines > Install product key > Activate > Online activate.
4. **Proxy activation** for machines without internet: the VAMT host collects installation IDs, gets confirmation
   IDs from Microsoft and installs them. For an isolated workgroup, VAMT is installed in the workgroup and CILx files
   are carried to an internet-connected VAMT instance and back.

## Track
A MAK can be activated only a limited number of times (`0xC004C020` means the limit is exceeded); request more
activations from the Microsoft Licensing Activation Centers. Keep VAMT's database as the inventory of what used
which key.

## Gotchas
- Do not put MAKs in images or scripts in shared repos.

## Verify
- [ ] `slmgr /dli` shows License Status: Licensed.
- [ ] VAMT inventory updated after each batch.

## Checked

2026-10-27. Documentation release: Microsoft Learn VAMT pages (technical reference and install, last updated 2025-05-14), proxy activation, manage product keys, slmgr options and the activation error codes page (2026-02-12). Confirmed: SQL Server Express or full SQL requirement, VAMT installed with the ADK, WMI firewall exception, search options, MAK remaining-activation refresh, proxy activation flow, /dti and /atp, /xpr note on perpetual MAK activation, 0xC004C020. Removed slui 4, the channel string, the reuse-on-reinstall claim and the retail media claim as unconfirmed.

Method: documentation only; no commands were run.
