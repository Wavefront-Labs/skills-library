---
id: computing-software.software-engineering.cobol.class-definition-methods
name: class-definition-methods
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, class-definition-methods, cobol-oo, class-id, method-id, factory-object]
level: advanced
status: draft
description: "Define classes with factory and instance sections and methods in COBOL."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CLASS-ID, METHOD-ID and OBJECT sections
**Goal:** read and write the OO COBOL syntax.

```cobol
CLASS-ID. Account INHERITS Base.
ENVIRONMENT DIVISION.
REPOSITORY.
    CLASS Base IS "java.lang.Object" ...
FACTORY.
  PROCEDURE DIVISION.
  METHOD-ID. newAccount.
  ...
  END METHOD newAccount.
END FACTORY.
OBJECT.
  DATA DIVISION. WORKING-STORAGE SECTION.
  01 balance PIC S9(9)V99.
  PROCEDURE DIVISION.
  METHOD-ID. deposit.
  ...
END OBJECT.
END CLASS Account.
```
- Defined by the ISO 2002 standard; IBM Enterprise COBOL implemented it for Java interoperability (IBM has deprecated OO COBOL in newer releases; unconfirmed exact version).
- GnuCOBOL does not implement OO COBOL (as of 3.x).
- Practical advice: for new work use procedural COBOL with callable programs and keep OO usage only for existing Java-COBOL code.

## Gotchas
- Syntax details (REPOSITORY entries, class names for Java) are compiler specific; start from the vendor sample.
- Check the roadmap before investing: availability varies by compiler and release.

## Self-check
Confirm your compiler version accepts `CLASS-ID` by compiling a minimal class before any design work.
