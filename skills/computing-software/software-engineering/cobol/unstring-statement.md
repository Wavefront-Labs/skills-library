---
id: computing-software.software-engineering.cobol.unstring-statement
name: unstring-statement
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, unstring-statement, parsing, delimiter-in, count-in, tallying]
level: intro
status: docs-checked
description: "Split delimited text with UNSTRING and capture delimiters, counts and field tallies."
sources:
  - https://www.ibm.com/docs/en/cobol-zos/6.4?topic=statements-unstring-statement
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UNSTRING (parsing) with DELIMITER, COUNT and TALLYING
**Goal:** parse CSV-like records (Enterprise COBOL for z/OS rules).

```cobol
UNSTRING IN-LINE DELIMITED BY ',' OR ';'
    INTO F1 COUNT IN C1
         F2 COUNT IN C2
         F3
    WITH POINTER WS-P
    TALLYING IN WS-FIELDS
    ON OVERFLOW PERFORM TOO-MANY
END-UNSTRING
```
- Receivers fill in order. Overflow occurs when the pointer is less than 1, the pointer exceeds the sending field length, or all receivers have been used and the sending field still has unexamined characters; NOT ON OVERFLOW is then ignored.
- Several delimiters are an OR condition: each non-overlapping occurrence of any one is recognised in the order specified. A multi-character delimiter counts only if its characters are contiguous and in order.
- `DELIMITER IN` moves the delimiter that ended each field (spaces if the field ended at the end of the sender); `COUNT IN` receives the number of characters examined, excluding the delimiter.
- WITH POINTER and TALLYING IN fields must be initialized by you before the statement; the pointer ends at its initial value plus the positions examined and the tally at its initial value plus the receivers acted on. They must be integers without P in the PICTURE.
- A numeric receiver must be usage DISPLAY or NATIONAL with no P in its PICTURE. Data is moved with the normal MOVE rules for the sender and receiver categories.
- Without DELIMITED BY, each receiver takes as many characters as its own size; DELIMITER IN and COUNT IN are not allowed then.

## Gotchas
- Consecutive delimiters give a receiver filled with spaces or zeros unless `DELIMITED BY ALL` is specified, in which case they count as one delimiter.
- The format has no phrase for quoted fields, so a CSV field with embedded commas needs your own parsing.

## Self-check
Parse `A,,C` with `DELIMITED BY ','` into three alphanumeric receivers and verify the middle one is spaces and the tally is 3.

## Checked
Date: 2026-11-08. Read the whole IBM docs UNSTRING page and, in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted), the UNSTRING format and Data flow sections. Confirmed the phrase order of the example against the format, overflow conditions, OR delimiters, ALL, DELIMITER IN, COUNT IN, POINTER, TALLYING and numeric receiver rules. Removed: the hex tab delimiter X'09' (tab is not X'09' on EBCDIC systems and the page does not cover it), the NUMVAL advice and the unconfirmed "no quote handling" claim was reworded to the format having no such phrase. Removed the unread ISO and GnuCOBOL root sources.
Method: documentation only; no commands were run.
