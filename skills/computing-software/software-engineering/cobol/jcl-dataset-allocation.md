---
id: computing-software.software-engineering.cobol.jcl-dataset-allocation
name: jcl-dataset-allocation
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, jcl-dataset-allocation, cobol-jcl, disp-parameter, space-allocation, dcb-recfm-lrecl, blksize]
level: practitioner
status: draft
description: "Allocate new datasets and choose DISP, SPACE and DCB values for COBOL files."
sources:
  - https://www.ibm.com/docs/en/zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DISP, SPACE, DCB and dataset allocation
**Goal:** correct allocation for each output file.

- `DISP=(status,normal,abnormal)`: status NEW, OLD, SHR, MOD; normal CATLG, KEEP, DELETE, PASS; abnormal usually DELETE or CATLG.
- `SPACE=(CYL|TRK|blocklen,(primary,secondary[,dir]),RLSE)`.
- `DCB` (or `RECFM=`, `LRECL=`, `BLKSIZE=` shortcuts); `BLKSIZE=0` (or omitted with system-determined blocksize) lets the system pick an optimal size.
- `RECFM=FB` fixed blocked, `VB` variable blocked, `FBA`/`VBA` ASA carriage control; `LRECL` must match the COBOL record (plus 4 for RDW in VB).
- SMS: `DATACLAS=`, `STORCLAS=`, `MGMTCLAS=` where used.

## Gotchas
- `DISP=OLD` gives exclusive access; use SHR for read-only inputs.
- LRECL, RECFM and RECORD CONTAINS mismatches give OPEN status 39 or abend S013.
- ABEND S0C4-class after OPEN is usually a DCB or storage issue, not DISP.

## Self-check
Rerun the job: with DISP=(NEW,CATLG,DELETE) it fails on an existing dataset (JCL error); change to MOD or delete first.
