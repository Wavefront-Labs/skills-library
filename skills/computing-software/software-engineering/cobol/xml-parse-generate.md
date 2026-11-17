---
id: computing-software.software-engineering.cobol.xml-parse-generate
name: xml-parse-generate
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, xml-parse-generate, cobol-json-xml, xml-parse, xml-generate, processing-procedure]
level: advanced
status: docs-checked
description: "Parse XML via event processing procedures and generate XML from COBOL data (Enterprise COBOL for z/OS 6.4 rules)."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XML PARSE and XML GENERATE
**Goal:** exchange XML documents. Rules below are from the Enterprise COBOL for z/OS 6.4 Language Reference.

```cobol
XML PARSE WS-XML PROCESSING PROCEDURE 5000-XML-EVENT
    ON EXCEPTION DISPLAY 'XML-CODE ' XML-CODE
END-XML
...
5000-XML-EVENT.
    EVALUATE XML-EVENT
        WHEN 'START-OF-ELEMENT'  ...
        WHEN 'CONTENT-CHARACTERS' MOVE XML-TEXT TO WS-VALUE
    END-EVALUATE.

XML GENERATE WS-OUT FROM CUST-REC COUNT IN WS-LEN
```
- XML PARSE parses a document into pieces and passes each one, one at a time, to a user-written processing procedure. Two parsers sit behind it, chosen by the `XMLPARSE` compiler option: `XMLPARSE(XMLSS)` (z/OS XML System Services) or `XMLPARSE(COMPAT)` (the run-time parser, compatible with Enterprise COBOL 3).
- Special registers: `XML-EVENT` (`PICTURE X(30)`, holds the event name such as START-OF-ELEMENT, CONTENT-CHARACTERS or EXCEPTION; cannot be a receiving item), `XML-CODE` (`S9(9)` binary; zero for every event except EXCEPTION), and `XML-TEXT` or `XML-NTEXT` for the text.
- XML-CODE after XML GENERATE is zero on success or a nonzero error code. COUNT IN on XML GENERATE returns the number of characters generated.
- Input item rules: alphanumeric or national (group or elementary), not dynamic-length. A national item must hold UTF-16BE (CCSID 1200).
- Under XMLPARSE(XMLSS) the document is parsed with the code page from the ENCODING phrase, else the CODEPAGE compiler option, and any encoding declaration in the document is ignored. ENCODING, RETURNING NATIONAL and VALIDATING are allowed only with XMLSS.
- Schema validation is the `VALIDATING` phrase (XMLSS only). The schema is in a preprocessed format called Optimized Schema Representation (OSR), held in a data item or in a file named via the XML-SCHEMA clause. The FILE form is not supported under CICS. A validation failure raises an EXCEPTION event with return code 24 in the high-order halfword of XML-CODE.

## Gotchas
- With COMPAT, a national document must not contain character entities that need multiple encoding units; use a character reference such as `&#x10813;` with a lowercase x.
- Source and COBOL code-page mismatch (for example UTF-8 versus EBCDIC) garbles text; set the encoding deliberately.

## Self-check
Round-trip a record through XML GENERATE then XML PARSE and compare.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed in the 6.4 Language Reference text: XMLPARSE option, XML PARSE format and phrase rules, XML-CODE and XML-EVENT definitions, event names used in the example, COUNT IN, VALIDATING and OSR. Removed: the GnuCOBOL 3.2 claim, the "single call" and "must not consume the buffer" gotchas (no support found), and the unconfirmed-detail wording on validation.
