---
id: computing-software.systems-network-administration.windows-server.wac-high-availability-gateway
name: wac-high-availability-gateway
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-admin-center, wac-high-availability, failover-cluster, gateway]
level: advanced
status: docs-checked
description: "Deploy Windows Admin Center gateway as a highly available role on a failover cluster with shared storage and a certificate on the client access point."
sources:
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/deploy/high-availability
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/plan/installation-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Highly available Windows Admin Center gateway

A single WAC gateway server is a single point of failure for admins who live in it. WAC can run in a failover cluster
as an active-passive generic service with its data on a cluster shared volume (CSV): one instance is active and it fails
over to another node.

## Prerequisites
- Failover cluster of two or more nodes on Windows Server 2016 or later.
- A CSV for persistent data that all nodes can access (the docs say 10 GB is enough).
- A certificate thumbprint from a valid CA, with the private key installed on every node.
- The HA scripts from the Windows Admin Center HA script zip (`Deploy-GatewayV2Ha.zip`: Deploy, Validate, Inspect and
  Uninstall scripts; keep all of them on every node) and the Windows Admin Center `.exe` installer.

## Install
Run `Deploy-GatewayV2Ha.Deploy.ps1` as administrator on one node with:
`-clusterStorage` (CSV path), `-clientAccessPoint` (name users browse to), optional `-staticAddress`, `-InstallerPath` (the `.exe`),
`-CertificateThumbprint`, optional `-generateSslCert` (self-signed, expires in 60 days) and optional `-HttpsPort` (default 443).
`-WhatIf` and `-Verbose` are supported.
```powershell
$parameters = @{
  ClusterStorage = "<CSV path>\Gateway"
  ClientAccessPoint = "gateway-ha"
  StaticAddress = '10.0.0.50'
  InstallerPath = "<path to installer>.exe"
  CertificateThumbprint = "<thumbprint>"
}
Deploy-GatewayV2Ha.Deploy @parameters
```

## Update / certificate change
Run the same script again with the new `-InstallerPath` to update without losing connection data. To change only the
certificate, add `-UpdateCertificate` with `-ClusterStorage`, `-ClientAccessPoint` and the new `-CertificateThumbprint`.

## Gotchas
- WAC 2311 and older cannot be upgraded directly from an HA deployment to 2410 or newer (architecture change): uninstall and
  reinstall. The installation-options page also says version 2410 itself does not support HA; check it for your version.
- Logs are in the `temp` folder of the CSV; `Deploy-GatewayV2Ha.Inspect.ps1 -Mode Diagnostics` collects diagnostics.
- Uninstall with `Deploy-GatewayV2Ha.Uninstall` (`-ClusterStorage`, `-ClientAccessPoint`).

## Verify
- [ ] `Get-ClusterGroup` shows the WAC role online; moving it to another node keeps the client access point URL working.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, Windows Admin Center pages (ms.date 2025 for access, install, certificate, HA and troubleshooting; WAC 2410+ modernized gateway).
Confirmed from deploy/high-availability (ms.date 2025-06-23): active-passive design, prerequisites (2016+, CSV 10 GB, certificate on every node), the Deploy-GatewayV2Ha scripts and parameters,
-UpdateCertificate, uninstall and Inspect diagnostics, the 2311-to-2410 upgrade restriction, and plan/installation-options (2410 HA note).
Replaced the legacy Install-WindowsAdminCenterHA.ps1 example and MSI/PFX parameters; removed the CNO delegation and shared-extensions claims, which the page does not state.
Method: documentation only; no commands were run.
