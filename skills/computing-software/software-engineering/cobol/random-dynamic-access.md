---
id: computing-software.software-engineering.cobol.random-dynamic-access
name: random-dynamic-access
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, random-dynamic-access, cobol-indexed-relative, start-statement, read-next, rewrite-delete, dynamic-access]
level: practitioner
status: docs-checked
description: "Position and iterate keyed files with START and READ NEXT, and update with REWRITE and DELETE."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# START, READ NEXT, REWRITE, DELETE and random reads
**Goal:** browse and update indexed or relative files by key (Enterprise COBOL for z/OS rules).

```cobol
MOVE '1000' TO CUST-ID
START CUST KEY IS >= CUST-ID
    INVALID KEY SET NO-MORE TO TRUE
END-START
PERFORM UNTIL NO-MORE
    READ CUST NEXT RECORD
        AT END SET NO-MORE TO TRUE
        NOT AT END PERFORM SHOW-REC
    END-READ
END-PERFORM
```
- START positions within an indexed or relative file for later sequential retrieval. The file must be open INPUT or I-O and in sequential or dynamic access. Relations: EQUAL TO (=), GREATER THAN (>), NOT LESS THAN (NOT <), GREATER THAN OR EQUAL TO (>=). Without a KEY phrase, EQUAL to the prime record key is implied.
- If no record satisfies the comparison, the invalid key condition holds and the position is undefined. A successful START makes the key used the key of reference for later READs.
- For indexed files the START key is compared as alphanumeric. The Language Reference warns that a numeric key must use EQUAL TO, or results can be unexpected.
- Dynamic access: use `READ file NEXT RECORD` for sequential retrieval (NEXT is mandatory in dynamic mode, optional in sequential mode). Format 2 `READ file RECORD [INTO x] [KEY IS key]` is the random read; KEY IS applies only to indexed files and names a record key (prime or alternate). Without KEY, the prime record key is the key of reference. In dynamic access the key of reference stays in force for later sequential READs until a different one is established.
- Before a sequential READ the file position must have been set by a successful OPEN, START, or READ.
- REWRITE needs the file open in I-O mode. In sequential access the previous I/O statement must be a successful READ, and for indexed files the prime key must still equal that of the record read (otherwise invalid key). In random or dynamic access the record is chosen by the prime record key (indexed) or RELATIVE KEY (relative); a missing record gives invalid key. REWRITE does not move the file position indicator.
- DELETE needs I-O mode. In sequential access the previous statement must be a successful READ and INVALID KEY must not be specified. In random or dynamic access the prime record key or RELATIVE KEY selects the record; absent means invalid key. DELETE does not change the record area or the file position indicator.

## Gotchas
- INVALID KEY covers keyed conditions (START, random READ, WRITE, REWRITE, DELETE); a sequential READ uses AT END. Other failures are reported through FILE STATUS or a USE AFTER ERROR declarative.
- A rewritten alternate key may change; the access path stays consistent. An alternate key without DUPLICATES that collides with an existing record makes REWRITE invalid key (status 22).
- With duplicate alternate keys, sequential reads return records in the order written, but a random READ returns only the first record written.

## Self-check
START at a key, READ NEXT three times, REWRITE the third, and reread it to confirm the update.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted): START statement (formats, KEY phrase, indexed and relative rules), READ statement (sequential, random, dynamic sections), REWRITE, DELETE, ACCESS MODE clause, ALTERNATE RECORD KEY clause, Invalid key condition and the File status key table. Confirmed that START needs sequential or dynamic access; rewrote the REWRITE rules (sequential access requires a prior successful READ; random and dynamic use the key) and added the numeric-key START warning. Removed the unread ISO, ibm.com/docs and GnuCOBOL sources.
Method: documentation only; no commands were run.
