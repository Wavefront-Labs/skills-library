---
id: computing-software.systems-network-administration.virtualisation.vcenter-dcli-automation-api
name: vcenter-dcli-automation-api
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [dcli, vsphere-automation-api, vcenter, vmware, vsphere]
level: practitioner
status: draft
description: "Use the Datacenter CLI (dcli) against the vSphere Automation API for vCenter and appliance tasks: interactive mode, credstore, namespaces and JSON output."
sources:
  - https://developer.broadcom.com/tools/vmware-data-center-cli/latest
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Datacenter CLI (dcli)

**Goal:** script vCenter and VCSA appliance operations exposed by the Automation (REST) API without writing HTTP calls.

## Where it runs
- Preinstalled on the VCSA (`dcli` in the appliance shell).
- On a workstation: `pip install dcli` (Python 3).

## Basics
```bash
dcli +server vcsa01.example.com +skip-server-verification com vmware vcenter vm list
dcli +i +server vcsa01.example.com            # interactive shell with tab completion
dcli +server vcsa01 +formatter json com vmware vcenter cluster list
dcli +server vcsa01 +credstore-add +username administrator@vsphere.local   # cache credentials
```
Commands mirror the API namespaces: `com vmware vcenter ...` (inventory: vm, host, cluster, datastore, network), `com vmware appliance ...` (VAMI functions: networking, NTP, services, update, backup), `com vmware content ...` (content library), `com vmware cis tagging ...` (tags).

## Useful examples
```bash
dcli +server vcsa01 com vmware appliance system version get
dcli +server vcsa01 com vmware appliance health system get
dcli +server vcsa01 com vmware vcenter services list
dcli +server vcsa01 com vmware vcenter vm power start --vm vm-1234
dcli +server vcsa01 com vmware appliance ntp set --servers 10.0.0.10
```
Use `--help` at any level to see operations and parameters.

## Gotchas
- Object IDs are managed object IDs (`vm-1234`, `host-56`), not names; list and filter first (`--names app01`).
- Only API-exposed operations exist; some vSphere Client actions still need PowerCLI/pyVmomi (vim API).
- `+skip-server-verification` is for labs; import the VMCA root into the client trust store instead.
- The credstore file holds credentials; protect the user profile.

## Verify
`com vmware appliance system version get` returns the build; scripted commands return JSON parseable by `jq`.
