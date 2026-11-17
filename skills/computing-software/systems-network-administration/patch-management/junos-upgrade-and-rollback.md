---
id: computing-software.systems-network-administration.patch-management.junos-upgrade-and-rollback
name: junos-upgrade-and-rollback
category: computing-software
field: systems-network-administration
product: patch-management
tags: [junos-upgrade, network-device-upgrade, network-rollback, image-verification, juniper, issu]
level: advanced
status: gated
description: "Upgrade Juniper Junos devices safely: storage cleanup, image validation, request system software add options, dual-RE and Virtual Chassis notes, snapshots and rollback."
sources:
  - https://www.juniper.net/documentation/us/en/software/junos/software-installation-and-upgrade/index.html
  - https://www.juniper.net/documentation/us/en/software/junos/cli-reference/topics/ref/command/request-system-software-add.html
  - https://www.juniper.net/documentation/us/en/software/junos/cli-reference/topics/ref/command/request-system-software-rollback.html
  - https://www.juniper.net/documentation/us/en/software/junos/cli-reference/topics/ref/command/request-system-software-in-service-upgrade.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Junos upgrade and rollback

## Prepare
- Pick the JTAC recommended release for the platform (Juniper publishes a recommended-releases list in its knowledge base; look it up there); read release notes and upgrade paths (some need intermediate releases).
- Backup config off-box: `show configuration | display set | save scp://...`, plus your
  config backup system (Oxidized/RANCID).
- Check storage: `show system storage`; clean: `request system storage cleanup`.
- Console/out-of-band access available.

## Copy and verify image
```
file copy scp://user@repo.corp.example/junos/<package>.tgz /var/tmp/
file checksum sha256 /var/tmp/<package>.tgz      # compare with Juniper download page (gated: unconfirmed, source is paywalled or blocked)
```

## Install
```
request system software validate /var/tmp/junos-...tgz          # config compatibility check
request system software add /var/tmp/junos-...tgz no-copy reboot
```
Options listed in the CLI reference for `request system software add`: `no-copy`, `no-validate` (avoid), `unlink` (remove the package after install), `reboot`, `validate`, `force`, and `member <id>` (MX Virtual Chassis only, id 0 or 1). Other Virtual Chassis platforms use platform-specific options: check the CLI reference for your platform.
Dual Routing Engines: upgrade backup RE first, switchover (`request chassis routing-engine
master switch`), upgrade the other; or use **ISSU** (`request system software in-service-upgrade`)
on supported platforms, with the redundancy features that platform's ISSU documentation requires.
SRX clusters: ISSU or a node-by-node procedure; the ISSU page says to fail over so all redundancy groups are active on one device first, and recommends graceful restart for routing protocols.

## After reboot
```
show version
show system alarms
show chassis alarms
show interfaces terse | match down
request system snapshot slice alternate     # copy running to backup partition (EX/QFX/SRX branch)
```
Compare routing/BGP/OSPF neighbours and LLDP with the pre-change capture.

## Rollback
- Software: `request system software rollback` (reverts to the last successfully installed package) then reboot;
  or boot the alternate partition (`request system reboot slice alternate media internal`)
  if you didn't snapshot after upgrade.
- Config: `rollback 1` / `rollback <n>` then `commit` (separate from software rollback).

## Gotchas
- Snapshot the alternate slice only **after** validating the new release, otherwise you lose
  the fallback.
- Upgrades crossing major versions may change default behaviour; review "Changes in
  behavior" sections.

## Verify
`show version` on all members shows the target; alarms clear; pre/post diff of neighbours,
routes count and interface state matches.

## Checked
Date: 2026-10-27. Documentation: Juniper Junos CLI reference pages for request system software add, validate, rollback, in-service-upgrade, request system snapshot, request system reboot (slice and media options), request system storage cleanup and request chassis routing-engine master switch (all confirmed to exist with the options used). Removed the unconfirmed KB number, the example package name, `all-members` for add and ICU. The file checksum command page could not be read, so its use is gated.
Method: documentation only; no commands were run.
