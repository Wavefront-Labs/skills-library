---
id: computing-software.systems-network-administration.virtualisation.vcsa-deployment-and-sizing
name: vcsa-deployment-and-sizing
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vcsa, vcenter-deployment, vcenter-server-appliance, vcsa-deployment, vcsa-sizing, vcsa-deploy-cli, vmware, vcenter, vsphere]
level: practitioner
status: docs-checked
description: "Deploy the vCenter Server Appliance: DNS prerequisites, deployment and storage size choice, stage 1/2 installer, CLI JSON templates and first-day checks."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-installation-and-setup/deploying-the-vcenter-server-appliance/cli-deployment-of-the-vcsa-and-psc-appliance/deploy-the-vcsa-by-using-the-cli.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-installation-and-setup/deploying-the-vcenter-server-appliance/vcenter-server-appliance-requirements.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying the vCenter Server Appliance (VCSA)

**Goal:** a correctly sized vCenter that comes up first time, because the two things that
break VCSA installs (DNS and size) were settled beforehand.

## Before you start
- **Forward and reverse DNS** for the VCSA FQDN must resolve from the deployment
  workstation and from the target ESXi host. The FQDN becomes the system name (PNID) and
  is painful to change later. Never deploy with an IP as the system name in production.
- **NTP** consistent on ESXi hosts and VCSA; SSO token validation fails with skew.
- Static IP, gateway, and a free port group on the target host.
- Note the SSO domain name (`vsphere.local` default); check the current guide for
  constraints before choosing it.

## Sizing
Deployment sizes (tiny through x-large) each carry a vCPU/RAM/host/VM limit, and a
separate storage size choice mostly affects stats, events and tasks retention. Take the
numbers for your release from the System Requirements for the vCenter Server Appliance
section of the guide; sizing tables change between releases. Pick for expected growth:
scaling up later is supported but means a reconfigure/resize.

## Stage 1 and 2
- **Stage 1** deploys the OVA to an ESXi host (or existing vCenter) with thin disk if
  space is tight. **Stage 2** configures SSO, NTP, SSH and CEIP. If stage 2 fails, finish
  it at `https://<vcsa>:5480` rather than redeploying.
- CLI for repeatable builds:
```sh
vcsa-deploy install --accept-eula --acknowledge-ceip <json-template>.json
```
The installer ships sample templates in the `vcsa-cli-installer/templates/install`
directory; see the CLI deployment pages for the full command syntax.

## First-day checks
- VAMI (`:5480`): health green, backup schedule configured, time sync with host or NTP.
- Replace or plan certificates; add AD/LDAP identity source; create named admin accounts
  and keep `administrator@vsphere.local` as break-glass only.
- Set DRS rule or override so vCenter is a high HA restart priority.

## Verify
`https://<fqdn>/ui` loads with the FQDN (not IP); `nslookup <ip>` returns the FQDN;
VAMI → Summary shows all services healthy.

## Checked
2026-10-31: DNS/clock prerequisites for deployment confirmed on the System Requirements for vCenter Server Appliance page; `vcsa-deploy install --accept-eula --acknowledge-ceip`, the `vcsa-cli-installer/templates/install` template directory and the stage-1/stage-2 structure confirmed on the CLI deployment pages; VAMI port 5480 confirmed in the vSphere Automation API overview. Removed the numeric sizing table (could not be confirmed against a fetched page) and the unconfirmed `--no-ssl-certificate-verification`/`--verify-template-only` flags, vDS-ephemeral and SSO-domain-rename claims.
Method: documentation only; no commands were run.
