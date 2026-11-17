---
id: computing-software.systems-network-administration.active-directory.ad-forest-recovery-plan
name: ad-forest-recovery-plan
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-recovery, ad-backup, forest-recovery, authoritative-sysvol, krbtgt-reset, rid-pool-raise, disaster-recovery, ransomware-recovery]
level: sme
status: docs-checked
description: "Plan and execute AD forest recovery: backups to keep, isolated restore of one DC per domain, metadata cleanup, RID and krbtgt resets, and staged redeployment."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-guide
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-steps-for-restoring-the-forest
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-reset-the-krbtgt-password
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-authoritative-recovery-sysvol
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD forest recovery plan

For when the whole forest has to be returned to its state before a forest-wide failure. Microsoft's AD Forest Recovery
Guide says forest recovery should in many cases be the last option and that you should work with Microsoft Support to
determine the cause and evaluate remedies first. This skill summarizes that guide.

## Prepare now
- Back up system state of DCs regularly; restore only from a backup within the tombstone lifetime (default 180 days).
- Follow the guide's assumption of one AD-integrated DNS zone per AD domain; if you do not have that, plan DNS
  recovery yourself.
- Rehearse the recovery regularly, as the guide recommends, to practise it and to check that your custom steps and your
  choice of DCs to restore in each domain still work.
- Account for disk-volume protection such as BitLocker when planning access to DC volumes.

## Recovery sequence (the guide's five phases)
1. **Identify the problem**: scope and likely causes with IT, Microsoft Support and business stakeholders.
2. **Determine how to recover** the forest and complete the preliminary steps.
3. **Perform the initial recovery**: in isolation, recover one DC per domain, clean it and reconnect the domains. In this
   phase, reset privileged accounts and fix problems caused by security breaches. The guide's steps for it include:
   - restore the DC from backup and make SYSVOL authoritative (edit `msDFSR-Options`, or use `wbadmin -authsysvol` when
     restoring a system state backup to the same hardware and OS instance; a bare-metal restore needs the attribute edit);
   - seize operations master roles with ntdsutil (see fsmo-role-seizure);
   - clean the metadata of removed DCs;
   - raise the RID pool value (`rIDAvailablePool`) and invalidate the current RID pool (see rid-master-and-rid-pool);
   - reset the `krbtgt` password **twice**, waiting 10 hours between resets (the default maximum ticket lifetimes; wait
     longer if you changed them); the account keeps a password history of 2. This applies to writable DCs, not RODCs, and
     the `krbtgt_<number>` accounts of RODCs you plan to recover must not be deleted;
   - reset the trust passwords with `netdom trust <domain> /domain:<other> /resetOneSide /passwordT:<password>` on each
     side (use the same `passwordT` value on both sides);
   - reset the DC's computer account password with `Reset-ComputerMachinePassword`, and run it a second time;
   - add the global catalog role as needed and configure DNS.
4. **Redeploy the remaining DCs**: adapt to your design; virtualized DC cloning can speed this up.
5. **Clean up**: reconfigure name resolution as needed and get line-of-business applications working.

## Gotchas
- You cannot use the backup of an RODC to restore a writable DC.
- Virtual DC snapshots are not a supported backup (see virtual-dc-generation-id-safeguards).
- The recovery steps are designed so recovered DCs do not replicate with dangerous writable DCs, but only taking
  writable DCs offline guarantees that no replication occurs.

## Verify
- [ ] A rehearsal of the recovery has been run and timed, and the plan updated from it.

## Checked

Documentation: Microsoft Learn "AD Forest Recovery Guide" pages (prerequisites, steps to restore the forest, authoritative
SYSVOL recovery, seizing operations master roles, raising and invalidating RID pools, resetting the krbtgt password,
resetting trust and computer account passwords), from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: the five phases, SYSVOL authoritative restore methods, krbtgt reset twice with a 10-hour wait and password
history of 2, `netdom ... /resetOneSide` with a matching `/passwordT`, `Reset-ComputerMachinePassword` run twice, RODC
krbtgt_ warning, RODC backups cannot restore a writable DC. Removed unconfirmed claims: "two DCs per domain" backups,
Windows LAPS DSRM backup, the specific "+100000" RID figure as an instruction, the ransomware section and
`repadmin /replsummary`. The guide's "nonauthoritative restore in DSRM" step was not individually checked here.

Method: documentation only; no commands were run.
