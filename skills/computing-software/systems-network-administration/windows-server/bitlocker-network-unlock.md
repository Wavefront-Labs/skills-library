---
id: computing-software.systems-network-administration.windows-server.bitlocker-network-unlock
name: bitlocker-network-unlock
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, bitlocker, network-unlock, wds, tpm-and-pin, bitlocker-network-unlock, certificate, dhcp]
level: advanced
status: docs-checked
description: "Deploy BitLocker Network Unlock so TPM+PIN servers reboot unattended on the corporate network: WDS feature, certificate, GPO, and troubleshooting."
sources:
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/network-unlock
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BitLocker Network Unlock

Lets machines with a TPM+PIN protector boot without the PIN when they are wired to the
corporate network: UEFI DHCP talks to a WDS-hosted provider that releases a key.

## Requirements
- UEFI firmware with a DHCP driver implemented in the firmware.
- Windows Deployment Services role on a server (does not need to serve images) with the
  BitLocker Network Unlock feature; DHCP server reachable.

## Server side
```powershell
Install-WindowsFeature WDS-Deployment -IncludeManagementTools
Install-WindowsFeature BitLocker-NetworkUnlock
```
Create a certificate (RSA 2048, EKU OID 1.3.6.1.4.1.311.67.1.1 "BitLocker Network Unlock")
(self-signed: `New-SelfSignedCertificate` or `certreq.exe`), then import the private key into the WDS server's
Local Computer store under **BitLocker Drive Encryption Network Unlock**.

## GPO
- Enable **Allow Network Unlock at startup** and deploy the public certificate to clients with Group Policy (see the
  Network Unlock page for the certificate policy location).
- Operating system volumes use TPM+PIN protectors; Network Unlock replaces the PIN prompt on the corporate network.

## Troubleshoot
- Server: on the WDS server, Event Viewer > Applications and Services Logs > Microsoft > Windows >
  Deployment-Services-Diagnostics > Debug.
- PIN still prompted: check that the client can reach DHCP and the WDS server, and that the WDS server holds the
  certificate private key.

## Verify
- [ ] Reboot on the corporate wired network boots without PIN; off-network asks for PIN.

## Checked

2026-10-28. Confirmed against: BitLocker Network Unlock page (BitLocker-NetworkUnlock feature name, WDS requirement, UEFI DHCP driver, OID 1.3.6.1.4.1.311.67.1.1, 2048-bit RSA certificate, Allow Network Unlock at startup, BitLocker Drive Encryption Network Unlock certificate store, Deployment-Services-Diagnostics log, TPM+PIN behaviour). Removed (not confirmable from the cited pages): TPM 1.2 and wired-only requirements, wdsutil /standalone command, AD CS template advice, GPO menu paths, TpmNetworkKey protector name and BitLocker-API log name.

Method: documentation only; no commands were run.
