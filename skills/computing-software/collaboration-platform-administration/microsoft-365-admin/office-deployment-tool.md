---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.office-deployment-tool
name: office-deployment-tool
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [office-deployment-tool, m365-apps-deploy]
level: practitioner
status: draft
description: Install Microsoft 365 Apps with ODT and a configuration XML.
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deploy with the Office Deployment Tool
**Goal:** Install Microsoft 365 Apps with ODT and a configuration XML.

- Download ODT (setup.exe); build the XML at config.office.com.
- `setup.exe /download config.xml` to cache the source; `setup.exe /configure config.xml` to install.
- Set Product ID `O365ProPlusRetail`, Channel, Display Level=None, Accept EULA.
- Exclude apps with `<ExcludeApp ID="Groove"/>` as needed.
- For managed devices prefer Intune or Configuration Manager (reference those products).

## Gotchas
- Mixing MSI Office and Click-to-Run installs on a device fails; remove the old one.
- Shared computer activation needs `SharedComputerLicensing` set to 1.

## Self-check
Check Account > About in an Office app and `Get-ItemProperty` the ClickToRun Configuration registry key for the channel.
