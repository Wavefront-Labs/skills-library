---
id: computing-software.systems-network-administration.syncthing.introducer-devices
name: introducer-devices
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, introducer, device-introduction, auto-add]
level: practitioner
status: docs-checked
description: "Use a Syncthing introducer so new devices on shared folders are added automatically, and avoid mutual introducers."
sources: ["https://docs.syncthing.net/users/introducer.html", "https://docs.syncthing.net/users/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Introducer devices

## Concept
The introducer feature lets a device automatically add new devices. When two devices connect they exchange a list of mutually shared folders and the devices connected to those shares. Marking a remote device R as an introducer lets your device L add R's other peers. Example: L and R share Pictures, and R also shares it with A and B. L then adds A and B as if R had introduced them. Device C, who only shares Videos with R, is not added because L does not share that folder.

## Setting it
Edit the remote device in the GUI and check the option under the Sharing tab. In the configuration it is the device's `introducer` attribute ("trusted as an introducer, i.e. we should copy their list of devices per folder when connecting").

## What is copied
Device IDs, labels and configured address settings are autoconfigured; no other device-specific settings are. Autoconfiguration is applied only once per offered device, when the device connects to an introducer (a restart after configuring the introducer forces this), and later settings are not updated from the introducer.

## Ongoing behaviour
- If an introducer adds or removes devices or shares, or changes device-share settings, the change is reflected on your next connection. A device that is no longer on the introducer, or no longer shares mutual folders, is removed when devices next connect to the introducer. `skipIntroductionRemovals` (device attribute) makes you follow introductions but not de-introductions.
- If you manually remove an introduced device or unshare it from a folder, it is re-added automatically as long as the introducer is still marked as such.
- Introducer status is transferable: an introducer's introducer becomes your introducer as well.

## Warning
The docs say it is not a good idea to set two devices as introducers of each other. Adding works, but removing a device may be a problem, as the two devices constantly re-introduce the removed device to each other.

## Related
The device `autoAcceptFolders` setting automatically adds and syncs folders shared from that remote device under the default path; it is a separate feature.

## Checked
2026-11-04. Read Introducer Configuration and the config page (`introducer`, `skipIntroductionRemovals`, `introducedBy`, `autoAcceptFolders`): the L/R/A/B/C example, GUI path, what is autoconfigured and when, change propagation, re-adding, transferability and the mutual-introducer warning.
Method: documentation only; no commands were run.
