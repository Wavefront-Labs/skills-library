---
id: computing-software.software-engineering.cobol.accept-display-statements
name: accept-display-statements
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, accept-display-statements, cobol-edited-pictures, accept-statement, display-upon, console-io]
level: intro
status: docs-checked
description: "Use DISPLAY for output and ACCEPT for console or SYSIN input, with UPON and WITH NO ADVANCING."
sources:
  - https://www.ibm.com/docs/en/cobol-zos/6.4?topic=statements-display-statement
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6pg40.pdf
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACCEPT and DISPLAY
**Goal:** simple terminal and job-stream I/O.

```cobol
DISPLAY 'ENTER NAME: ' WITH NO ADVANCING
ACCEPT WS-NAME
DISPLAY 'TOTAL=' WS-TOTAL-ED UPON CONSOLE
ACCEPT WS-CARD FROM SYSIN
```
- Enterprise COBOL (z/OS): the UPON names allowed for DISPLAY are SYSOUT, SYSLIST, SYSLST, SYSPUNCH, SYSPCH and CONSOLE (or a mnemonic-name for one); ACCEPT FROM allows SYSIN, SYSIPT and CONSOLE. SYSERR is not in IBM's list.
- IBM DISPLAY converts binary and internal decimal items to zoned decimal; a negative value gets a low-order sign overpunch (unreadable output under DISPSIGN(COMPAT)) or a separate sign under DISPSIGN(SEP). The V in a PICTURE is an assumed decimal point with no stored character, so DISPLAY shows no point; move to a numeric-edited field first.
- z/OS: with no UPON (or UPON SYSOUT) DISPLAY writes to the ddname in the OUTDD compiler option; if that DD is not allocated and you are not in the z/OS UNIX environment, a default `SYSOUT=*` DD is allocated. Default and maximum record sizes apply per device (system output 120 default, 255 maximum; console 100).
- z/OS: ACCEPT has no editing or error checking of incoming data. From the system input device it reads records until the receiving area is filled, concatenating successive records, and pads with spaces if EOF comes after some data. ACCEPT with no FROM uses the system input device; from the console it is limited to 114 characters per message.
- GnuCOBOL: `DISPLAY ... UPON SYSERR` (or STDERR) writes to output pipe 2, other devices to pipe 1; with no UPON, CONSOLE is assumed. `ACCEPT ... FROM ENVIRONMENT 'NAME'` reads an environment variable. With no FROM, ACCEPT reads from CONSOLE, and a numeric receiver is parsed like NUMVAL.

## Gotchas
- Check your compiler for UPON device names; SYSERR works in GnuCOBOL, not in the IBM table.
- A numeric ACCEPT receiver does not guarantee numeric content on IBM (no checking is done); validate it.

## Self-check
Run the program with input redirected from a file (GnuCOBOL) or from a SYSIN DD (z/OS) and confirm ACCEPT reads it.

## Checked
Date: 2026-11-08. Read the whole IBM docs DISPLAY page; in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the ACCEPT statement section (data transfer, console, date formats) and SPECIAL-NAMES Table 5; in the Programming Guide PDF the DISPLAY and ACCEPT task sections (OUTDD, default SYSOUT=*); in the GnuCOBOL Programmer's Guide the ACCEPT FROM CONSOLE, ACCEPT FROM ENVIRONMENT and DISPLAY UPON device sections (found by search in the page, sections read in full). Removed: the original `DISPLAY 'ERR' UPON SYSERR` from the IBM-flavoured example (not an IBM name) and the "ACCEPT FROM SYSIN reads the next SYSIN record" claim (IBM reads and concatenates records until the area is filled). Removed the unread ISO source. The old "large volumes of DISPLAY output slow batch jobs" gotcha was removed as unconfirmed.
Method: documentation only; no commands were run.
