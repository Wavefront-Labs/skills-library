---
id: manufacturing-production.industrial-automation-plc-programming.aveva-wonderware.system-platform-templates-galaxy-deployment-and-intouch
name: system-platform-templates-galaxy-deployment-and-intouch
category: manufacturing-production
field: industrial-automation-plc-programming
product: aveva-wonderware
tags: [aveva-wonderware, aveva, wonderware, system-platform, archestra, archestra-ide, galaxy, galaxy-repository, application-object, derived-template, object-template, $userdefined, platform, appengine, area-object, device-integration, di-object, oi-server, dasabcip, dassidirect, intouch, intouch-for-system-platform, omi, managed-intouch, historian, galaxy-backup, deploy, undeploy, scada, hmi, industrial-automation-plc-programming]
level: practitioner
status: draft
description: "Build an AVEVA System Platform galaxy: base-to-derived template hierarchy, platform/engine/area model, device integration, safe deploy/undeploy, and InTouch or OMI graphics bound to objects."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# System Platform templates, galaxy deployment and InTouch

**Goal:** a Wonderware/AVEVA System Platform galaxy where a change to "every pump"
is one template edit, deployments don't drop production data, and graphics bind to
objects rather than to thousands of loose tags.

*Draft: based on System Platform 2017–2023 R2 usage. Product names have changed
repeatedly (ArchestrA IDE → System Platform IDE, OI Servers replaced DAServers);
confirm names for your release.*

## 1. Object model
- **Galaxy** = the configuration database (on the Galaxy Repository node, SQL Server).
- **WinPlatform** object per PC → **AppEngine(s)** that execute objects → **Area**
  objects that group objects for alarms and security → application objects.
- **Device Integration**: a DI object (or OI Server, e.g. ABCIP for Logix, SIDirect
  for S7) owns the PLC connection; application objects reference its scan groups.
- Spread AppEngines across platforms for load; redundancy pairs need a dedicated
  redundancy network/NIC configuration.

## 2. Template hierarchy (the whole point)
- Never instantiate base templates (`$UserDefined`, `$AnalogDevice`) directly.
- Create a **company base**: `$cUserDefined` derived from `$UserDefined` with your
  standard attributes and scripts. Then device templates: `$cPump` → `$cPump_VSD`.
- **Lock** attributes in the template that instances must not change (padlock icon);
  leave unlocked only what differs per instance (I/O reference, description).
- Contained objects (a `$cValve` inside `$cSkid`) build composite equipment; the
  hierarchical name (`Skid101.InletValve`) reads naturally on screens.
- Put graphics (**ArchestrA/industrial graphics symbols**) on the template; instances
  inherit them. A symbol edit propagates on next deploy.

## 3. Deploy and undeploy safely
- Changing a template marks instances as **"pending changes"** (orange). They only take
  effect when **redeployed**.
- Redeploy restarts the object: its scripts reinitialise, alarms may clear and
  re-raise, history may show a short gap. Do it at a quiet point and tell operators.
- **Cascade deploy** from an engine redeploys everything below — powerful and
  dangerous on a running plant. Prefer selecting the changed objects.
- Undeploying a platform takes down everything it hosts, including InTouch runtime
  on that node.
- Use **check-out/check-in** with comments; multiple engineers editing the same object
  will block each other, which is the point.

## 4. Graphics: InTouch for System Platform / OMI
- Managed InTouch applications or **OMI** (Operations Management Interface) ViewApps
  are deployed from the galaxy. Bind symbols to object references
  (`Me.PV`, `Pump101.Running`) and use **owning-object relative references** so one
  symbol works for every instance.
- Standalone (non-managed) InTouch with its own tagname dictionary still exists in many
  plants; migrating needs a plan for every script that references tags by name.

## 5. Backups and versions
- **Galaxy backup** (.cab) from the System Management Console before every change
  session. Export templates (.aaPKG) to a library for reuse across galaxies.
- Restoring a galaxy onto a newer System Platform version upgrades it; you can't go back.

## Gotchas
- Scripts set to "execute on scan" with no trigger run every scan — CPU load creep.
- Historised attribute with a tiny deadband floods Historian storage.
- Security: OS-group-based security relies on domain groups; a misconfigured group can
  lock operators out of acknowledging alarms.
- Time sync across nodes matters for alarm ordering — point every node at one NTP source.

## Verify
- [ ] Every instance derives from a company template; no direct base instances.
- [ ] No objects left in "pending changes" or "undeployed" state unexpectedly.
- [ ] A recent galaxy backup exists and was taken before today's changes.
- [ ] One symbol edit reflected on all instances after deploy.
- [ ] Alarm and history continuity checked after redeploy.
