---
id: computing-software.software-engineering.refactoring.extract-interface
name: extract-interface
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, extract-interface, interfaces, dependency-inversion, test-doubles, dealing-with-generalization]
level: practitioner
status: draft
description: "Extract an interface from a class to decouple clients, enable test doubles or multiple implementations, keeping it narrow and owned by the client."
sources: ["https://refactoring.guru/extract-interface", "https://www.jetbrains.com/help/idea/extract-interface.html", "https://www.oreilly.com/library/view/working-effectively-with/0131177052/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Extract Interface

**Motivation:** several clients use the same subset of a class, you need a substitute for tests
(Feathers' main use in legacy code), or you want more implementations. Create an interface with that
subset and make clients depend on it.

## Mechanics
1. Decide the methods clients actually use (often a small subset). Name the interface after the
   **role** (`PaymentAuthorizer`, `Clock`, `OrderStore`), not `IThingImpl`-style mirrors of the class.
2. Create the interface; declare that the class implements it. IDE: IntelliJ "Refactor > Extract
   Interface" (can update usages to the interface), Rider/VS "Extract interface", VS Code Java/TS
   code actions.
3. Change client declarations (fields, parameters) from the class to the interface, one client at a
   time, compiling as you go.
4. Introduce substitutes: fakes/stubs in tests, alternative implementations.

```java
interface Clock { Instant now(); }
final class SystemClock implements Clock { public Instant now() { return Instant.now(); } }
class InvoiceService { InvoiceService(Clock clock, ...) {...} }
// test: new InvoiceService(() -> Instant.parse("2026-10-18T00:00:00Z"), ...)
```

## Design rules
- **Interface segregation**: one fat interface per class is a mirror; several role interfaces
  let clients depend on only what they use.
- Put the interface in the **client's** package/module (dependency inversion), so the
  implementation depends on the client's abstraction, not vice versa.
- Don't extract interfaces for every class "just in case"; one implementation and no test need is
  ceremony. In Python/TS, structural types (`Protocol`, TS interfaces) let you add the type
  without touching the class.
- Static/non-virtual dependencies in legacy code (C++, sealed classes) may need Feathers' "Extract
  Implementer" (rename class to impl, extract interface with the old name) to avoid changing callers.

## Verify
Clients compile against the interface only (search for remaining concrete references), and tests
can construct the client with a fake.
