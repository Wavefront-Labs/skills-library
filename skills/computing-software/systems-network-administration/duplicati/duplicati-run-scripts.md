---
id: computing-software.systems-network-administration.duplicati.duplicati-run-scripts
name: duplicati-run-scripts
category: computing-software
field: systems-network-administration
product: duplicati
tags: [run-script-before, run-script-after, script-exit-codes, run-script-timeout, run-script-post-backup, script-log-prefixes]
level: advanced
status: docs-checked
description: "Run scripts before and after Duplicati operations, control whether the operation proceeds with exit codes and write log entries from script output."
sources: ["https://docs.duplicati.com/detailed-descriptions/automation-and-integration/scripts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running scripts before and after Duplicati operations

Script options hook into backups and other operations for preparation (such as locking a database), cleanup or notification.
- `--run-script-before`: runs first; the operation blocks until it ends or times out.
- `--run-script-before-required`: same, but a non-zero exit code or a timeout aborts the operation.
- `--run-script-after`: runs on exit and receives the operation results on stdout.
- `--run-script-post-backup`: runs after the data is written and snapshots (such as VSS) are released, before remote verification and compacting.
- `--run-script-timeout`: default 60s, formats like 30s or 1m15s; `0` waits forever. After a timeout on a non-required script, a warning is logged and the operation continues; no output is captured.
- `--run-script-with-arguments=true` parses the script value as a command line with quoted arguments.
- `--run-script-result-output-format` (`Duplicati` default or `Json`), `--run-script-log-level` (default Warning) and `--run-script-log-filter` shape the results passed to after-scripts.

Exit codes for the before scripts: 0 OK run; 1 OK do not run; 2 warning run; 3 warning do not run; 4 error run; 5 error do not run; anything else error do not run. For the after script the operation has finished, so the do-not-run codes act like the run codes (1 as 0, 3 as 2, 5 as 4). Non-required before scripts only log a warning for a non-zero exit.

Logging from scripts: stdout lines starting with `LOG:INFO`, `LOG:WARN` or `LOG:ERROR` become entries at that severity in the Duplicati log and in reports, for example `echo "LOG:WARN Database backup older than 24 hours detected"`.

## Checked

2026-11-04. Confirmed against the Scripts page. Fixed the before-required wording (any non-zero exit code or a timeout aborts; the script header lists allowed codes 0, 2, 4) and the LOG:WARN example text to match the page.

Method: documentation only; no commands were run.
