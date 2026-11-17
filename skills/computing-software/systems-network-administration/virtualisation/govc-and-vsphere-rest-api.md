---
id: computing-software.systems-network-administration.virtualisation.govc-and-vsphere-rest-api
name: govc-and-vsphere-rest-api
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [govc, vsphere-api, vsphere-rest-api, vsphere-automation-api, pyvmomi, govmomi, curl, automation, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Automate vSphere from Linux/CI with govc and the vSphere Automation REST API: auth/session tokens, common govc commands, REST calls with curl, and when to use pyVmomi."
sources:
  - https://raw.githubusercontent.com/vmware/govmomi/main/govc/USAGE.md
  - https://developer.broadcom.com/xapis/vsphere-automation-api/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# govc and the vSphere REST API

**Goal:** script vSphere without Windows or PowerShell: CI pipelines, Linux jump hosts,
quick one-liners.

## govc
Single static Go binary from the govmomi project.
```sh
export GOVC_URL='https://vc01.<domain>/sdk'    # credentials from your vault; see the govc usage reference
export GOVC_DATACENTER=DC1 GOVC_INSECURE=false     # trust the CA rather than skipping TLS
govc about
govc ls /DC1/vm
govc find / -type m -runtime.powerState poweredOn | wc -l
govc vm.info -json app01 | jq '.virtualMachines[0].guest.ipAddress'
govc snapshot.tree -vm app01 -D -i
govc vm.clone -vm tmpl-ubuntu -on=false -folder=/DC1/vm/apps -ds=ds01 app02
govc vm.change -vm app02 -c 4 -m 8192
govc vm.power -on app02
govc host.esxcli -host esx01 system version get
govc datastore.ls -ds=ds01 app01/
```
`govc object.collect` reads any property; `-json` output pipes into `jq`.

## REST (vSphere Automation API, `/api`)
```sh
TOKEN=$(curl -s -X POST -u '<user>:<pw>' https://vc01/api/session | tr -d '"')
curl -s -H "vmware-api-session-id: $TOKEN" https://vc01/api/vcenter/vm | jq '.[] | {name}'
curl -s -H "vmware-api-session-id: $TOKEN" -X POST "https://vc01/api/vcenter/vm/<vm-id>/power?action=start"
curl -s -X DELETE -H "vmware-api-session-id: $TOKEN" https://vc01/api/session
```
REST covers VM lifecycle, tagging, content library, appliance (VAMI) management and
backups, but not everything; deep inventory/performance still lives in the SOAP
Web Services API (pyVmomi, govmomi, PowerCLI).

## Choosing
| Need | Tool |
|---|---|
| Shell one-liners, CI | govc |
| Appliance and tag/content library operations | REST |
| Complex inventory, events, performance | pyVmomi / govmomi / PowerCLI |
| Declarative infrastructure | Terraform vSphere provider |

## Gotchas
- Sessions time out when idle; reuse a token per run and delete it after.
- Service accounts need only the privileges for the operations used.
- `GOVC_INSECURE` in examples on the internet; don't carry it into production.

## Verify
`govc about` returns the vCenter version with TLS verification on; a dry-run script
lists the objects it would touch before changing anything.

## Checked
2026-10-31: `govc about`, `govc ls`, `govc find -type m -runtime.powerState`, `govc vm.info -json`, `govc snapshot.tree`, `govc vm.clone`, `govc vm.change`, `govc vm.power`, `govc host.esxcli`, `govc datastore.ls`, the `GOVC_URL`/`GOVC_DATACENTER`/`GOVC_INSECURE` variables and the `-json` output option confirmed in the govc USAGE.md reference; the `vmware-api-session-id` header, POST Create Session and port 5480 confirmed in the vSphere Automation API overview. Removed unconfirmed specifics: GOVC_USERNAME/GOVC_PASSWORD environment variables, the `power_state` REST response field, the 30-minute session timeout and the PowerCLI Get-View example.
Method: documentation only; no commands were run.
