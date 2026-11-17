---
id: computing-software.systems-network-administration.windows-server.iis-migration-with-web-deploy
name: iis-migration-with-web-deploy
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, workload-migration, server-migration, web-deploy, msdeploy, iis, iis-migration, sync-webserver]
level: practitioner
status: docs-checked
description: "Migrate IIS sites between servers with Web Deploy (msdeploy): install, dependency check, package or live sync, skip rules, certificates and post-migration checks."
sources:
  - https://learn.microsoft.com/en-us/iis/publish/using-web-deploy/synchronize-iis
  - https://learn.microsoft.com/en-us/iis/publish/using-web-deploy/introduction-to-web-deploy
  - https://learn.microsoft.com/en-us/iis/publish/using-web-deploy/migrate-a-web-site-from-iis-60-to-iis-7-or-above
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrate IIS sites with Web Deploy

## Install
Install Web Deploy on source and destination. For live sync, install the Remote Agent Service (MsDepSvc) on whichever
side you push to or pull from; non-administrator deployers connect through the Web Management Service handler that
Web Deploy installs. Give the destination the same IIS features: compare `Get-WindowsFeature Web-*` on both.

## Check dependencies
```cmd
msdeploy -verb:getDependencies -source:apphostconfig="Default Web Site"
```
Lists the modules and components the site needs (see Viewing Web Site Dependencies in Microsoft's docs). Install them
on the destination first.

## Package then deploy (offline)
```cmd
msdeploy -verb:sync -source:apphostconfig="Shop" -dest:package=<package-zip>
msdeploy -verb:sync -source:package=<package-zip> -dest:apphostconfig="Shop" -whatif > dryrun.log
msdeploy -verb:sync -source:package=<package-zip> -dest:apphostconfig="Shop"
```
`-whatif` is an optimistic preview: it does not catch every failure (for example inability to write to the
destination), so check the result afterwards.

## Live sync (push or pull)
```cmd
msdeploy -verb:sync -source:apphostconfig="Shop" -dest:apphostconfig="Shop",computername=WEB02 -whatif
msdeploy -verb:sync -source:apphostconfig="Shop",computername=WEB01 -dest:apphostconfig="Shop"
```
Run the same command without `-whatif` once the preview looks right.

## Check manually after migration
Web Deploy has providers for configuration (appHostConfig), GAC assemblies (gacAssembly), COM objects
(comObject32/64) and databases, but do not assume everything moves. Verify by hand: TLS certificates and their
bindings, app pool identity passwords, machine keys, registry settings, ODBC DSNs and scheduled tasks.

## Verify
- [ ] Sites start, bindings correct, app pools running under the right identities; hosts-file test before the DNS
  cutover.

## Checked
Date 2026-10-27. Documentation: Microsoft pages "Synchronize IIS" (quick guide) and "Introduction to Web Deploy".
Confirmed: getDependencies, sync with package and computername, `-whatif` caveat, Remote Agent Service and Web
Management Service roles, provider names. Skip rules, link options and remote-endpoint URL syntax are not stated.
Method: documentation only; no commands were run.
