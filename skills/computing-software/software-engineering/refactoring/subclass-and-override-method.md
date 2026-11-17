---
id: computing-software.software-engineering.refactoring.subclass-and-override-method
name: subclass-and-override-method
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, legacy-code, subclass-and-override, extract-and-override, seams, test-doubles]
level: advanced
status: draft
description: "Break dependencies in legacy code with Subclass and Override Method and Extract and Override Call/Factory Method, creating testing subclasses that neutralise side effects."
sources: ["https://www.oreilly.com/library/view/working-effectively-with/0131177052/", "https://martinfowler.com/bliki/LegacySeam.html", "https://www.jetbrains.com/help/idea/extract-method.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subclass and override / extract and override call

Feathers' core dependency-breaking technique for object-oriented code: isolate the troublesome
behaviour in a method, then override it in a test-only subclass (an **object seam**).

## Extract and Override Call
```java
class InvoiceProcessor {
    public void process(Invoice inv) {
        validate(inv);
        sendToLedger(inv);            // was: LedgerClient.getInstance().post(inv.toLedgerEntry());
        inv.markProcessed();
    }
    protected void sendToLedger(Invoice inv) { LedgerClient.getInstance().post(inv.toLedgerEntry()); }
}
// test
class TestingInvoiceProcessor extends InvoiceProcessor {
    List<Invoice> sent = new ArrayList<>();
    @Override protected void sendToLedger(Invoice inv) { sent.add(inv); }
}
```
1. Extract the call into a new method (IDE Extract Method), protected/virtual.
2. Subclass in test code and override to record or fake.
3. Test the rest of the logic through the subclass.

## Extract and Override Factory Method
Constructor creates a collaborator (`this.mailer = new SmtpMailer()`): move creation into
`protected Mailer makeMailer()` and override it. Caution: in Java/C# calling overridable methods
from constructors runs the subclass override before subclass fields are initialised; C++ calls the
base version. Prefer Extract and Override **Getter** (lazy creation in a getter) in those cases.

## Subclass and Override Method (general)
Any method doing something irritating (I/O, time, randomness, UI) can be overridden: `now()`,
`showDialog()`, `readConfig()`. Override with the simplest stand-in.

## Requirements and limits
- Language must allow overriding: `virtual` in C#/C++, non-final in Java/Kotlin (Kotlin classes are
  final by default: `open` them or use the all-open plugin for tests), any method in Python/Ruby
  (where monkeypatching is the dynamic equivalent).
- It's a stepping stone. The testing subclass couples tests to internals; once tests exist, refactor
  towards injected collaborators (Parameterize Constructor, Extract Interface).
- Don't override the method under test, only its dependencies.
