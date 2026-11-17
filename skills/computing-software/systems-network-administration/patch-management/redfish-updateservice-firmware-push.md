---
id: computing-software.systems-network-administration.patch-management.redfish-updateservice-firmware-push
name: redfish-updateservice-firmware-push
category: computing-software
field: systems-network-administration
product: patch-management
tags: [redfish, firmware-updates, bmc-firmware, simpleupdate, idrac, ilo, automation]
level: advanced
status: docs-checked
description: "Update server firmware vendor-neutrally through the Redfish UpdateService: inventory, SimpleUpdate from a URI, multipart push, apply-time options, task monitoring."
sources:
  - https://www.dmtf.org/standards/redfish
  - https://redfish.dmtf.org/schemas/v1/UpdateService.json
  - https://www.dmtf.org/sites/default/files/standards/documents/DSP0266_1.21.0.html
  - https://github.com/ansible-collections/community.general/blob/main/plugins/modules/redfish_command.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firmware updates via Redfish UpdateService

Redfish (DMTF) is a REST API implemented by many server BMCs. The **UpdateService** gives one automation path across vendors (with vendor quirks).

## Inventory
```sh
B=https://bmc01.oob.example; A="-u admin:pass --cacert bmc-ca.pem"
curl -s $A $B/redfish/v1/UpdateService | jq '{ServiceEnabled, MultipartHttpPushUri, Actions}'
curl -s $A $B/redfish/v1/UpdateService/FirmwareInventory | jq -r '.Members[]."@odata.id"' |
  while read m; do curl -s $A $B$m | jq -r '[.Name, .Version, .Updateable] | @tsv'; done
```

## Option 1: SimpleUpdate (BMC pulls from a URI)
```sh
curl -s $A -H 'Content-Type: application/json' -X POST \
  $B/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate \
  -d '{"ImageURI":"http://repo.corp.example/fw/BIOS_2.21.2.EXE","TransferProtocol":"HTTP",
       "@Redfish.OperationApplyTime":"OnReset"}' -i | grep -i location
```
`@Redfish.OperationApplyTime` values defined by Redfish: `Immediate`, `OnReset`, `AtMaintenanceWindowStart`, `InMaintenanceWindowOnReset`, `OnStartUpdateRequest` (support varies by service).

## Option 2: multipart push (upload the image)
```sh
curl -s $A -X POST "$B$(curl -s $A $B/redfish/v1/UpdateService | jq -r .MultipartHttpPushUri)" \
  -F 'UpdateParameters={"Targets":[],"@Redfish.OperationApplyTime":"OnReset"};type=application/json' \
  -F 'UpdateFile=@BIOS_2.21.2.EXE;type=application/octet-stream'
```

## Monitor
The response `Location` header points to a Task (`/redfish/v1/TaskService/Tasks/<id>`):
```sh
curl -s $A $B/redfish/v1/TaskService/Tasks/<id> | jq '{TaskState, PercentComplete, Messages}'
```
Then reboot via `ComputerSystem.Reset` (with a `ResetType` value the system lists in its allowable values) inside the
maintenance window when apply time is OnReset.

## Tooling
- Ansible `community.general.redfish_command`
  (`SimpleUpdate`, `MultipartHTTPPushUpdate`) and `redfish_info`.
- Vendor OEM extensions add catalog-based updates on some platforms (see the vendor's Redfish documentation).

## Gotchas
- Image formats are vendor specific; use the vendor's firmware package for your model.
- A BMC firmware update can restart the BMC, so the API may be unavailable for a while; poll with backoff.
- Use a dedicated low-privilege account with only update/reset rights and verify TLS.

## Verify
Firmware inventory shows target versions after reset; task state Completed; SEL/Lifecycle
log has no errors.

## Checked
Date: 2026-10-27. Documentation checked: DMTF UpdateService schema (`SimpleUpdate` action with `ImageURI` and `TransferProtocol`, `MultipartHttpPushUri`, `FirmwareInventory`, apply-time values Immediate, OnReset, AtMaintenanceWindowStart, InMaintenanceWindowOnReset, OnStartUpdateRequest), DMTF Redfish specification DSP0266 1.21 (multipart push parts `UpdateParameters` and `UpdateFile`), and the `community.general.redfish_command` module source (`SimpleUpdate`, `MultipartHTTPPushUpdate`). Fixed the Ansible command name (`UpdateSimple` is not a command) and removed the vendor image-format and OEM-extension specifics, which were not confirmed.

Method: documentation only; no commands were run.
