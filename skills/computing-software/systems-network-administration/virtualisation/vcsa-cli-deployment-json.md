---
id: computing-software.systems-network-administration.virtualisation.vcsa-cli-deployment-json
name: vcsa-cli-deployment-json
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vcsa-cli-installer, vcsa-deploy-json, vcsa, vcenter-deployment, automation, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Deploy vCenter Server Appliance repeatably with vcsa-deploy and JSON templates: template choice, precheck-only runs, verbose logs and common failures."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-installation-and-setup/deploying-the-vcenter-server-appliance/cli-deployment-of-the-vcsa-and-psc-appliance/deploy-the-vcsa-by-using-the-cli.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-installation-and-setup/deploying-the-vcenter-server-appliance/cli-deployment-of-the-vcsa-and-psc-appliance/prepare-json-configuration-files-for-cli-deployment/deployment-templates.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CLI deployment of the VCSA (vcsa-deploy)

## Where things are
On the mounted VCSA ISO: `vcsa-cli-installer/<win32|lin64|mac>/vcsa-deploy` and sample
templates in `vcsa-cli-installer/templates/install/` (e.g. `embedded_vCSA_on_ESXi.json`,
`embedded_vCSA_on_VC.json`, `vCSA_with_cluster_on_ESXi.json`). Copy one, never edit in place.

## Key template sections
Copy one of the shipped templates (for example `embedded_vCSA_on_ESXi.json`) and fill in
the ESXi host, appliance, network, OS and SSO settings plus CEIP; the Deployment
Configuration Parameters section of the guide documents every key.
`deployment_option` selects the deployment size.
`system_name` must be the FQDN with working forward and reverse DNS, or first boot fails.

## Run
```sh
vcsa-deploy install --accept-eula --acknowledge-ceip --precheck-only  vc01.json   # validate only
vcsa-deploy install --accept-eula --acknowledge-ceip --log-dir ./logs vc01.json
```
Other subcommands: `upgrade` and `migrate`. See the Syntax of the CLI Deployment Command
page for the full option list.

## Failures and fixes
| Symptom | Cause |
|---|---|
| Stage 2 hangs or first boot fails | DNS/reverse DNS wrong, or NTP far off |
| Certificate verification errors | supply the thumbprint or skip verification (see the CLI deployment syntax) |
| Insufficient resources | wrong `deployment_option` or datastore free space |
| Password rejected | complexity: 8-20 chars, lower, numeric, special (vCenter password requirements) |

## Verify
`https://vc01.corp.example:5480` VAMI reachable, `https://vc01/ui` login with
administrator@vsphere.local, and the logs in `--log-dir` show a completed deployment.
Keep the JSON (without secrets) in version control as the build record.

## Checked
2026-10-31: Template names (`embedded_vCSA_on_ESXi.json`, `embedded_vCSA_on_VC.json`, `vCSA_with_cluster_on_ESXi.json`) and the `vcsa-cli-installer/templates/install` directory confirmed on the JSON Templates for CLI Deployment page; `vcsa-deploy install` with `--precheck-only`, `--accept-eula`, `--acknowledge-ceip` and `--log-dir` confirmed on the CLI deployment pages; the vCenter password requirements (8-20 chars, lowercase/numeric/special) confirmed on the vCenter Password Requirements and Lockout Behavior page; VAMI port 5480 confirmed in the vSphere Automation API overview. Removed the full JSON key example, `--no-ssl-certificate-verification` and `--verbose`, the `-lstorage`/`-xlstorage` sizes, and unconfirmed symptom strings.
Method: documentation only; no commands were run.
