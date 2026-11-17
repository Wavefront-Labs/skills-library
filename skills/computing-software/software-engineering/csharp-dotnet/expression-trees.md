---
id: computing-software.software-engineering.csharp-dotnet.expression-trees
name: expression-trees
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-reflection, expression-trees, linq-expressions, expressionvisitor, iqueryable, dynamic-queries]
level: advanced
status: docs-checked
description: "Use C# expression trees: Expression<TDelegate>, compiling lambdas, immutability, ExpressionVisitor rewriting, closure pitfalls and constructs trees cannot contain."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/expression-trees/", "https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/expression-trees/expression-trees-execution", "https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/expression-trees/expression-trees-translating", "https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/expression-trees/expression-trees-explained"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expression trees

An expression tree represents code as a tree data structure in which each node is an expression (a method call, a binary operation such as `x < y`). You can examine, modify or execute it. Entity Framework's LINQ APIs accept expression trees so the C# query can be translated to SQL; the delegate form (`Func<>`) cannot be inspected that way.

```csharp
using System.Linq.Expressions;

Expression<Func<int, bool>> lambda = num => num < 5;   // compiler builds a tree, not a delegate
Func<int, bool> f = lambda.Compile();                  // convert to executable IL as a delegate
bool ok = f(3);
```

You can also build trees by hand from the `System.Linq.Expressions` types (`Expression.Parameter`, `Expression.Constant`, `Expression.Lambda<TDelegate>(body, parameters)`).

## Rules
- Assigning a lambda to `Expression<TDelegate>` makes the compiler emit code that builds the tree. Only expression lambdas (single expression) convert; statement lambdas do not.
- Trees are **immutable**. To change one, subclass `ExpressionVisitor`, override methods such as `VisitBinary` (conditional AND is a binary expression), and return a new tree; unchanged nodes are shared between old and new trees. Calling the base implementation rebuilds a similar node with the visited children.
- Only `LambdaExpression` (and `Expression<TDelegate>`) can be executed, via `Compile()`, which returns a `Delegate` (cast to the right type, or use `DynamicInvoke` when the delegate type is unknown). `CompileToMethod` exists only on .NET Framework. For another expression kind, wrap it with `Expression.Lambda(body, parameters)` first.
- Keep and reuse the compiled delegate; you need not recompile each call. Microsoft cautions against building your own expression-tree caches because comparing two arbitrary trees costs more than the compile.

## Cannot appear in expression trees
`async` lambdas and `await`, statement bodies and assignment, `?.` and null-coalescing assignment, `dynamic` operations, interpolated strings, collection expressions, `throw` expressions, tuples, pattern matching `is` and `switch` expressions, discards, `ref`/`in`/`out` parameters and `ref struct` values, `Index`/`Range`, local function references, named and optional arguments, `params` calls, and attributed lambdas. Newer C# features that can be expressed in earlier syntax appear in that older form.

## Closure pitfalls
- Lambdas create closures over referenced locals. A variable must still be usable when you call `Compile` and when you run the delegate: disposing an `IDisposable` captured by the expression (for example in a `using`) makes the delegate throw `ObjectDisposedException` later.
- Code in the expression may reference other assemblies, which must be available when the tree is defined, compiled and executed, otherwise `ReferencedAssemblyNotFoundException`.
- Be careful about touching `this` state when returning an expression tree through a public API.

## Verify
Compile the tree and run it on sample inputs, then assert that a rewritten tree (for example AND turned into OR by a visitor) returns the expected results on an in-memory list.

## Checked
2026-11-03. Confirmed against dotnet/docs: Expression Trees overview, "Expression trees explained", "Execute expression trees" and "Translate expression trees". Removed because not found there: the hand-built `Expression.Property`/`Equal` sample, the predicate-combining `AndAlso` rebind sample and the claim that separate lambdas cannot be joined without it, LinqKit mention, EF `ToQueryString`, millisecond compile cost, Native AOT remark, closure parameterisation by EF, and `Convert` node remarks.
Method: documentation only; no commands were run.
