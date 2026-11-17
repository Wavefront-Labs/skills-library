---
id: computing-software.software-engineering.csharp-dotnet.extension-methods-design
name: extension-methods-design
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-type-system, extension-methods, static-classes, namespace-discovery, extension-blocks, api-design]
level: practitioner
status: docs-checked
description: "Design C# extension methods and C# 14 extension blocks: static class rules, using-based discovery, instance members win, guideline cautions, namespaces, extending object."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/extension-methods", "https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/extension-methods", "https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/tutorials/extension-members"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extension methods

```csharp
namespace Acme.Text;

public static class StringExtensions
{
    public static int WordCount(this string s) => s.Split(' ').Length;   // classic syntax (before C# 14)
}
// call site: using Acme.Text;  "Hello Extension Methods".WordCount()
```

## What they are
- Static methods called with instance syntax; the first parameter follows the `this` modifier and names the extended type. They compile to the same IL as any static method, and can also be called as `StringExtensions.WordCount(s)`.
- They must be declared in a non-nested, non-generic static class, and are only in scope where the namespace is imported with a `using` directive.
- Extension members respect encapsulation: they only see what the extended type's access declarations allow.
- **Instance members win.** The compiler first looks for a matching member on the type; an extension with the same name and signature as an existing instance method is never called. So adding such a method to the type later silently changes which code runs.
- C# 14 adds `extension` blocks (inside a non-nested, non-generic static class): they hold methods, properties and operators, and can extend an instance or the type itself (static extensions). Use `extension(ref Point point)` for a struct receiver when the members must change the caller's value; without `ref` they change a copy. The `this` form remains supported and compiles to the same IL. A later C# 15 adds extension indexers.

## Design guidance (Framework Design Guidelines, marked "not current" by Microsoft)
- Avoid defining extension methods frivolously, especially on types you do not own; if you own the type, prefer instance methods.
- Consider them for helper functionality relevant to every implementation of an interface (the LINQ operators on `IEnumerable<T>`), or to avoid a dependency an instance method would introduce.
- Avoid extending `System.Object`.
- Do not put them in the same namespace as the extended type unless extending interfaces or for dependency management; consider the interface's own namespace if the methods are meant for most or all uses.
- Avoid two extension methods with the same signature, even in different namespaces.
- Put a feature's extension methods in the namespace of that feature, with a descriptive namespace name rather than a generic one like "Extensions".

## Verify
A test compile that omits the `using` confirms discovery is intentional, and a test that an instance method with the same signature takes precedence.

## Checked
2026-11-03. Confirmed against dotnet/docs: "Extension members" (this and extension syntaxes, scope, binding rules), the design guidelines page and the extension members tutorial. Removed because not found there: null-receiver and `ThrowIfNull` advice, `AddXxx`/`UseXxx` service collection conventions and DI-guidelines namespace claim, `ref`/`in` struct receiver for the `this` form, reflection and `[Extension]` attribute remarks, ambiguity error number, and CA1062.
Method: documentation only; no commands were run.
