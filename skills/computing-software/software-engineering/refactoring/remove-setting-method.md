---
id: computing-software.software-engineering.refactoring.remove-setting-method
name: remove-setting-method
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, remove-setting-method, encapsulation, immutability, constructor-initialization]
level: practitioner
status: draft
description: "Remove setters for fields that should not change after construction, moving initialisation into constructors or factories and making fields immutable."
sources: ["https://refactoring.com/catalog/removeSettingMethod.html", "https://martinfowler.com/books/refactoring.html", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-8.html#jls-8.3.1.2"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remove Setting Method

**Motivation:** a setter says "this may change". If a field (like an id or creation date) must
not change after the object is created, the setter is a lie and an invitation to bugs.

## Mechanics (Fowler)
1. If the value isn't already a constructor parameter, use **Change Function Declaration** to add it.
   Make the constructor assign the field.
2. Find each caller of the setter. Where it's called just after construction, move the value into
   the constructor call. Where it's called later, stop: the field really is mutable, or the design
   needs a new object instead (value object replacement).
3. Run tests after each caller change.
4. Remove the setter. Make the field `final` / `readonly` / `val` / frozen so the compiler enforces it.
5. Test.

```java
// before
Person p = new Person(); p.setId("1234");
// after
Person p = new Person("1234");
class Person { private final String id; Person(String id) { this.id = id; } String getId() { return id; } }
```

## Language notes
- C#: `{ get; init; }` allows object initialisers but not later mutation; `readonly` fields;
  `record` types.
- Kotlin: `val`; Python: `@dataclass(frozen=True)` or properties without setters; TypeScript: `readonly`.
- Frameworks that require setters (old JavaBeans, JPA, some serializers): use field access,
  constructor binding (Jackson `@JsonCreator`, Spring Boot `@ConstructorBinding`, EF Core
  constructor binding), or package-private setters for the framework only.

## Related
Many required parameters after this -> **Replace Constructor with Factory Function** or a builder.
For fields that legitimately change as a business action, replace generic setters with intention-
revealing methods (`account.close(reason)`), not public `setStatus()`.
