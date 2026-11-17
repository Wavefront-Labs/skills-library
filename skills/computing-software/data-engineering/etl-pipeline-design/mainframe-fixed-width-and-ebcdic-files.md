---
id: computing-software.data-engineering.etl-pipeline-design.mainframe-fixed-width-and-ebcdic-files
name: mainframe-fixed-width-and-ebcdic-files
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, fixed-width-files, ebcdic, copybooks, mainframe]
level: advanced
status: gated
description: "Ingest mainframe extracts: fixed-width layouts from COBOL copybooks, EBCDIC code pages, packed decimal (COMP-3), signed fields, redefines and record validation."
sources:
  - https://github.com/AbsaOSS/cobrix
  - https://www.ibm.com/docs/en/cobol-zos/6.4?topic=clauses-usage-clause
  - https://pandas.pydata.org/docs/reference/api/pandas.read_fwf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mainframe / fixed-width / EBCDIC files

**Goal:** decode mainframe extracts into correct, typed rows, not mojibake and wrong amounts.

## Get the layout
Ask for the **COBOL copybook** and the code page. A copybook defines offsets, lengths and types:
```
01 CUSTOMER-REC.
   05 CUST-ID        PIC 9(8).
   05 CUST-NAME      PIC X(30).
   05 BALANCE        PIC S9(9)V99 COMP-3.
   05 OPEN-DATE      PIC 9(8).
```
- `PIC X(n)`: n bytes text. `PIC 9(n)`: zoned decimal digits. `V`: implied decimal point (no character stored).
- `COMP-3`: packed decimal, 2 digits per byte + sign nibble: `S9(9)V99` occupies 6 bytes.
- `COMP`/`BINARY`: big-endian binary integers.
- `REDEFINES` / `OCCURS DEPENDING ON`: variable layouts; multiple record types in one file.

Checked here: Python's `cp037` codec decodes EBCDIC (`C3 E4 E2 E3` -> `CUST`); a hand-written COMP-3 pack/unpack of `S9(9)V99` is 6 bytes and round-trips `1234567.89` and `-0.05`; EBCDIC zone D0-D9 decode to `}` and `J`-`R` and C0-C9 to `{` and `A`-`I` in cp037; `pd.read_fwf(..., dtype=str)` keeps leading zeros.

## Decode with a copybook-aware reader
Spark + Cobrix (option names and the `record_format` codes were not run or fetched (gated: unconfirmed, source is paywalled or blocked)):
```python
df = (spark.read.format("cobol")
      .option("copybook", "/Volumes/main/raw/copybooks/customer.cpy")
      .option("encoding", "ebcdic").option("ebcdic_code_page", "cp037")
      .option("record_format", "F")           # fixed; V/VB for variable-length with RDW
      .load("/Volumes/main/raw/mainframe/customer/"))
```
Python for small files: decode text with `bytes.decode("cp037")`, unpack COMP-3 by nibbles. Never convert the whole file EBCDIC->ASCII before parsing: it corrupts packed and binary fields.

## Plain fixed-width ASCII
```python
pd.read_fwf(path, colspecs=[(0, 8), (8, 38), (38, 49)], names=["id", "name", "balance"], dtype=str)
```
Read as strings, then cast; apply implied decimals explicitly.

## Validate
- Record length equals the copybook total for every record.
- Trailer record counts/hash totals match (mainframe extracts often have header/trailer records).
- Sign handling: zoned decimals carry the sign in the last digit's zone (e.g. `}` / `J`-`R` in ASCII renderings).

## Verify
Sum of decoded balances equals the trailer control total; spot-check a few records against the source screen.
