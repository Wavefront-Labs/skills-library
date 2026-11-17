---
id: computing-software.software-engineering.csharp-dotnet.test-data-builders-and-assertion-libraries
name: test-data-builders-and-assertion-libraries
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-testing-practice, bogus-autofixture, assertion-libraries, shouldly, fluentassertions, test-data]
level: practitioner
status: draft
description: "Generate test data with Bogus and AutoFixture and assert expressively with Shouldly or AwesomeAssertions; deterministic seeds, builders, snapshot testing and licence notes on FluentAssertions 8."
sources: ["https://github.com/bchavez/Bogus", "https://github.com/AutoFixture/AutoFixture", "https://docs.shouldly.org/", "https://awesomeassertions.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test data and assertions

## Bogus (realistic fake data)
```csharp
Randomizer.Seed = new Random(8675309);                        // deterministic across runs
var faker = new Faker<User>()
    .RuleFor(u => u.Id, f => f.IndexFaker)
    .RuleFor(u => u.Email, (f, u) => f.Internet.Email(u.Name))
    .RuleFor(u => u.Name, f => f.Name.FullName())
    .RuleFor(u => u.Age, f => f.Random.Int(18, 90));
var users = faker.Generate(100);
```
Good for seeding databases and realistic-looking load data. Always seed (or log the seed) so failures reproduce.

## AutoFixture (anonymous values)
```csharp
var fixture = new Fixture();
var order = fixture.Build<Order>().With(o => o.Status, "open").Without(o => o.Customer).Create();
// xUnit auto-data: [Theory, AutoData] public void Test(Order o, string name) { }
// with NSubstitute/Moq: AutoFixture.AutoNSubstitute -> new Fixture().Customize(new AutoNSubstituteCustomization())
```
Use it to hide irrelevant constructor parameters; state only the values the test cares about. Recursive graphs need `fixture.Behaviors.OfType<ThrowingRecursionBehavior>().ToList().ForEach(...)` replaced with `OmitOnRecursionBehavior`.

## Hand-written builders
For key domain objects, a `OrderBuilder` with defaults and `WithX()` methods beats generators for readability.

## Assertion libraries
```csharp
result.ShouldBe(42);                              // Shouldly: failure messages include the original expression
list.ShouldContain(x => x.Id == 3);
await Should.ThrowAsync<InvalidOperationException>(() => svc.RunAsync());
// AwesomeAssertions (community fork of FluentAssertions 7, Apache-2.0) keeps the Should() API
actual.Should().BeEquivalentTo(expected, o => o.Excluding(x => x.CreatedAt));
```
**Licence note:** FluentAssertions 8+ requires a paid licence for commercial use; stay on 7.x, move to AwesomeAssertions, or use Shouldly. Check before upgrading.
Snapshot testing: Verify (`VerifyXunit`) stores approved output files; scrub volatile values (`DateTime`, GUIDs).

## Gotchas
- Random test data without a seed produces flaky tests that cannot be reproduced.
- Over-specified equivalence assertions couple tests to irrelevant fields; exclude or use members.
- Don't assert on floating values exactly; use tolerance.
- Mocking everything with AutoFixture hides missing real wiring.

## Verify
Run the suite twice with the same seed and get identical generated data; a deliberately wrong assertion yields a readable message.
