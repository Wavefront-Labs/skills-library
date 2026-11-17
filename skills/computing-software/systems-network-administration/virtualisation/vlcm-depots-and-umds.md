---
id: computing-software.systems-network-administration.virtualisation.vlcm-depots-and-umds
name: vlcm-depots-and-umds
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [umds, vlcm-depot, vlcm, lifecycle-manager, offline-bundle, air-gapped-patching, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Feed vSphere Lifecycle Manager from online depots, offline bundles or UMDS for air-gapped vCenters, including the Broadcom download token URL change and depot troubleshooting."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/managing-host-and-cluster-lifecycle/working-with-vsphere-lifecycle-manager-depots/installing-setting-up-and-using-update-manager-download-service.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vLCM depots and UMDS

vLCM builds images and baselines from **depots**: online (vendor URLs), offline bundles
imported into vCenter, or a UMDS-served share for vCenters without internet.

## Online depots
Lifecycle Manager → Settings → Patch Downloads / Patch Setup. The URLs of the official
online depot are now unique for each customer; update the download-source URLs per the
Broadcom KB articles the UMDS documentation links (KB 390121 / KB 390123). Sync: Actions →
Sync Updates.

## Offline bundles
Lifecycle Manager → Actions → **Import Updates** → upload the ESXi offline bundle zip or
vendor add-on zip. Use for one-off vendor drivers or when internet is blocked and UMDS is
overkill.

## UMDS (air-gapped)
UMDS (Update Manager Download Service) is a separate, Linux-only install (Windows is no
longer supported) running on a host with internet: download the updates with UMDS, then
export the downloads so they become available to Lifecycle Manager.
Serve the export over HTTP(S) inside the secure zone (or carry it across on media — the
documentation also covers a portable media drive as a download source) and set vLCM's
download source to that web server folder. Automate the download/export on a schedule.

## Gotchas
- UMDS version must match the vCenter major version.
- Self-signed HTTPS on the internal depot: import the CA into vCenter trusted roots or
  sync fails silently with certificate errors in `vmware-updatemgr` logs.
- Depot content does not delete itself; old bundles accumulate in the Update Manager
  storage, filling the partition. Delete unused images/baselines.
- Logs: the `vmware-updatemgr` service logs.

## Verify
Lifecycle Manager → Updates shows new patches with today's release dates; Image
Depot lists the expected ESXi versions and vendor add-ons.

## Checked
2026-10-31: Confirmed the per-customer depot URLs, the Linux-only UMDS install, the
UMDS/vLCM version-match rule and the export-to-web-server workflow against the
"Installing, Setting Up, and Using the Update Manager Download Service" and "Using UMDS"
pages; the vmware-updatemgr service name against the vCenter services KB. Removed the
unconfirmed vmware-umds command flags, the dl.broadcom.com URL template, the ISO `umds`
folder claim and the /storage/updatemgr path.
Method: documentation only; no commands were run.
