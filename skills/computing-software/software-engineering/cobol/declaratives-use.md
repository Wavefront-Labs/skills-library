---
id: computing-software.software-engineering.cobol.declaratives-use
name: declaratives-use
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, declaratives-use, cobol-exceptions, declaratives, use-after-error, error-section]
level: advanced
status: docs-checked
description: "Centralize file error handling with a USE AFTER STANDARD ERROR declarative section, including when it runs and its restrictions."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DECLARATIVES with USE AFTER ERROR PROCEDURE
**Goal:** one handler for I/O errors that have no local phrase (Enterprise COBOL for z/OS rules).

```cobol
PROCEDURE DIVISION.
DECLARATIVES.
IO-ERRORS SECTION.
    USE AFTER STANDARD ERROR PROCEDURE ON CUST-FILE.
IO-ERR-PARA.
    DISPLAY 'FILE ERROR STATUS ' WS-FS
    MOVE 16 TO RETURN-CODE.
END DECLARATIVES.
MAIN SECTION.
MAIN-PARA.
    ...
```
- Declaratives must be grouped at the start of the PROCEDURE DIVISION, after the header, and the whole PROCEDURE DIVISION must then be divided into sections. DECLARATIVES and END DECLARATIVES each start in Area A, end with a period and share no line with other text. Each declarative section header is followed by a period and a USE statement with a period.
- The USE statement is never executed; it defines the condition under which the following paragraphs run. When the procedure's last statement runs, it exits and control returns to the routine that triggered it.
- Form: `USE [GLOBAL] AFTER STANDARD {EXCEPTION | ERROR} PROCEDURE ON {file-name... | INPUT | OUTPUT | I-O | EXTEND}`. EXCEPTION and ERROR are synonyms. I-O is valid for direct-access files. No sort or merge file can be named. Only one such procedure can apply to any file; a file-name declarative takes precedence over an open-mode one.
- It runs in addition to the standard system error routine, in three situations: after the system-defined I/O error routine; when an INVALID KEY or AT END condition occurs and the statement has no such phrase; and for an IBM-defined condition that sets file status key 1 to 9. It does not run when the statement does carry the INVALID KEY or AT END phrase that handles the condition.
- It can be activated by READ, WRITE, REWRITE, START, OPEN, CLOSE or DELETE errors. The file status value is set before the declarative runs, so the procedure can inspect it.
- After it finishes, control returns to the I/O system; unless the status shows a critical I/O error, control continues at the next executable statement after the failed I/O statement. So later logic must not assume success.
- Declarative and non-declarative procedures may PERFORM each other, and may GO TO from a declarative into either kind. A declarative may re-execute itself, but you must ensure an eventual exit to avoid an infinite loop.

## Gotchas
- You cannot use GOBACK or STOP RUN while an EXCEPTION/ERROR declarative is active because of a QSAM abend on READ, WRITE or REWRITE (status can be 34 or 90); EXIT PROGRAM is also barred in a non-nested subprogram in that case. In a nested program, GOBACK and EXIT PROGRAM are barred while any declarative is active, and in a method, GOBACK and EXIT METHOD.
- Nested programs: the first qualifying declarative wins, in this order: file-specific in the program with the failing statement, mode-specific there, then GLOBAL file-specific and GLOBAL mode-specific ones in the containing programs outward.
- Declarative sections in a declaratives part must have priority numbers 0 to 49, if any; priority numbers are not allowed in a method, a RECURSIVE program or a THREAD-compiled program.

## Self-check
Open a missing non-optional file with no FILE STATUS clause and no inline phrase, and observe that the declarative runs; add an inline handler and observe that it does not.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted): Declaratives and Procedures (priority numbers), USE statement (EXCEPTION/ERROR declarative, precedence rules for nested programs), Invalid key condition and At end condition. Rewrote the vague "some compilers" wording: the PDF states that the procedure runs only when the INVALID KEY or AT END phrase is absent. Removed the unsupported "declaratives cannot be nested" claim and the unread ISO, ibm.com/docs and GnuCOBOL sources. Changed the self-check to match documented behaviour (it was not run).
Method: documentation only; no commands were run.
