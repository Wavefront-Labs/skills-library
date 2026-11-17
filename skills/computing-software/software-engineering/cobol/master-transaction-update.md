---
id: computing-software.software-engineering.cobol.master-transaction-update
name: master-transaction-update
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, master-transaction-update, cobol-batch-patterns, master-update, balance-line, match-merge, checkpoint-restart]
level: advanced
status: draft
description: "Apply sorted transactions to a sorted master with the balance-line algorithm, with restart in mind."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Master file / transaction file update (match-merge)
**Goal:** a robust nightly update.

```cobol
PERFORM UNTIL WS-MASTER-KEY = HIGH-VALUES AND WS-TRAN-KEY = HIGH-VALUES
    EVALUATE TRUE
        WHEN WS-MASTER-KEY < WS-TRAN-KEY
            WRITE NEW-MASTER-REC FROM OLD-MASTER-REC
            PERFORM READ-MASTER
        WHEN WS-MASTER-KEY = WS-TRAN-KEY
            PERFORM APPLY-TRAN
            PERFORM READ-TRAN
        WHEN OTHER
            PERFORM ADD-NEW-FROM-TRAN
            PERFORM READ-TRAN
    END-EVALUATE
END-PERFORM
```
- Set the key to `HIGH-VALUES` at end of each file so the loop drains the other.
- Write a new master (old master stays untouched) so a failed run is rerun from the same inputs.
- Checkpoint/restart: record last processed key/count in a control file or DB2 table; on restart skip until past it. z/OS also supports system checkpoints and `RESTART=` on the JOB, but application-level keys are more portable.
- Reject unmatched updates/deletes to an exception report.

## Gotchas
- Duplicate transaction keys need a rule (apply in order, or reject).
- HIGH-VALUES must compare higher than any real key under your collating sequence.

## Self-check
Run with transactions for existing, new and missing keys; compare totals in = totals out.
