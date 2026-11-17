---
id: computing-software.database-administration.oracle-database.asm-disk-groups
name: asm-disk-groups
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-tablespaces, datafiles, asm, asm-diskgroup, asmcmd, rebalance, asm-power-limit, failure-group, external-redundancy, normal-redundancy, afd, asmlib]
level: advanced
status: docs-checked
description: "Create and manage Oracle ASM disk groups: redundancy and failure groups, adding and dropping disks with controlled rebalance, compatibility attributes, and asmcmd checks."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/ostmg/admin-asm-diskgroups.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/ostmg/manage-asm-asmcmd.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/ALTER-DISKGROUP.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASM disk groups

Run as the Grid owner against the ASM instance (`. oraenv` -> `+ASM`, `sqlplus / as sysasm`, or `asmcmd`).

## Redundancy
- `EXTERNAL`: no ASM mirroring; the array does RAID. Common with enterprise SANs.
- `NORMAL`: 2-way mirror across **failure groups**; `HIGH`: 3-way. `FLEX`/`EXTENDED` also exist (per-file redundancy, stretch clusters); see the CREATE DISKGROUP reference.
Failure groups = disks that fail together (same controller/shelf/site). Default: each
disk is its own failure group. Keep failure groups equal in size; free space must allow
re-mirroring after losing one (`REQUIRED_MIRROR_FREE_MB`, `USABLE_FILE_MB` in V$ASM_DISKGROUP).

## Create
```sql
CREATE DISKGROUP data NORMAL REDUNDANCY
  FAILGROUP ctl_a DISK '/dev/oracleafd/disks/DATA01', '/dev/oracleafd/disks/DATA02'
  FAILGROUP ctl_b DISK '/dev/oracleafd/disks/DATA03', '/dev/oracleafd/disks/DATA04'
  ATTRIBUTE 'compatible.asm' = '19.0.0.0', 'compatible.rdbms' = '19.0.0.0',
            'au_size' = '4M';
```
Disks presented via ASM Filter Driver (AFD, prevents non-Oracle writes), ASMLib, or
udev rules with stable names and `oracle:asmadmin` ownership. Use same-size, same-speed
disks in a group. Raising `compatible.rdbms` locks out older database versions; check the attribute rules in the CREATE DISKGROUP reference before changing any `compatible.*` value.
In RAC, mount the group on all nodes (`srvctl start diskgroup -g data`), or create via
`asmca`.

## Add / drop / resize disks (online)
```sql
ALTER DISKGROUP data ADD DISK '/dev/oracleafd/disks/DATA05', '/dev/oracleafd/disks/DATA06' REBALANCE POWER 8;
ALTER DISKGROUP data DROP DISK DATA_0001 REBALANCE POWER 8;   -- disk is released only when rebalance finishes
ALTER DISKGROUP data RESIZE ALL SIZE 2T;                      -- after the LUNs were grown
```
Watch it:
```sql
SELECT group_number, operation, state, power, sofar, est_work, est_minutes FROM v$asm_operation;
```
Do not physically remove a dropped disk until the rebalance has finished and `v$asm_disk.header_status` shows it released (FORMER).
`ASM_POWER_LIMIT` (default 1; range 0-1024 when `COMPATIBLE.ASM` is 11.2.0.2 or higher; 0 cannot be set on Exadata/ODA) sets the default rebalance power; higher is
faster but heavier I/O. A failed disk in NORMAL redundancy goes offline and is
dropped automatically after `disk_repair_time` (default 12 h in 19c; it was 3.6 h in 12c; set e.g. `'6h'`; hours if no unit); fix and
`ALTER DISKGROUP data ONLINE DISK DATA_0003` before then to avoid a full rebalance.

## Day to day
```bash
asmcmd lsdg                       # Free_MB, Usable_file_MB, Req_mir_free_MB, offline disks
asmcmd lsdsk -k -G DATA           # disks, failgroups, paths
asmcmd du +DATA/ORCL              # space per database
asmcmd ls -l +DATA/ORCL/DATAFILE
asmcmd cp +DATA/ORCL/... /tmp/    # copy files in/out of ASM
asmcmd afd_lsdsk                  # AFD labels
asmcmd md_backup /tmp/dg_meta.bak -G DATA   # disk group metadata backup (not data)
```
`Usable_file_MB` negative in NORMAL/HIGH = cannot re-mirror after a failure: add space now.
Alert at ~80 % used, since rebalance and re-mirroring need headroom.

## Gotchas
- Never write over a device that is an ASM disk; check `v$asm_disk.header_status` first.
- Keep disks in a group the same size: mixed sizes make usable space depend on the failure-group layout.
- Dropping a disk with `FORCE` skips copying and relies on mirrors: only for dead disks in NORMAL/HIGH.

## Verify
- [ ] `asmcmd lsdg`: no offline disks, Usable_file_MB > 0, used % within threshold.
- [ ] Disk group metadata backed up (`md_backup`) after changes.
- [ ] `compatible.*` attributes recorded before any upgrade plan.

## Checked
Date 2026-10-22. Oracle Database 19c SQL Language Reference (ALTER DISKGROUP), Database Reference (ASM_POWER_LIMIT) and
ASM Administrator's Guide as indexed by search. Confirmed: REBALANCE POWER range 0-1024, `DROP DISK ... FORCE` semantics
(not for external redundancy), `RESIZE ALL SIZE`, `ONLINE DISK`, ASM_POWER_LIMIT default 1 and range, `md_backup`
(`-G`), `afd_lsdsk`, `lsdg`/`lsdsk -G`. Corrected: DISK_REPAIR_TIME default is 12 h in 19c (3.6 h was the 12c default).
Removed unconfirmed: combined ADD/DROP example, 12.2+ gate for FLEX/EXTENDED, kfed advice. The two original source URLs
returned 404 to a fetch and were replaced.
Method: documentation only; no commands were run.
