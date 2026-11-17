---
id: computing-software.software-engineering.cobol.invoke-statement
name: invoke-statement
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, invoke-statement, cobol-oo, invoke-method, object-reference, usage-object-reference]
level: advanced
status: docs-checked
description: "Call methods and create objects with INVOKE and manage object references in Enterprise COBOL for z/OS 6.4."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# INVOKE and method calls
**Goal:** use COBOL or Java objects from COBOL. Rules below are from the Enterprise COBOL for z/OS 6.4 Language Reference.

```cobol
01 acct USAGE OBJECT REFERENCE Account.
INVOKE Account "newAccount" RETURNING acct
INVOKE acct "deposit" USING BY VALUE amt
SET acct TO NULL
```
- Forms: `INVOKE object-reference "method"`, `INVOKE class-name "method"` (static method of a Java class, factory method of a COBOL class) and `INVOKE class-name NEW`. USING and RETURNING are optional (NEW requires RETURNING), with ON EXCEPTION / NOT ON EXCEPTION and END-INVOKE.
- The class name must appear in the REPOSITORY paragraph of the class or program containing the INVOKE.
- The method name literal (or a data item holding the name) is case-sensitive. Name, argument count and argument types select the matching signature, and the method may be overloaded.
- Arguments must be passed BY VALUE (or LENGTH OF). Argument and return types are restricted to those supported for Java interoperation.
- If the object reference is NULL or not a valid object reference, the result is undefined.
- With NEW on a COBOL class, USING must not be given; with a Java class, USING selects the constructor.
- The ON EXCEPTION condition occurs when the object or class has no method with a matching signature. Without ON EXCEPTION a severity-3 Language Environment condition is raised.
- RETURN-CODE is not set by INVOKE. The compiler does not verify argument conformance; that is the programmer's responsibility.

## Gotchas
- A universal object reference (no class name) is required when the method name comes from a data item.
- An object-reference argument must be typed exactly to the class of the method parameter, not a subclass or superclass.

## Self-check
Create an object, invoke a getter, and print the value to confirm the call chain works.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed in the 6.4 Language Reference text: INVOKE format, class-name, NEW, literal case-sensitivity, BY VALUE, RETURNING, ON EXCEPTION, RETURN-CODE note. Removed: ISO 2002 inline method call claim, Java garbage-collection claim, and "exceptions thrown by Java methods" claim (the manual defines ON EXCEPTION only for signature mismatch).
