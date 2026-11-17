---
id: computing-software.it-support-helpdesk.servicenow.backout-plan-for-changes
name: backout-plan-for-changes
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, change-management, change-enablement, backout-plan, rollback, go-no-go, itil-4]
level: practitioner
status: draft
description: "Plan a backout before any change: decision trigger and deadline, tested rollback steps, data/state captured beforehand, time budget inside the window, and who calls it."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://learn.microsoft.com/en-us/windows/deployment/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# backout-plan-for-changes
Goal: if the change goes wrong you can get back to the known-good state
inside the window, without improvising at 2am.

## The four parts of a usable backout plan
1. **Trigger**: objective conditions that force backout, written before
   the change. "Any of: VPN login test fails from two sites, error rate
   > 2% for 10 min, step 6 not complete by 01:30."
2. **Point of no return**: the step after which backout changes shape
   (e.g. after the database schema migration, rollback means restore, not
   uninstall). Mark it in the implementation plan.
3. **Steps**: numbered, with commands, as detailed as the forward plan.
   "Reinstall previous version" is not a step; the installer path, version
   number and config restore command are.
4. **Owner and time**: who decides (change owner or on-call manager) and
   how long backout takes. Implementation + verification + backout must
   fit in the window.

## Capture state before you start
- Config exports: device configs, GPO backups (`Backup-GPO -All -Path`),
  Intune policy JSON exports, registry exports of keys you will touch.
- Snapshots/backups: VM snapshot or backup job confirmed successful (not
  just scheduled). Snapshots are short-term; delete after sign-off.
- Versions: record current firmware/app/driver versions and keep the old
  installer media on hand (vendors pull old downloads).
- For endpoint rollouts: keep the previous app version assignment and a
  pilot ring so backout is "reassign", not "rebuild".

## Test the backout
In the lab or pilot, perform the backout once. A rollback that has never
run is a hope. For irreversible changes (data migrations, certificate
replacement with revoked old cert), say so explicitly and get the approver
to accept a fix-forward plan instead.

## Gotchas
- Backout that depends on the thing you are changing (remote access to a
  firewall you are upgrading) needs out-of-band access (console, iLO).
- Partial success is the hard case: decide in advance whether 1 of 2
  nodes upgraded counts as backout or proceed.
- Teams continue "just one more fix" past the trigger time; the change
  owner calls it at the deadline.

## Verify
Backout trigger, steps, timing and owner are written in the RFC, and the
backout was rehearsed or the irreversibility was signed off.
