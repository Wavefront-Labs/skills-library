---
id: computing-software.database-administration.oracle-database.autoupgrade-utility
name: autoupgrade-utility
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, oracle-database, oracle-patching, opatch, autoupgrade, upgrade-to-19c, upgrade-to-23ai, non-cdb-to-pdb, guaranteed-restore-point, analyze-mode]
level: advanced
status: docs-checked
description: "Upgrade Oracle databases with AutoUpgrade: config file, analyze/fixups/deploy modes, guaranteed restore point fallback, non-CDB to PDB conversion and job monitoring."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/upgrd/autoupgrade-command-line-parameters.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/26/upgrd/autoupgrade-command-line-parameters.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/26/upgrd/upgrade-parameters-autoupgrade-config-file.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AutoUpgrade

**Goal:** a repeatable, logged upgrade (e.g. 12.2/18c/19c → 19c/23ai) with prechecks
and an automatic fallback point, the method Oracle recommends over DBUA/manual.

## Get the latest jar
Oracle recommends downloading the most recent AutoUpgrade from My Oracle Support Document 2485457.1 and using that `autoupgrade.jar` to prepare and deploy the upgrade.

## Config file
```
global.autoupg_log_dir=/u01/autoupgrade/logs
upg1.source_home=/u01/app/oracle/product/19.0.0/dbhome_1
upg1.target_home=/u01/app/oracle/product/26.0.0/dbhome_1
upg1.sid=ORCL
upg1.restoration=yes                    # default; creates a guaranteed restore point (needs a fast recovery area; use no for NOARCHIVELOG and Standard Edition)
upg1.target_cdb=CDB26                    # mandatory only to upgrade and convert a non-CDB into this CDB as a PDB (case-sensitive SID)
upg1.timezone_upg=yes                   # default yes for upgrade, no for patching
```

## Modes
```bash
java -jar autoupgrade.jar -config orcl.cfg -mode analyze   # read-only prechecks; report in logs (HTML/JSON)
java -jar autoupgrade.jar -config orcl.cfg -mode fixups    # prechecks plus preupgrade fixups, no upgrade
java -jar autoupgrade.jar -config orcl.cfg -mode deploy    # upgrade start to finish (modes also include upgrade and postfixups)
```
In the interactive console (`upg>` prompt): `-lsj`, `-status -job 100`, `-tasks`, `-resume -job 100`, `-stop -job 100`.
Run deploy inside `screen`/`tmux` or with `-noconsole` (console disabled).

## Fallback
With `restoration=yes` (default), AutoUpgrade creates a guaranteed restore point (GRP). Add `-restore_on_fail` to a deploy to restore failed jobs automatically, or restore by hand:
```bash
java -jar autoupgrade.jar -config orcl.cfg -restore -jobs 100
```
This flashes the databases back to the GRP, which AutoUpgrade must already have created. After `COMPATIBLE` is raised, downgrade is not possible, and with `raise_compatible=yes` the GRP must be deleted before the upgrade starts. For unplug-plug flows the default `nocopy` option leaves no recovery of the source PDB: back it up.

## Gotchas
- Don't raise `COMPATIBLE` until after a soak period; doing so removes the downgrade/flashback path.
- Analyze reports items that need manual action before deploy: fix them first.
- Data Guard: follow the documented upgrade sequence for the standby (not covered here).

## Verify
Check the job status in the console (`-status -job <n>`) and the logs under `global.autoupg_log_dir`; `SELECT version_full FROM v$instance;` and `dba_registry` components VALID.

## Checked
Date 2026-10-22. Oracle AI Database 26ai Upgrade Guide (command-line parameters, upgrade parameters) and 19c
spucs/upgrd pages as indexed by search. Confirmed: `-config`, `-mode` values, `-restore -jobs`, `-noconsole`,
`restore_on_fail`, console commands (`-lsj`, `-status`, `-tasks`, `-resume`, `-stop`), `restoration` default yes and
needs FRA, `target_cdb`, `timezone_upg` default, MOS note 2485457.1 recommendation, COMPATIBLE and GRP caveat.
Corrected: there is no `abort` console command (use `-stop -job`); removed Java 8 and `$ORACLE_HOME/jdk`, fixups
detail list and status.html path (not confirmed). Replaced 404 source URLs (19 using-autoupgrade page, 23 path).
Method: documentation only; no commands were run.
