---
id: computing-software.systems-network-administration.windows-server.iis-appcmd-and-shared-configuration
name: iis-appcmd-and-shared-configuration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, iis, appcmd, iis-shared-configuration, applicationhost-config, web-farm]
level: advanced
status: docs-checked
description: "Manage IIS from the command line with appcmd, back up and restore applicationHost.config, and use IIS Shared Configuration to keep web farm nodes identical."
sources:
  - https://learn.microsoft.com/en-us/iis/get-started/getting-started-with-iis/getting-started-with-appcmdexe
  - https://learn.microsoft.com/en-us/iis/web-hosting/configuring-servers-in-the-windows-web-platform/shared-configuration_211
  - https://learn.microsoft.com/en-us/iis/get-started/whats-new-in-iis-8/iis-80-centralized-ssl-certificate-support-ssl-scalability-and-manageability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IIS appcmd and shared configuration

## appcmd basics (`%windir%\system32\inetsrv\appcmd.exe`)
```cmd
appcmd list sites /state:Stopped
appcmd list apppools /state:started
appcmd add site /name:Shop /bindings:https/*:443:shop.example.com /physicalPath:<WEB_ROOT>\shop
appcmd set apppool Shop /managedRuntimeVersion:""
appcmd set config Shop -section:system.webServer/httpErrors /errorMode:Custom /commit:apphost
appcmd recycle apppool Shop
appcmd list config Shop -section:system.webServer/security/authentication/windowsAuthentication
```
`/commit:apphost` writes to applicationHost.config instead of the site's web.config; some sections (for example
`asp`) are locked by default and give a lock violation error unless you commit at server level or unlock them.
The binding string is `protocol/IP:port:hostheader`. Check HTTPS bindings still need a certificate bound in http.sys.

## Config backup and restore
```cmd
appcmd add backup "before-change"
appcmd list backups
appcmd restore backup "before-change"
```
A backup holds the current applicationHost.config plus related server-wide state (FTP and IIS Administration Tool
configuration). Without a name, appcmd names it from the date and time. Take one before any server change.

## Shared configuration (web farms)
Stores applicationHost.config, administration.config and the IIS/ASP.NET encryption keys (exported as
`configEncKey.key`) on a share. Not shared: machine.config, root web.config, site web.config files and content,
custom modules and installed modules.
1. Create a restricted account (domain account, or a local account on each machine if not domain joined) with read
   access to a share created for the config, for example with `net share <name>$=<path> /grant:<account>,Read`.
2. On the first server: IIS Manager > server > **Shared Configuration** > Export Configuration to the share path,
   with Connect As credentials and an encryption key password.
3. On every node: tick Enable shared configuration, enter the path, account and password, Apply, then supply the
   encryption key password.
4. Content stays local (deploy it) or on a share.

## Gotchas
- Installed modules must be configured the same way on every node; they are not part of the shared config.
- Certificates for HTTPS bindings need to be on each node or served from the Centralized SSL Certificate Support
  share (files named `<CN>.pfx`, wildcard written `_.domain.pfx`; an optional IIS 8.0+ component that needs a file
  share alongside the shared-configuration share).

## Verify
- [ ] `appcmd list backups` shows a pre-change backup; on a farm, a change on node 1 appears on node 2's
  `appcmd list sites`.

## Checked
Date 2026-10-27. Documentation: IIS getting started with appcmd, Shared Configuration, IIS 8.0 Centralized SSL
Certificate Support pages. Confirmed: command forms, backup behaviour, shared config contents and setup, lock
behaviour, CCS file naming. Backup folder location and automatic configuration history figures are not stated.
Method: documentation only; no commands were run.
