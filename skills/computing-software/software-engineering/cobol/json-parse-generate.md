---
id: computing-software.software-engineering.cobol.json-parse-generate
name: json-parse-generate
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, json-parse-generate, cobol-json-xml, json-parse, json-generate, json-name-mapping]
level: advanced
status: docs-checked
description: "Convert between COBOL group items and JSON text with JSON GENERATE and JSON PARSE (Enterprise COBOL for z/OS 6.4 rules)."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON PARSE and JSON GENERATE
**Goal:** produce and consume JSON from COBOL records. Rules below are from the Enterprise COBOL for z/OS 6.4 Language Reference.

```cobol
JSON GENERATE WS-JSON-TEXT FROM CUST-REC
    COUNT IN WS-JSON-LEN
    ON EXCEPTION PERFORM JSON-ERROR
END-JSON

JSON PARSE WS-JSON-TEXT INTO CUST-REC
    WITH DETAIL
    NAME OF CUST-ID IS 'id'
    ON EXCEPTION DISPLAY JSON-CODE
END-JSON
```
- `JSON-CODE` is a special register defined as `PICTURE S9(9) USAGE BINARY VALUE 0`. After either statement it holds zero on success or a nonzero exception code. JSON PARSE also sets `JSON-STATUS` (same definition) for nonexception conditions.
- The generated text is UTF-8 (CCSID 1208), except UTF-16BE (CCSID 1200) when the receiver is national, or an EBCDIC CCSID when the receiver is alphanumeric and ENCODING names one.
- The receiver may be alphanumeric, national or UTF-8 (elementary or group). It must be big enough: the manual suggests 2 to 3 times the size of the source, depending on data-name lengths; otherwise an exception condition exists. COUNT IN gives the number of characters (or bytes) actually generated.
- No white space is inserted into the output, and if the receiver is longer than the text only the generated part is changed, so initialise it or use COUNT IN.
- JSON names come from the NAME phrase if given; otherwise the exact mixed-case spelling of the data-name is kept (not folded to upper case). FILLER items, REDEFINES items and RENAMES items are ignored.
- Numeric fields are converted to character form then trimmed: leading zeros are removed up to the digit before the decimal point, trailing zeros after the point are kept (0013 becomes 13, 0000.45 becomes 0.45). `"` and `\` are escaped as `\"` and `\\`.
- A table with zero occurrences is written as an empty array, e.g. `{"name":[]}`.
- WITH DETAIL on JSON PARSE makes the parser emit runtime messages for nonexception and exception conditions. The NAME phrase on JSON PARSE changes the name used to match a JSON name/value pair.
- SUPPRESS (with WHEN ZERO/SPACES/LOW-VALUES/HIGH-VALUES or EVERY NUMERIC/NONNUMERIC) omits items from generated output.

## Gotchas
- JSON GENERATE and JSON PARSE share `JSON-CODE`: if you generate inside the processing of a parse, save and restore `JSON-CODE`.
- Every elementary item generated must have a USAGE other than POINTER, FUNCTION-POINTER, PROCEDURE-POINTER or OBJECT REFERENCE, and non-FILLER data names must be unique within the source.

## Self-check
Generate JSON for a small record, then parse it back into a second record and compare field by field.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed in the 6.4 Language Reference text: JSON-CODE definition, JSON GENERATE receiver and source rules, encoding, COUNT, name formation, trimming, empty tables, WITH DETAIL and NAME on PARSE. Removed: the claimed 6.1+ release gate, the upper-case name claim (the manual keeps mixed case), and the unverified GnuCOBOL 3.2 claim.
