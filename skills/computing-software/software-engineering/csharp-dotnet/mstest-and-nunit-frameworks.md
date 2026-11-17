---
id: computing-software.software-engineering.csharp-dotnet.mstest-and-nunit-frameworks
name: mstest-and-nunit-frameworks
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-testing-practice, mstest-nunit, mstest, nunit, data-driven-tests, test-lifecycle]
level: practitioner
status: draft
description: "MSTest and NUnit essentials for .NET: attributes, lifecycle, data-driven tests, parallelism, categories, Microsoft.Testing.Platform, and mapping to xUnit concepts."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-mstest-writing-tests", "https://docs.nunit.org/", "https://learn.microsoft.com/en-us/dotnet/core/testing/microsoft-testing-platform-intro"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MSTest and NUnit

| Concept | xUnit | MSTest | NUnit |
|---|---|---|---|
| Test | `[Fact]` | `[TestMethod]` (class `[TestClass]`) | `[Test]` (`[TestFixture]` optional) |
| Data rows | `[Theory][InlineData]` | `[DataRow(1,2)]` / `[DynamicData]` | `[TestCase(1,2)]` / `[TestCaseSource]` |
| Setup per test | ctor | `[TestInitialize]` | `[SetUp]` |
| Teardown | `IDisposable` | `[TestCleanup]` | `[TearDown]` |
| Once per class | `IClassFixture<T>` | `[ClassInitialize]` (static) | `[OneTimeSetUp]` |
| Category | `[Trait]` | `[TestCategory("slow")]` | `[Category("slow")]` |

```csharp
[TestClass]
public class PriceTests
{
    [TestMethod] [DataRow(100, 10, 90)] [DataRow(50, 0, 50)]
    public void Discount(int price, int pct, int expected) => Assert.AreEqual(expected, Price.Apply(price, pct));

    [TestMethod] public async Task Throws() => await Assert.ThrowsExceptionAsync<ArgumentOutOfRangeException>(() => Price.ApplyAsync(-1, 5));
    [TestMethod, Timeout(2000)] public void Fast() { }
}
// NUnit
[TestFixture] public class PriceNUnit {
    [TestCase(100, 10, ExpectedResult = 90)] public int Discount(int p, int pct) => Price.Apply(p, pct);
    [Test] public void Constraint() => Assert.That(Price.Apply(10, 10), Is.EqualTo(9).Within(0.01));
}
```
## Running
```bash
dotnet test --filter "TestCategory=slow"          # MSTest/NUnit: category names; xUnit uses Trait=...
dotnet test --logger "trx" --collect:"XPlat Code Coverage"
```
MSTest 3.x ships MSTest.Sdk and supports **Microsoft.Testing.Platform** (`dotnet run`-able test exes, faster, `<TestingPlatformDotnetTestSupport>`); NUnit 4 moved to the constraint model (`Assert.That`); classic `Assert.AreEqual` is under `ClassicAssert`.

## Parallelism and isolation
MSTest: `[assembly: Parallelize(Workers = 4, Scope = ExecutionScope.MethodLevel)]` and `[DoNotParallelize]`. NUnit: `[Parallelizable(ParallelScope.All)]`, `[NonParallelizable]`. xUnit parallelises by class by default. Tests sharing statics/files/DBs must not run in parallel.

## Gotchas
- MSTest creates a new class instance per test; NUnit reuses one fixture instance by default (state leaks across tests unless `[FixtureLifeCycle(InstancePerTestCase)]`).
- `[ClassInitialize]` must be static with a `TestContext` parameter.
- `async void` tests are not awaited; return `Task`.
- Do not mix frameworks in one project.

## Verify
`dotnet test --list-tests` lists expected tests; a failing DataRow shows its own row in results.
