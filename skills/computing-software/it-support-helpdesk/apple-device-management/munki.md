---
id: computing-software.it-support-helpdesk.apple-device-management.munki
name: munki
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, app-automation, munki, manifests]
level: practitioner
status: docs-checked
description: "Deploy software with Munki catalogs, manifests and repos, including managed installs, optional installs and update checks."
sources:
  - "https://github.com/munki/munki/wiki"
  - "https://github.com/munki/munki/wiki/managedsoftwareupdate"
  - "https://github.com/munki/munki/wiki/Manifests"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# munki

Goal: a self-hosted software repo and client for Macs.

## Repo
- The server is simply a web server serving a file tree (pkginfo, catalogs, manifests, pkgs); any platform or cloud
  storage works, and the Munki tools are not needed on it.
- A Mac with the Munki admin tools creates the content: `munkiimport` imports installers, `makepkginfo` creates pkginfo
  metadata for an installer (edit it afterwards), `makecatalogs` builds catalogs from pkginfo files, `manifestutil`
  edits manifests.
- Every client has the tools in `/usr/local/munki/` and `Managed Software Center.app`.

## Manifests
- A manifest names the catalogs to search and lists items by their pkginfo `name` (case-sensitive): `managed_installs`
  (installed and kept up to date), `optional_installs` (offered in Managed Software Center), `managed_uninstalls`,
  `managed_updates`, and `included_manifests`.
- Catalog order matters: the first catalog with a match stops the search, so list a testing catalog before production
  only for clients meant to test.
- The client requests its manifest by `--id`, else the `ClientIdentifier` in `/Library/Preferences/ManagedInstalls.plist`,
  else its fully qualified hostname, short hostname, serial number, then `site_default`.

## Client
- `/usr/local/munki/managedsoftwareupdate` runs automatically about hourly. `--checkonly` (the default with no other
  option) checks without installing; `--installonly` installs what was downloaded. From Munki 7.2, `--installonly` skips
  items with running blocking applications or needing a logout or restart unless `--force` is used.
- `--show-config` prints the effective configuration; `--id=ID` overrides the identifier for one run.
- Only the current Munki release is supported. Munki 7 no longer includes Python.

## Practice
Use separate catalogs (for example testing and production) and back up the repo, which holds every package version and
all manifests.

## Gotchas
`makecatalogs` builds the catalogs from your pkginfo files, so rebuild them after adding or editing items.

## Checked

2026-11-09: confirmed on the Munki wiki home, managedsoftwareupdate and Manifests pages (read from the wiki's raw
markdown): server needs, tools, client options and 7.2 behaviour, manifest keys, catalog search order, manifest lookup
order. Removed: the Installomator and AutoPkg wiki sources, the claim that an MDM installs the client and preference, the
promotion delay wording. The `makecatalogs` wiki page was not available; its role is taken from the home page.

Method: documentation only; no commands were run.

## Verify
The client log shows the new item installed and Managed Software Center lists the optional items.
